import re
import difflib


# --- Token diff ---
def tokenize_with_spans(text: str):
    """
    Tokenize text into (token, start, end).
    Keeps exact character positions.
    """
    tokens = []
    for match in re.finditer(r"\w+|\s+|[^\w\s]", text):
        tokens.append((match.group(), match.start(), match.end()))
    return tokens


def detailed_spans(text_a: str, text_b: str) -> list[tuple[int, int]]:
    """
    Return character spans in text_a that differ from text_b.
    Token-based diff with exact char alignment.
    """
    tokens_a = tokenize_with_spans(text_a)
    tokens_b = tokenize_with_spans(text_b)

    seq_a = [t[0] for t in tokens_a]
    seq_b = [t[0] for t in tokens_b]

    matcher = difflib.SequenceMatcher(None, seq_a, seq_b)

    spans = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue

        # Skip insertion-tags because we want to highlight spans in text_a
        if tag in "replace":
            tokens = " ".join([tup[0] for tup in tokens_b[j1:j2]])
        elif tag == "delete":
            tokens = " ".join([tup[0] for tup in tokens_a[i1:i2]])
        else:
            continue

        # Skip mismatches of newlines, spaces, etc.
        if tokens.strip() == "":
            continue

        start = tokens_a[i1][1]
        end = tokens_a[i2-1][2]
        spans.append((start, end))

    return merge_spans(spans)


def merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping or adjacent spans.
    """
    if not spans:
        return spans

    spans = sorted(spans)
    merged = [spans[0]]

    for start, end in spans[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


# --- sentence diff ---
def split_sentences_with_spans(text: str):
    """
    Returns [(sentence, start, end)]
    """
    pattern = r'[^.!?\n]+[.!?]?|\n'
    sentences = []

    for match in re.finditer(pattern, text):
        s = match.group()
        if s.strip():  # ignore pure whitespace
            sentences.append((s, match.start(), match.end()))

    return sentences


def normalize_sentence(s: str) -> str:
    """
    Normalize for robust matching:
    - lowercase
    - remove non-alphanumeric
    """
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()


def sentence_aware_spans(text_a: str, text_b: str):
    sentences_a = split_sentences_with_spans(text_a)
    sentences_b = split_sentences_with_spans(text_b)

    norm_a = [normalize_sentence(s[0]) for s in sentences_a]
    norm_b = [normalize_sentence(s[0]) for s in sentences_b]

    matcher = difflib.SequenceMatcher(None, norm_a, norm_b)

    final_spans = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        # Skip insertion-tags because we want to highlight spans in text_a
        if tag in ["equal", "insert"]:
            continue

        # Handle deleted or replaced sentences in A
        sub_str_b = " ".join([tup[0] for tup in sentences_b[j1:j2]])
        for idx in range(i1, i2):
            sent_a, start_a, end_a = sentences_a[idx]
            if tag == "delete":
                final_spans.append((start_a, end_a))

            # If we have a counterpart → detailed diff
            else:
                local_spans = detailed_spans(sent_a, sub_str_b)

                # map local → global
                for s, e in local_spans:
                    final_spans.append((start_a + s, start_a + e))

    return merge_spans(final_spans)