from pathlib import Path
from collections import defaultdict
from PIL import Image
from tqdm import tqdm
import logging
import json


class DatasetValidator:

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

    def __init__(self, dataset_path, report_path="artifacts/dataset_report.json"):

        self.dataset_path = Path(dataset_path)
        self.report_path = Path(report_path)

        self.report = {
            "structure": {},
            "image_count": {},
            "invalid_extensions": [],
            "corrupted_images": [],
            "image_sizes": defaultdict(int),
            "channels": defaultdict(int)
        }

        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s - %(message)s"
        )

    # ---------------------------------------------------------

    def validate_structure(self):

        logging.info("Checking dataset structure...")

        required = [
            "Training/glioma",
            "Training/meningioma",
            "Training/pituitary",
            "Training/notumor",
            "Testing/glioma",
            "Testing/meningioma",
            "Testing/pituitary",
            "Testing/notumor",
        ]

        status = True

        for folder in required:

            path = self.dataset_path / folder

            exists = path.exists()

            self.report["structure"][folder] = exists

            if not exists:
                status = False
                logging.error(f"Missing folder: {folder}")

        return status

    # ---------------------------------------------------------

    def count_images(self):

        logging.info("Counting images...")

        for split in ["Training", "Testing"]:

            self.report["image_count"][split] = {}

            split_path = self.dataset_path / split

            if not split_path.exists():
                continue

            for class_dir in split_path.iterdir():

                if class_dir.is_dir():

                    count = len(list(class_dir.glob("*")))

                    self.report["image_count"][split][class_dir.name] = count

    # ---------------------------------------------------------

    def validate_extensions(self):

        logging.info("Checking file extensions...")

        for file in self.dataset_path.rglob("*"):

            if file.is_file():

                if file.suffix.lower() not in self.ALLOWED_EXTENSIONS:

                    self.report["invalid_extensions"].append(str(file))

    # ---------------------------------------------------------

    def find_corrupted_images(self):

        logging.info("Scanning for corrupted images...")

        images = [
            file
            for file in self.dataset_path.rglob("*")
            if file.suffix.lower() in self.ALLOWED_EXTENSIONS
        ]

        for image_path in tqdm(images):

            try:

                with Image.open(image_path) as img:
                    img.verify()

            except Exception:

                self.report["corrupted_images"].append(str(image_path))

    # ---------------------------------------------------------

    def collect_statistics(self):

        logging.info("Collecting image statistics...")

        images = [
            file
            for file in self.dataset_path.rglob("*")
            if file.suffix.lower() in self.ALLOWED_EXTENSIONS
        ]

        for image_path in tqdm(images):

            try:

                with Image.open(image_path) as img:

                    size = f"{img.width}x{img.height}"

                    self.report["image_sizes"][size] += 1

                    self.report["channels"][img.mode] += 1

            except Exception:
                pass

    # ---------------------------------------------------------

    def generate_report(self):

        logging.info("Saving report...")

        self.report_path.parent.mkdir(parents=True, exist_ok=True)

        report = dict(self.report)

        report["image_sizes"] = dict(report["image_sizes"])
        report["channels"] = dict(report["channels"])

        with open(self.report_path, "w") as f:

            json.dump(report, f, indent=4)

    # ---------------------------------------------------------

    def run(self):

        logging.info("Starting Dataset Validation...\n")

        self.validate_structure()

        self.count_images()

        self.validate_extensions()

        self.find_corrupted_images()

        self.collect_statistics()

        self.generate_report()

        logging.info("\nValidation Completed Successfully.")