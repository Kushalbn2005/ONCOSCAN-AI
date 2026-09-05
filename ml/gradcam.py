from pathlib import Path
import uuid

import cv2
import numpy as np
import tensorflow as tf

from tensorflow import keras


from ml.predict import Predictor

class GradCAM:
    """
    Grad-CAM for Brain Tumor Classification
    """

    def __init__(self, predictor: Predictor, output_dir=None):

        self.predictor = predictor

        self.model = predictor.model

        self.class_names = predictor.class_names

        self.image_size = predictor.image_size

        self.output_dir = Path(output_dir) if output_dir else Path("artifacts/gradcam")

        self._grad_model = None
        self._last_conv_name = None

        self.create_directories()

    ###########################################################

    def create_directories(self):

        self.output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

    ###########################################################

    

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

    def _get_backbone(self):
        for layer in self.model.layers:
            if isinstance(layer, keras.Model):
                return layer
        raise ValueError("No backbone model found inside classifier.")

    ###########################################################

    def build_gradcam_model(self, last_conv_layer_name):
        backbone = self._get_backbone()
        conv_layer = backbone.get_layer(last_conv_layer_name)

        grad_model = keras.models.Model(
            inputs=backbone.input,
            outputs=[
                conv_layer.output,
                backbone.output
            ]
        )

        return grad_model

    def get_cached_grad_model(self):
        """Build the Grad-CAM model once and reuse it across requests."""
        if self._grad_model is None:
            self._last_conv_name = self.get_last_conv_layer()
            self._grad_model = self.build_gradcam_model(self._last_conv_name)
        return self._grad_model
    

    ###########################################################

    def make_heatmap(
        self,
        image,
        class_index,
        last_conv_layer_name=None
    ):
        """
        Generate Grad-CAM heatmap.
        """

        grad_model = self.get_cached_grad_model()

        with tf.GradientTape() as tape:
            conv_outputs, x = grad_model(image)

            for layer in self.model.layers[2:]:
                x = layer(x, training=False)

            predictions = x
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

    ###########################################################

    def overlay_heatmap(
        self,
        original_image,
        heatmap,
        alpha=0.4,
        colormap=cv2.COLORMAP_JET
    ):
        """
        Resize heatmap to original image dimensions and blend with the MRI.
        Returns the BGR overlay image.
        """

        h, w = original_image.shape[:2]

        heatmap_uint8 = np.uint8(255 * heatmap)

        heatmap_resized = cv2.resize(heatmap_uint8, (w, h))

        heatmap_colored = cv2.applyColorMap(heatmap_resized, colormap)

        overlay = cv2.addWeighted(
            original_image, 1 - alpha,
            heatmap_colored, alpha,
            0
        )

        return overlay

    ###########################################################

    def save_visualization(
        self,
        original_image,
        overlay,
        heatmap,
        class_name,
        confidence,
        output_path
    ):
        """
        Save a three-panel image: original | heatmap | overlay.
        """

        h, w = original_image.shape[:2]

        heatmap_uint8 = np.uint8(255 * heatmap)
        heatmap_resized = cv2.resize(heatmap_uint8, (w, h))
        heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)

        panel = np.concatenate(
            [original_image, heatmap_colored, overlay],
            axis=1
        )

        label = f"{class_name} ({confidence:.2%})"
        cv2.putText(
            panel, label,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.imwrite(str(output_path), panel)

        print(f"Saved : {output_path}")

    ###########################################################

    def run(self, image_path, output_name=None):
        """
        Full pipeline: load → predict → heatmap → overlay → save.
        """

        image_path = Path(image_path)

        if output_name is None:
            output_name = f"gradcam_{image_path.stem}.jpg"

        output_path = self.output_dir / output_name

        original, input_tensor = self.load_image(image_path)

        class_index, class_name, confidence = self.predict(input_tensor)

        heatmap = self.make_heatmap(input_tensor, class_index)

        overlay = self.overlay_heatmap(original, heatmap)

        self.save_visualization(
            original,
            overlay,
            heatmap,
            class_name,
            confidence,
            output_path
        )

        return {
            "class_name": class_name,
            "confidence": confidence,
            "heatmap": heatmap,
            "overlay": overlay,
            "output_path": str(output_path)
        }
    
    def generate(self, image_path, class_index=None):
        """
        Generate Grad-CAM heatmap, save overlay image, and return filename.
        """
        image_path = Path(image_path)
        original, input_tensor = self.load_image(image_path)

        if class_index is None:
            class_index, _, _ = self.predict(input_tensor)

        heatmap = self.make_heatmap(input_tensor, class_index)
        overlay = self.overlay_heatmap(original, heatmap)

        filename = f"gradcam_{uuid.uuid4().hex[:10]}.png"
        output_path = self.output_dir / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(str(output_path), overlay)

        return filename
