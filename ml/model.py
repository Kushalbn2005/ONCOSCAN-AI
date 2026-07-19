import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import regularizers


class BrainTumorClassifier:

    def __init__(
        self,
        input_shape=(224, 224, 3),
        num_classes=4,
        learning_rate=1e-4,
        fine_tune=False
    ):

        self.input_shape = input_shape
        self.num_classes = num_classes
        self.learning_rate = learning_rate
        self.fine_tune = fine_tune

    ###########################################################

    def build(self):

        base_model = keras.applications.EfficientNetB0(
        include_top=False,
        weights="imagenet",
        input_shape=self.input_shape,
        )

        self.base_model = base_model

        # Freeze pretrained weights initially
        base_model.trainable = self.fine_tune

        inputs = keras.Input(shape=self.input_shape)

        x = base_model(inputs, training=False)

        x = layers.GlobalAveragePooling2D()(x)

        x = layers.BatchNormalization()(x)

        x = layers.Dropout(0.30)(x)

        x = layers.Dense(
            256,
            activation="relu",
            kernel_regularizer=regularizers.l2(1e-5)
        )(x)

        x = layers.Dropout(0.20)(x)

        outputs = layers.Dense(
            self.num_classes,
            activation="softmax"
        )(x)

        model = keras.Model(
            inputs=inputs,
            outputs=outputs,
            name="BrainTumorClassifier"
        )

        optimizer = keras.optimizers.Adam(
            learning_rate=self.learning_rate
        )

        model.compile(

            optimizer=optimizer,

            loss="sparse_categorical_crossentropy",

            metrics=[
                "accuracy"
            ]

        )

        return model