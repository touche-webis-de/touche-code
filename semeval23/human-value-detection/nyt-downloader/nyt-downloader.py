# Authors:
#   - Zeljko Bekcic      https://github.com/zeljkobekcic
#   - Johannes Kiesel    https://github.com/johanneskiesel

import argparse
import html
import pathlib
import time
import unicodedata
from pathlib import Path

import pandas as pd
import spacy
from requests_html import HTMLSession

nlp = spacy.load("en_core_web_sm")

from bs4 import BeautifulSoup


def write_to_cache(url: str, html_content: str):
    cache_dir = pathlib.Path("cache")
    if not cache_dir.exists():
        cache_dir.mkdir()

    filename = url.replace(":", "__COLON__").replace("/", "__SLASH__")
    (cache_dir / filename).write_text(html_content)


def read_from_cache(url: str) -> str:
    cache_dir = pathlib.Path("cache")
    if not cache_dir.exists():
        cache_dir.mkdir()
        raise FileNotFoundError()

    filename = url.replace(":", "__COLON__").replace("/", "__SLASH__")
    target_file = cache_dir / filename
    if not target_file.exists():
        raise FileNotFoundError()

    return target_file.read_text()


def download_raw_article(url: str) -> str:
    session = HTMLSession()
    r = session.get(url)
    r.html.render(timeout = 60)
    return r.html.html


def parse_article_content(html_content: str) -> str:
    _raw_article_content = html.unescape(html_content)
    _raw_article_content = unicodedata.normalize("NFKC", _raw_article_content)
    soup = BeautifulSoup(_raw_article_content, "html.parser")
    soup_headline = soup.find("h1", attrs={"data-testid": "headline"})
    soup_summary = soup.find("p", attrs={"id": "article-summary"})
    soup_paragraphs = soup.find("section", attrs={"name": "articleBody"}).find_all("p")

    fragments = []

    if soup_headline is not None:
        fragments.append(soup_headline.text.strip())

    if (soup_summary is not None) and (stripped_summary := soup_summary.text.strip()):
        fragments.append(stripped_summary)

    paragraphs = []
    for p in soup_paragraphs:
        if str_p := p.text.strip():
            paragraphs.append(str_p)

    text = " ".join(paragraphs)
    doc = nlp(text)
    fragments.extend([str(s) for s in doc.sents])

    return " ".join(fragments)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-file", type=Path, required=True)
    parser.add_argument("--output-file", type=Path, required=True)

    args = parser.parse_args()

    input_file: Path = args.input_file
    output_file: Path = args.output_file
    if not input_file.exists():
        print(f"There is no file at {input_file}")
        return

    df = pd.read_csv(input_file, sep="\t")
    article_urls = set("https://web.archive.org/web/" + df['Internet Archive timestamp'].astype(str) + "/" +  df['URL'])
    articles: dict[str, str] = {}
    for a in article_urls:
        try:
            articles[a] = read_from_cache(a)
            print(f"Used cached data for {a}")
        except FileNotFoundError:
            print(f"Downloading {a}")
            articles[a] = download_raw_article(a)
            print(f"Finished Downloading {a}")
            write_to_cache(a, articles[a])
            time.sleep(10)

    article_content = {a: parse_article_content(c) for a, c in articles.items()}

    result = []
    for i, row in df.iterrows():
        text = article_content["https://web.archive.org/web/" + str(row["Internet Archive timestamp"]) + "/" + row["URL"]]
        conclusion_pos = row["Conclusion token position"]
        conclusion_start, conclusion_end = conclusion_pos.split(":")
        conclusion_start = int(conclusion_start)
        conclusion_end = int(conclusion_end)
        conclusion = text[conclusion_start:conclusion_end]

        premise_pos = row["Premise token position"]
        premise_start, premise_end = premise_pos.split(":")
        premise_start = int(premise_start)
        premise_end = int(premise_end)
        premise = text[premise_start:premise_end]
        result.append(
            {
                "Argument ID": row["Argument ID"],
                "Conclusion": conclusion,
                "Stance": row["Stance"],
                "Premise": premise
            }
        )

    pd.DataFrame(result).to_csv(output_file, sep="\t", index=False)


if __name__ == '__main__':
    main()
