from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


class DatasetLoader:
    """
    TensorFlow Dataset Loader

    Responsibilities
    ----------------
    • Load dataset
    • Split training/validation
    • Apply augmentation
    • Normalize images
    • Batch
    • Prefetch
    """

    def __init__(
        self,
        train_dir,
        test_dir,
        image_size=(224, 224),
        batch_size=32,
        validation_split=0.2,
        seed=42
    ):

        self.train_dir = Path(train_dir)
        self.test_dir = Path(test_dir)

        self.image_size = image_size
        self.batch_size = batch_size
        self.validation_split = validation_split
        self.seed = seed

        self.class_names = None

        self.data_augmentation = keras.Sequential(
            [
                layers.RandomFlip("horizontal"),
                layers.RandomRotation(0.05),
                layers.RandomZoom(0.10),
                layers.RandomContrast(0.10),
            ],
            name="data_augmentation"
        )

    ##########################################################

    def normalize(self, image, label):
        # EfficientNetB0 includes Rescaling(1/255); keep pixels in [0, 255].
        image = tf.cast(image, tf.float32)
        return image, label

    ##########################################################

    def augment(self, image, label):

        image = self.data_augmentation(image)

        return image, label

    ##########################################################

    def load_training_dataset(self):

        train_ds = keras.utils.image_dataset_from_directory(

            self.train_dir,

            validation_split=self.validation_split,

            subset="training",

            seed=self.seed,

            image_size=self.image_size,

            batch_size=self.batch_size

        )

        self.class_names = train_ds.class_names

        return train_ds

    ##########################################################

    def load_validation_dataset(self):

        val_ds = keras.utils.image_dataset_from_directory(

            self.train_dir,

            validation_split=self.validation_split,

            subset="validation",

            seed=self.seed,

            image_size=self.image_size,

            batch_size=self.batch_size

        )

        return val_ds

    ##########################################################

    def load_test_dataset(self):

        test_ds = keras.utils.image_dataset_from_directory(

            self.test_dir,

            shuffle=False,

            image_size=self.image_size,

            batch_size=self.batch_size

        )

        return test_ds

    ##########################################################

    def prepare_dataset(self, dataset, training=False):

        dataset = dataset.map(
            self.normalize,
            num_parallel_calls=tf.data.AUTOTUNE
        )

        # Cache before augment so each epoch still gets fresh transforms.
        dataset = dataset.cache()

        if training:
            dataset = dataset.shuffle(1000)
            dataset = dataset.map(
                self.augment,
                num_parallel_calls=tf.data.AUTOTUNE
            )

        dataset = dataset.prefetch(tf.data.AUTOTUNE)

        return dataset

    ##########################################################

    def load(self):

        train_ds = self.load_training_dataset()

        val_ds = self.load_validation_dataset()

        test_ds = self.load_test_dataset()

        train_ds = self.prepare_dataset(
            train_ds,
            training=True
        )

        val_ds = self.prepare_dataset(
            val_ds
        )

        test_ds = self.prepare_dataset(
            test_ds
        )

        print("=" * 50)

        print("Dataset Loaded Successfully")

        print("=" * 50)

        print(f"Classes      : {self.class_names}")

        print(f"Train Batches: {len(train_ds)}")

        print(f"Valid Batches: {len(val_ds)}")

        print(f"Test Batches : {len(test_ds)}")

        print("=" * 50)

        return train_ds, val_ds, test_ds