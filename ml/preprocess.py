from pathlib import Path
from PIL import Image
import logging
import numpy as np


class ImageProcessor:
    """
    Image preprocessing pipeline.

    Responsibilities:
    - Load images
    - Convert to RGB
    - Resize images
    - Normalize (for training/inference only)
    - Save processed images
    - Process entire dataset
    """

    def __init__(
        self,
        input_dir,
        output_dir,
        image_size=(224, 224)
    ):

        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.image_size = image_size

        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s - %(message)s"
        )

    # -------------------------------------------------------------

    def load_image(self, image_path: Path) -> Image.Image:
        """
        Load image from disk.
        """
        return Image.open(image_path)

    # -------------------------------------------------------------

    def convert_to_rgb(self, image: Image.Image) -> Image.Image:
        """
        Convert image to RGB.
        """
        return image.convert("RGB")

    # -------------------------------------------------------------

    def resize_image(self, image: Image.Image) -> Image.Image:
        """
        Resize image to configured size.
        """
        return image.resize(self.image_size)

    # -------------------------------------------------------------

    def normalize_image(self, image: Image.Image) -> np.ndarray:
        """
        Convert image into normalized NumPy array.

        NOTE:
        This is NOT used when saving processed images.
        It will be useful during model training/inference.
        """

        image = np.array(image).astype(np.float32)

        image /= 255.0

        return image

    # -------------------------------------------------------------

    def preprocess(self, image_path: Path) -> Image.Image:
        """
        Complete preprocessing pipeline.
        """

        image = self.load_image(image_path)

        image = self.convert_to_rgb(image)

        image = self.resize_image(image)

        return image

    # -------------------------------------------------------------

    def save_image(
        self,
        image: Image.Image,
        output_path: Path
    ) -> None:
        """
        Save processed image.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        image.save(output_path)

    # -------------------------------------------------------------

    def process_dataset(self) -> None:
        """
        Process the complete dataset.
        """

        logging.info("Starting preprocessing...")

        total_images = 0
        failed_images = 0

        valid_extensions = {
            ".jpg",
            ".jpeg",
            ".png"
        }

        for split in ["Training", "Testing"]:

            split_path = self.input_dir / split

            if not split_path.exists():
                continue

            for class_folder in split_path.iterdir():

                if not class_folder.is_dir():
                    continue

                logging.info(
                    f"Processing {split}/{class_folder.name}"
                )

                output_class_folder = (
                    self.output_dir /
                    split /
                    class_folder.name
                )

                for image_path in class_folder.iterdir():

                    if image_path.suffix.lower() not in valid_extensions:
                        continue

                    try:

                        processed = self.preprocess(image_path)

                        output_path = (
                            output_class_folder /
                            image_path.name
                        )

                        self.save_image(
                            processed,
                            output_path
                        )

                        total_images += 1

                    except Exception as e:

                        logging.error(
                            f"Failed: {image_path.name} | {e}"
                        )

                        failed_images += 1

        logging.info("=" * 50)
        logging.info("Preprocessing Completed")
        logging.info(f"Processed Images : {total_images}")
        logging.info(f"Failed Images    : {failed_images}")
        logging.info("=" * 50)