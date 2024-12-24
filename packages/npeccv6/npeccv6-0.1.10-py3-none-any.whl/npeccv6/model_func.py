
import os
from typing import Tuple

import keras
from tensorflow.keras.layers import (Conv2D, Conv2DTranspose, Dropout, Input,
                                     MaxPooling2D, concatenate)
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam

from npeccv6.utils import f1, iou, setup_logger

logger = setup_logger(debug=True)


def create_model(
    model_name: str,
    patch_size: int = 256,
    #output_classes: int = 1,
    #optimizer: str = "adam",
    #loss: str = "binary_crossentropy",
    # TO-DO: hyperparameters (e.g. adam(learning_rate)), change "adam" to accept optimizer function
    output_activation: str = "sigmoid",
    summary: bool = False,
    learning_rate: float = 0.001,
) -> keras.models.Model:
    """
    Author: Stinga Cristian, Hubert Waleńczak

    Create a U-Net model for semantic segmentation.

    Parameters:
        - model_name (str): Name of the model you want to create.
        - patch_size (int): Size of the patches that are the results of cutting image into smaller imges model is able to predict. Bigger patch size will produce better resoults but is more computionaly intensive, for most cases 256 is big enough. Default is '256'.
        - output_activation (str): Activation function for the output layer. Default is 'sigmoid'.
        - summary (bool): Whether to print the model summary. Default is False.
        - learning_rate (int): Learining rate of the model.

    Returns:
        - keras.models.Model: U-Net model for semantic segmentation.
    """
    optimizer = Adam(learning_rate=learning_rate)
    
    # Build the model
    inputs = Input((patch_size, patch_size, 1))
    s = inputs

    # Log input shape
    logger.debug(f"Input shape: {patch_size}")

    # Contraction path
    c1 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(s)
    c1 = Dropout(0.1)(c1)
    c1 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    c2 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p1)
    c2 = Dropout(0.1)(c2)
    c2 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c2)
    p2 = MaxPooling2D((2, 2))(c2)

    c3 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p2)
    c3 = Dropout(0.2)(c3)
    c3 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c3)
    p3 = MaxPooling2D((2, 2))(c3)

    c4 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p3)
    c4 = Dropout(0.2)(c4)
    c4 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c4)
    p4 = MaxPooling2D(pool_size=(2, 2))(c4)

    c5 = Conv2D(
        256, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(p4)
    c5 = Dropout(0.3)(c5)
    c5 = Conv2D(
        256, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c5)

    # Expansive path
    u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding="same")(c5)
    u6 = concatenate([u6, c4])
    c6 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u6)
    c6 = Dropout(0.2)(c6)
    c6 = Conv2D(
        128, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c6)

    u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding="same")(c6)
    u7 = concatenate([u7, c3])
    c7 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u7)
    c7 = Dropout(0.2)(c7)
    c7 = Conv2D(
        64, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c7)

    u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding="same")(c7)
    u8 = concatenate([u8, c2])
    c8 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u8)
    c8 = Dropout(0.1)(c8)
    c8 = Conv2D(
        32, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c8)

    u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding="same")(c8)
    u9 = concatenate([u9, c1], axis=3)
    c9 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(u9)
    c9 = Dropout(0.1)(c9)
    c9 = Conv2D(
        16, (3, 3), activation="relu", kernel_initializer="he_normal", padding="same"
    )(c9)

    outputs = Conv2D(1, (1, 1), activation=output_activation)(c9)

    model = Model(inputs=[inputs], outputs=[outputs])

    # Compile the model
    model.compile(optimizer=optimizer, loss="binary_crossentropy", metrics=["accuracy", f1, iou])

    # Show model summary
    if summary:
        logger.info(model.summary())

    # Finish creating the model
    logger.info(f"Model {model_name} created.")
    return model


def load_pretrained_model(
    model_name: str, models_path: str = "./models"
) -> keras.models.Model:
    """
    Author: Stinga Cristian

    Load a saved and pre-trained U-Net model from the specified directory.

    Parameters:
        - model_name (str): The name of the model file to load. No default.
        - models_path (str): Path to models directory. Default is "./models"

    Returns:
        - keras.models.Model: The loaded U-Net model.

    Raises:
        - FileNotensorflowoundError: If the model file does not exist at the specified path.

    Notes:
        - The model file needs to be in the './models' directory.
    """

    # Construct the model path
    model_path = f"{models_path}/{model_name}.keras"

    # Check if the model file exists
    if not os.path.exists(model_path):
        logger.error(f"No model found at {models_path} with the name: {model_name}")
        raise FileNotFoundError(
            f"No model found at {models_path} with the name: {model_name}"
        )

    # Load the model
    model = load_model(model_path, custom_objects={"f1": f1, "iou": iou})

    # Log the model being loaded succesfully
    logger.info(f"Model loaded successfully from {model_path}")

    return model
