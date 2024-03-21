import json
import os
import pandas
import sys

output_main_dir = "data"
if not os.path.exists(output_main_dir):
    os.makedirs(output_main_dir)

for input_file in sys.argv[1:]:
    print(input_file)
    sentences_frame = pandas.read_csv(input_file, encoding="utf-8", sep="\t", header=0)
    texts_frame = sentences_frame.groupby(by=["Text-ID"], as_index=False).agg({'Text': list})
    for index, row in texts_frame.iterrows():
        language = row["Text-ID"][0:2]
        if language != "EN" and language != "HE":
            output_dir = os.path.join(output_main_dir, row["Text-ID"])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            data = { "text": row["Text"], "source_lang": language, "target_lang": "EN" }
            with open(os.path.join(output_dir, "request.json"), "w") as request_file:
                json.dump(data, request_file)
            with open(os.path.join(output_dir, "chars.txt"), "w") as length_file:
                length_file.write(str(len("".join(row["Text"]))) + "\n")

