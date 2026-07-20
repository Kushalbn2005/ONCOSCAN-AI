from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf

from tensorflow import keras


class GradCAM:
    """
    Grad-CAM for Brain Tumor Classification

    Responsibilities
    ----------------
    • Load trained model
    • Load MRI image
    • Predict tumor class
    • Generate Grad-CAM heatmap
    • Overlay heatmap on MRI
    • Save visualization
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

        self.create_directories()

        self.load_model()

    ###########################################################

    def create_directories(self):

        Path("artifacts/gradcam").mkdir(

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

    def load_image(

        self,

        image_path

    ):
        """
        Returns

        original_image : Original BGR image

        input_tensor   : Tensor ready for prediction
        """

        image = cv2.imread(str(image_path))

        if image is None:

            raise FileNotFoundError(

                f"Cannot load image: {image_path}"

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

    def predict(

        self,

        image

    ):

        predictions = self.model.predict(

            image,

            verbose=0

        )

        class_index = np.argmax(

            predictions[0]

        )

        confidence = float(

            predictions[0][class_index]

        )

        class_name = self.class_names[

            class_index

        ]

        print("=" * 50)

        print(f"Prediction : {class_name}")

        print(f"Confidence : {confidence:.4f}")

        print("=" * 50)

        return (

            class_index,

            class_name,

            confidence

        )

    ###########################################################

    def get_last_conv_layer(self):
    # """
    # Automatically find the last Conv2D layer,
    # even inside nested models like EfficientNet.
    # """

    # Search top-level layers first
        for layer in reversed(self.model.layers):

            if isinstance(layer, keras.layers.Conv2D):
                print(f"Last Conv Layer: {layer.name}")
                return layer.name

            # Search inside nested Functional/Model layers
            if isinstance(layer, keras.Model):

                for inner_layer in reversed(layer.layers):

                    if isinstance(inner_layer, keras.layers.Conv2D):

                        print(f"Last Conv Layer: {inner_layer.name}")
                        return inner_layer.name

        raise ValueError("No Conv2D layer found.")
    
    ###########################################################

    def build_gradcam_model(self, last_conv_layer_name):

        grad_model = keras.models.Model(

            inputs=self.model.inputs,

            outputs=[
                self.model.get_layer(last_conv_layer_name).output,
                self.model.output
            ]

        )

        return grad_model
    

    ###########################################################

    def make_heatmap(
        self,
        image,
        class_index,
        last_conv_layer_name
    ):
        """
        Generate Grad-CAM heatmap.
        """

        grad_model = self.build_gradcam_model(
            last_conv_layer_name
        )

        with tf.GradientTape() as tape:

            conv_outputs, predictions = grad_model(image)

            loss = predictions[:, class_index]

        # Compute gradients
        gradients = tape.gradient(
            loss,
            conv_outputs
        )

        # Global Average Pooling over gradients
        pooled_gradients = tf.reduce_mean(
            gradients,
            axis=(0, 1, 2)
        )

        conv_outputs = conv_outputs[0]

        heatmap = tf.reduce_sum(
            conv_outputs * pooled_gradients,
            axis=-1
        )

        # Apply ReLU
        heatmap = tf.maximum(
            heatmap,
            0
        )

        # Normalize
        max_value = tf.reduce_max(heatmap)

        if max_value != 0:

            heatmap /= max_value

        heatmap = heatmap.numpy()

        return heatmap


