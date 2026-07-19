from pathlib import Path

from tensorflow import keras

from ml.dataset import DatasetLoader
from ml.model import BrainTumorClassifier


class Trainer:

    def __init__(

        self,

        train_dir,

        test_dir,

        epochs=20,

        batch_size=32,

        image_size=(224,224)

    ):

        self.train_dir = train_dir
        self.test_dir = test_dir

        self.epochs = epochs
        self.batch_size = batch_size
        self.image_size = image_size

        self.model = None

        self.create_directories()

    ###########################################################

    def create_directories(self):

        Path("artifacts/models").mkdir(
            parents=True,
            exist_ok=True
        )

        Path("artifacts/history").mkdir(
            parents=True,
            exist_ok=True
        )

        Path("artifacts/tensorboard").mkdir(
            parents=True,
            exist_ok=True
        )

    ###########################################################

    def get_callbacks(self):

        callbacks = [

            keras.callbacks.ModelCheckpoint(

                filepath="artifacts/models/best_model.keras",

                monitor="val_accuracy",

                save_best_only=True,

                mode="max",

                verbose=1

            ),

            keras.callbacks.EarlyStopping(

                monitor="val_loss",

                patience=5,

                restore_best_weights=True,

                verbose=1

            ),

            keras.callbacks.ReduceLROnPlateau(

                monitor="val_loss",

                factor=0.2,

                patience=2,

                verbose=1

            ),

            keras.callbacks.CSVLogger(

                "artifacts/history/training_history.csv"

            ),

            keras.callbacks.TensorBoard(

                log_dir="artifacts/tensorboard"

            )

        ]

        return callbacks

    ###########################################################

    def train(self):

        loader = DatasetLoader(

            train_dir=self.train_dir,

            test_dir=self.test_dir,

            batch_size=self.batch_size,

            image_size=self.image_size

        )

        train_ds, val_ds, _ = loader.load()

        builder = BrainTumorClassifier()

        self.model = builder.build()

        history = self.model.fit(

            train_ds,

            validation_data=val_ds,

            epochs=self.epochs,

            callbacks=self.get_callbacks()

        )

        return history