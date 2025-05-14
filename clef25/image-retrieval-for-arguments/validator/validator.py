from collections import defaultdict
import json
from pathlib import Path
import shutil
import zipfile
import settings as s


# project root is image-retrieval-for-arguments
# Read argument_id_list
with open(s.PROJECT_ROOT / "argument_ids_list.txt", "r") as file:
    argument_id_list = [line.strip() for line in file.readlines()]

# Read image_id_list
with open(s.PROJECT_ROOT / "image_id_list.txt", "r") as file:
    image_id_list = [line.strip() for line in file.readlines()]

TMP_DIR = Path.cwd() / "tmp"
if TMP_DIR.exists():
    shutil.rmtree(TMP_DIR)
TMP_DIR.mkdir(parents=True, exist_ok=True)

class Validator:
    def __init__(self, input_file):
        if not Path(input_file).exists():
            raise FileNotFoundError(f"File {input_file} does not exist.")

        self.file_directory = Path(input_file).parent
        self.tmp_dir = TMP_DIR
        self.results = []

        # check if it is a zip file
        if zipfile.is_zipfile(input_file):
            self._unzip_to_tmp_dir(input_file)

            tmp_path = Path(self.tmp_dir)

            dirs_to_check = [tmp_path]

            # Check if 'results.jsonl' exists in the unzipped file
            while dirs_to_check :
                current_dir = dirs_to_check.pop(0)  # Get the next directory to check

                # Check if the 'results.json' exists in the current directory
                if (current_dir / "results.jsonl").exists() :
                    self.file_directory = current_dir
                    break  # Stop searching once we find the directory

                # If not found, add subdirectories of the current directory to the list to check
                for path in current_dir.iterdir() :
                    if path.is_dir() :
                        dirs_to_check.append(path)  # Properly closing the append method

                if not dirs_to_check :
                    raise FileNotFoundError("❗ No results.jsonl found in the unzipped directory.")

        self.file_path = self.file_directory / "results.jsonl"

        if not self.file_directory.exists():
            raise FileNotFoundError(f"File {self.file_path} does not exist.")

        if self.validate_jsonl():
            with open(self.file_path, "r") as file :
                self.results = [json.loads(line.strip()) for line in file]
            self.check_keys()

    def _unzip_to_tmp_dir(self, input_file) :
        with zipfile.ZipFile(input_file, 'r') as zip_ref :
            zip_ref.extractall(self.tmp_dir)
        print(f"Unzipped to: {self.tmp_dir}")

    def validate_jsonl(self):
        with open(self.file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    json.loads(line.strip())
                except json.JSONDecodeError as e:
                    print(f"❗ Invalid JSON on line {line_number}: {e}")
                    return False
        print("✅ JSONL file is valid.")
        return True

    def _get_generated_image_names(self) :
        image_paths = [self.file_directory / "images", self.file_directory / "image"]

        for path in image_paths :
            if path.exists() and path.is_dir() :
                return [image.name for image in path.iterdir() if image.is_file()]

        return []

    def check_keys(self):
        errors = False
        keys_to_check = ["argument_id", "image_id", "rank", "method"]
        invalid_args = []
        id_check_dict = defaultdict(list)
        method_choosen_list = []

        for arg in self.results:
            if not all(key in arg for key in keys_to_check):
                invalid_args.append(arg)
                continue
            method_choosen_list.append(arg["method"])
            id_check_dict[arg["argument_id"]].append(arg)

        if invalid_args:
            print("❗ Invalid entries found:")
            for invalid in invalid_args:
                print(f"  - {invalid}")
            print("❗ Please check your jsonl file.")
            errors = True
            return

        choosen_method = set(method_choosen_list)
        if len(choosen_method) > 1:
            print(f"❗ Multiple methods found: {choosen_method}. Please check your jsonl file.")
            errors = True
            return

        # Check that all argument_ids are present
        if set(argument_id_list) != set(id_check_dict.keys()):
            errors = True
            missing_ids = set(argument_id_list) - set(id_check_dict.keys())
            print(f"❗ Not all argument_ids are present.")
            for missing_id in missing_ids:
                print(f"  - Missing argument_id: {missing_id}")
        else:
            print("✅ All argument_ids are present.")


        # Check that ranks are 1-5
        missing_ranks_list = []
        for key, arguments in id_check_dict.items():
            ranks = {arg.get("rank") for arg in arguments if "rank" in arg}
            expected_ranks = {1, 2, 3, 4, 5}
            missing_ranks = expected_ranks - ranks
            if missing_ranks:
                missing_ranks_list.append((key,missing_ranks,))

        if missing_ranks_list:
            errors = True
            print("❗ Some argument_ids have missing ranks:")
            for key, missing_ranks in missing_ranks_list:
                print(f"  - Argument_id: {key}, Missing ranks: {missing_ranks}")
        else:
            print("✅ All argument_ids have ranks 1-5.")

        # Validate image_id presence in corpus based on method
        if choosen_method == {"retrieval"}:
            for argId, arguments in id_check_dict.items():
                arg_ids_dict = defaultdict(int)
                for arg in arguments:
                    if arg["image_id"] not in image_id_list:
                        errors = True
                        print(f"❗ Image_id {arg['image_id']} for argument_id {arg['argument_id']} is not in the dataset")
                    arg_ids_dict[arg["image_id"]] += 1

                # Check for duplicate submissions
                if len(arg_ids_dict) != len(arguments):
                    errors = True
                    for arg_id, count in arg_ids_dict.items():
                        if count > 1:
                            print(f"❗ Duplicate image_id {arg_id} for argument_id {argId} with count {count}")


        elif choosen_method == {"generation"}:
            generated_image_id_list = self._get_generated_image_names()

            for argId, arguments in id_check_dict.items():
                arg_ids_dict = defaultdict(int)
                for arg in arguments:

                    if arg["image_id"] not in generated_image_id_list:
                        errors = True
                        print(f"❗ Generated image_id {arg['image_id']} for argument_id {arg['argument_id']} is missing")
                    if "prompt" not in arg: # generation submission requires additional key prompt
                        errors = True
                        print(f"❗ Prompt is missing for argument_id {arg['argument_id']} and image_id {arg['image_id']}")
                    arg_ids_dict[arg["image_id"]] += 1

                # Check for duplicate submissions
                if len(arg_ids_dict) != len(arguments) :
                    errors = True
                    for arg_id, count in arg_ids_dict.items() :
                        if count > 1 :
                            print(f"❗ Duplicate image_id {arg_id} for argument_id {argId} with count {count}")

        else:
            print(f"❗ Unknown method: {choosen_method}. Please check your jsonl file.")
            errors = True

        if errors:
            print("❗ Validation failed.")
        else:
            print("✅ Validation passed.")

if __name__ == "__main__":
    input_file = s.PROJECT_ROOT / "tests"/ "random"/ "results.jsonl"  # Replace with your input file
    # input_file = s.PROJECT_ROOT / "tests" / "generation-smoke-data.zip"  # Replace with your input file

    validator = Validator(input_file)
