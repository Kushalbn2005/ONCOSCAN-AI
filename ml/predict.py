from pathlib import Path

import cv2
import numpy as np

from tensorflow import keras


class Predictor:
    """
    Brain Tumor Inference Pipeline

    Responsibilities
    ----------------
    • Load trained model
    • Load MRI image
    • Preprocess image
    • Predict class
    • Return confidence scores
    """

    ###########################################################

    def __init__(

        self,

        model_path,

        image_size=(224, 224)

    ):

        self.model_path = Path(model_path)

        self.image_size = image_size

        self.model = None

        self.class_names = [

            "glioma",

            "meningioma",

            "notumor",

            "pituitary"

        ]

        self.load_model()

    ###########################################################

    def load_model(self):

        self.model = keras.models.load_model(

            self.model_path

        )

        print("=" * 50)
        print("Model Loaded Successfully")
        print("=" * 50)

    ###########################################################

    def load_image(

        self,

        image_path

    ):

        image = cv2.imread(str(image_path))

        if image is None:

            raise FileNotFoundError(

                f"Cannot load image : {image_path}"

            )

        original = image.copy()

        image = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

        image = cv2.resize(

            image,

            self.image_size

        )

        image = image.astype(np.float32)

        image = np.expand_dims(

            image,

            axis=0

        )

        return original, image

    ###########################################################

    def predict(self, image):

        predictions = self.model.predict(
            image,
            verbose=0
        )[0]

        class_index = int(np.argmax(predictions))
        confidence = float(predictions[class_index])
        class_name = self.class_names[class_index]

        probabilities = {
            self.class_names[i]: float(predictions[i])
            for i in range(len(self.class_names))
        }

        return {
            "class_index": class_index,
            "prediction": class_name,
            "confidence": confidence,
            "probabilities": probabilities
        }

    ###########################################################

    def predict_image(

        self,

        image_path

    ):

        original, image = self.load_image(

            image_path

        )

        result = self.predict(

            image

        )

        result["original"] = original

        result["input_tensor"] = image

        return result

    ###########################################################

    def predict_batch(

        self,

        image_paths

    ):

        results = []

        for image_path in image_paths:

            result = self.predict_image(

                image_path

            )

            results.append(

                result

            )

        return results

    ###########################################################

    def print_prediction(

        self,

        result

    ):

        print("=" * 60)

        print(

            f"Prediction : {result['class_name']}"

        )

        print(

            f"Confidence : {result['confidence']:.2%}"

        )

        print()

        print("Class Probabilities")

        print("-" * 60)

        for label, score in result["probabilities"].items():

            print(

                f"{label:<15}: {score:.2%}"

            )

        print("=" * 60)

    ###########################################################

    def run(

        self,

        image_path

    ):

        result = self.predict_image(

            image_path

        )

        self.print_prediction(

            result

        )

        return result