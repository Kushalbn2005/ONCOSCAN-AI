from pathlib import Path
import json

import numpy as np
import matplotlib.pyplot as plt

from tensorflow import keras

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

from ml.dataset import DatasetLoader


class Evaluator:
    """
    Model Evaluation Pipeline

    Responsibilities
    ----------------
    • Load trained model
    • Load test dataset
    • Evaluate model
    • Generate predictions
    • Generate confusion matrix
    • Generate classification report
    • Save evaluation artifacts
    """

    def __init__(
        self,
        model_path,
        train_dir,
        test_dir,
        batch_size=32,
        image_size=(224, 224),
    ):

        self.model_path = Path(model_path)

        self.train_dir = train_dir
        self.test_dir = test_dir

        self.batch_size = batch_size
        self.image_size = image_size

        self.model = None
        self.class_names = None

        Path("artifacts/evaluation").mkdir(
            parents=True,
            exist_ok=True
        )

    ###########################################################

    def load_model(self):

        self.model = keras.models.load_model(
            self.model_path
        )

        print("=" * 50)
        print("Model Loaded Successfully")
        print("=" * 50)

    ###########################################################

    def load_test_dataset(self):

        loader = DatasetLoader(

            train_dir=self.train_dir,

            test_dir=self.test_dir,

            batch_size=self.batch_size,

            image_size=self.image_size

        )

        _, _, test_ds = loader.load()

        self.class_names = loader.class_names

        return test_ds

    ###########################################################

    def evaluate(self):

        test_ds = self.load_test_dataset()

        loss, accuracy = self.model.evaluate(
            test_ds,
            verbose=1
        )

        print("=" * 50)
        print(f"Test Loss     : {loss:.4f}")
        print(f"Test Accuracy : {accuracy:.4f}")
        print("=" * 50)

        return test_ds, loss, accuracy

    ###########################################################

    def predict(self, dataset):

        y_true = []
        y_pred = []

        predictions = self.model.predict(
            dataset,
            verbose=1
        )

        predicted_labels = np.argmax(
            predictions,
            axis=1
        )

        for _, labels in dataset:

            y_true.extend(labels.numpy())

        y_true = np.array(y_true)

        y_pred = predicted_labels

        return y_true, y_pred

    ###########################################################

    def generate_classification_report(
        self,
        y_true,
        y_pred,
    ):

        report = classification_report(

            y_true,

            y_pred,

            target_names=self.class_names,

            digits=4

        )

        print("\nClassification Report\n")
        print(report)

        report_path = (
            Path("artifacts/evaluation")
            / "classification_report.txt"
        )

        with open(report_path, "w") as f:
            f.write(report)

    ###########################################################

    def generate_confusion_matrix(
        self,
        y_true,
        y_pred,
    ):

        cm = confusion_matrix(
            y_true,
            y_pred
        )

        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm,
            display_labels=self.class_names
        )

        fig, ax = plt.subplots(
            figsize=(8, 8)
        )

        disp.plot(
            cmap="Blues",
            ax=ax,
            colorbar=False
        )

        plt.title("Confusion Matrix")

        plt.tight_layout()

        plt.savefig(
            "artifacts/evaluation/confusion_matrix.png",
            dpi=300
        )

        plt.close()

    ###########################################################

    def save_metrics(
        self,
        loss,
        accuracy,
    ):

        metrics = {

            "test_loss": float(loss),

            "test_accuracy": float(accuracy)

        }

        with open(
            "artifacts/evaluation/metrics.json",
            "w"
        ) as f:

            json.dump(
                metrics,
                f,
                indent=4
            )

    ###########################################################

    def run(self):

        self.load_model()

        test_ds, loss, accuracy = self.evaluate()

        y_true, y_pred = self.predict(
            test_ds
        )

        self.generate_classification_report(
            y_true,
            y_pred
        )

        self.generate_confusion_matrix(
            y_true,
            y_pred
        )

        self.save_metrics(
            loss,
            accuracy
        )

        print("=" * 50)
        print("Evaluation Completed Successfully")
        print("=" * 50)