from ml.preprocess import ImageProcessor

processor = ImageProcessor(
    input_dir="data/raw",
    output_dir="data/processed",
    image_size=(224, 224)
)

processor.process_dataset()