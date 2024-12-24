import argparse
import datetime
from typing import List, Tuple

import mlflow
import numpy as np
import json
from keras.callbacks import EarlyStopping, History, TensorBoard
from keras.preprocessing.image import ImageDataGenerator

from npeccv6.model_func import load_pretrained_model
from npeccv6.preprocessing import preprocess_train
from npeccv6.utils import read_config, setup_logger

logger = setup_logger(debug=True)


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess images and masks into patches."
    )
    parser.add_argument(
        "--model_name",
        type=str,
        default="default",
        help="Model to be trained.",
    )
    parser.add_argument(
        "--models_folder",
        type=str,
        default="./models",
        help="Path to the root of models folder.",
    )
    parser.add_argument(
        "--folder",
        type=str,
        default='',
        help="Path to raw data. Leave empty if using model default raw data location (models/modelname/data)."
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=20,
        help="How many epochs to train the model.",
    )
    parser.add_argument(
        "--patience",
        type=int,
        default=3,
        help="How many epochs to train model without improvement.",
    )
    parser.add_argument(
        "--mask_class",
        type=str,
        default='root',
        help="What mask to train. Default is 'root'.",
    )
    parser.add_argument(
        "--clear_dest",
        type=bool,
        default=False,
        help="Clear destination folder for preprocessed images before preprocessing"
    )
    #parser.add_argument(
    #    "--model_save_path",
    #    type=str,
    #    default=None,
    #    help="Path to save new model if it has better performance. Will save in same location if not specified"
    #)
    #parser.add_argument(
    #    "--hyperparamers"
    #)

    args = parser.parse_args()

    if args.folder == '':
        folder = f'{args.models_folder}/{args.model_name}/data'
    else:
        folder = args.folder

    train_main(
        model_name = args.model_name,
        models_folder = args.models_folder,
        folder = folder,
        epochs = args.epochs,
        patience = args.patience,
        mask_class = args.mask_class,
        clear_dest = args.clear_dest,
        #model_save_path = args.model_save_path
    )
    

def load_and_preprocess_data(
    mask_class: str = "root",
    patch_size: int = 256,
    patch_dir: str = "./data_patched/",
    seed: int = 42,
    batch_size: int = 16,
) -> Tuple[zip, zip, int, int]:
    """
    Authorship: Hubert Waleńczak

    Load and preprocess image and mask data for training and testing.

    Parameters:
        - mask_class (str): class name of mask that will be predicted.
        - patch_size (int): Size of the patches the model is created for.
        - patch_dir (str): Directory containing images and masks patches.
        - seed (int, optional): Seed for data generators.
        - batch_size (int): Batch size for the generators.

    Returns:
        Tuple[zip, zip, int, int]: A tuple containing:
            - train_generator: Training data generator (image and mask).
            - val_generator: Testing data generator (image and mask).
            - steps_per_epoch: Number of steps to be taken per epoch.
            - validation_steps: Number of steps to be taken for validation.

    Notes:
        - The function uses ImageDataGenerator to create data generators for image and mask patches.
        - Training and testing data generators are created for both images and masks.
    """

    logger.info("Initializing data generators for training and testing.")

    logger.info("Creating ImageDataGenerator for training images.")

    train_image_datagen = ImageDataGenerator(rescale=1.0 / 255)

    logger.debug(f"load_and_preprocess_data - train image generator - {patch_dir}")
    train_image_generator = train_image_datagen.flow_from_directory(
        f"{patch_dir}/train",
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        classes=["images"],
        class_mode=None,
        color_mode="grayscale",
        seed=seed,
        shuffle=False,
    )

    logger.info("Creating ImageDataGenerator for training masks.")
    train_mask_datagen = ImageDataGenerator()
    logger.debug(f"load_and_preprocess_data - train mask generator - {patch_dir}")
    train_mask_generator = train_mask_datagen.flow_from_directory(
        f"{patch_dir}/train",
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        classes=[mask_class],
        class_mode=None,
        color_mode="grayscale",
        seed=seed,
        shuffle=False,
    )

    # Create train generator
    train_generator = zip(train_image_generator, train_mask_generator)

    logger.info("Creating ImageDataGenerator for testing images.")
    val_image_datagen = ImageDataGenerator(rescale=1.0 / 255)

    logger.debug(f"load_and_preprocess_data - test image generator - {patch_dir}")
    val_image_generator = val_image_datagen.flow_from_directory(
        f"{patch_dir}/test",
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        classes=["images"],
        class_mode=None,
        color_mode="grayscale",
        seed=seed,
        shuffle=False,
    )

    logger.debug("Creating ImageDataGenerator for testing masks.")
    val_mask_datagen = ImageDataGenerator()

    logger.debug(f"load_and_preprocess_data - test mask generator - {patch_dir}")
    val_mask_generator = val_mask_datagen.flow_from_directory(
        f"{patch_dir}/test",
        target_size=(patch_size, patch_size),
        batch_size=batch_size,
        classes=[mask_class],
        class_mode=None,
        color_mode="grayscale",
        seed=seed,
        shuffle=False
    )

    # Create validation generator
    val_generator = zip(val_image_generator, val_mask_generator)

    # Calculate train and validation steps
    steps_per_epoch = len(train_image_generator)
    validation_steps = val_image_generator.samples // batch_size

    logger.info(
        f"Data generators created successfully. Steps per epoch: {steps_per_epoch}, Validation steps: {validation_steps}."
    )

    return train_generator, val_generator, steps_per_epoch, validation_steps


def train_model(
    model_name: str,
    train_generator: zip,
    val_generator: zip,
    steps_per_epoch: int,
    validation_steps: int,
    epochs: int = 20,
    patience: int = 5,
    model=None,
) -> History:
    """
    Author: Hubert Waleńczak, Stinga Cristian

    Trains a convolutional neural network (CNN) model using the specified architecture and hyperparameters,
    with early stopping and TensorBoard logging. Logs metrics and parameters to MLflow.

    Parameters:
        - model_name (str): Name of model selected by user. This is used to retrieve the model parameters.
        - train_generator: Training data generator.
        - val_generator: Validation data generator.
        - steps_per_epoch (int): Number of steps to be taken per epoch.
        - validation_steps (int): Number of steps to be taken for validation.
        - epochs (int, optional): Number of training epochs.
        - patience (int, optional): Number of epochs the the training loop will wait to see if the val_loss improves.
        - model (keras.models.Model): A Keras model instance to be trained.

    Returns:
        - keras.callbacks.History: A History object containing the training process results (e.g., loss, accuracy, etc.).

    Notes:
        - Training is performed using the provided data generators and hyperparameters.
        - Early stopping and model checkpoint callbacks are applied during training.
        - TensorBoard callback is used for monitoring training progress.
        - Training metrics and model parameters are logged to MLflow for tracking.
        - This function assumes that `train_generator` and `val_generator` yield batches of data in the required format.
    """
    # Format the current time
    Now = datetime.datetime.now()
    time = Now.strftime("%Y.%m.%d-%H.%M")

    # Start MLflow tracking
    mlflow.start_run()
    # mlflow.tensorflow.autolog()

    # TensorBoard callback
    tb = TensorBoard(log_dir=rf".\logs\tensorboard\{time}", histogram_freq=1)
    # Log TensorBoard directory
    logger.info(
        f'Tensorboard of {model_name} at location {f"./logs/tensorboard/{time}"}'
    )
    # Early stopping callback
    early_stop = EarlyStopping(
        monitor="val_iou", patience=patience, restore_best_weights="True", mode="max"
    )

    # Train the model
    hist = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=validation_steps,
        callbacks=[early_stop, tb],
    )

    # Get the number of completed epochs
    completed_epochs = len(hist.history["loss"])

    # Log the model metrics to MLflow
    for epoch in range(completed_epochs):
        mlflow.log_metrics(
            {
                "train_loss": np.array(hist.history["loss"])[epoch],
                "train_accuracy": np.array(hist.history["accuracy"])[epoch],
                "train_f1": np.array(hist.history["f1"])[epoch],
                "train_iou": np.array(hist.history["iou"])[epoch],
                "val_loss": np.array(hist.history["val_loss"])[epoch],
                "val_accuracy": np.array(hist.history["val_accuracy"])[epoch],
                "val_f1": np.array(hist.history["val_f1"])[epoch],
                "val_iou": np.array(hist.history["val_iou"])[epoch],
            },
            step=epoch,
        )

    # Log the model metrics to MLflow at the end of the training
    mlflow.log_metric("train_loss", hist.history["loss"][-1])
    mlflow.log_metric("train_accuracy", hist.history["accuracy"][-1])
    mlflow.log_metric("train_f1", hist.history["f1"][-1])
    mlflow.log_metric("train_iou", hist.history["iou"][-1])
    mlflow.log_metric("val_loss", hist.history["val_loss"][-1])
    mlflow.log_metric("val_accuracy", hist.history["val_accuracy"][-1])
    mlflow.log_metric("val_f1", hist.history["val_f1"][-1])
    mlflow.log_metric("val_iou", hist.history["val_iou"][-1])

    # Log model's parameters
    mlflow.log_params(
        {
            "epochs": epochs,
            "steps_per_epoch": steps_per_epoch,
            "validation_steps": validation_steps,
            "patience": patience,
        }
    )

    # End the MLflow run
    mlflow.end_run()

    # Log the model history
    logger.info(f"train_model - {hist.history.keys() = }")
    return hist


def train_main(
    model_name: str,
    models_folder: str,
    folder: str,  # not preprocessed data
    epochs: int,
    patience: int,
    mask_class: str,
    clear_dest: bool,
    #model_save_path:str # may need for azure
):
    #if model_save_path == '' or model_save_path == None:
    #    model_save_path = f"{models_folder}/{model_name}/{model_name}.keras" # may need for azure
    model_save_path = f"{models_folder}/{model_name}/{model_name}.keras"
    
    # get model config
    config = read_config(model_name, models_folder)

    # preprocess data to model folder (preprocess_train function)
    preprocess_train(
        images_folder=folder,
        patch_size=config['patch_size'],
        scaling_factor=1,
        save_folder=f"{models_folder}/{model_name}/patched_data",
        clear_dest=clear_dest
    )
    
    # load data from model folder
    train_generator, val_generator, steps_per_epoch, validation_steps = (
        load_and_preprocess_data(
            mask_class=mask_class,
            patch_size=config['patch_size'],
            patch_dir=f"{models_folder}/{model_name}/patched_data",
            seed=42,
            batch_size=16,
        )
    )
    
    # get model from model folder
    model = load_pretrained_model(
        model_name=model_name, models_path=f"{models_folder}/{model_name}"
    )
    
    # train model
    hist = train_model(
        model_name=model_name,
        train_generator=train_generator,
        val_generator=val_generator,
        steps_per_epoch=steps_per_epoch,
        validation_steps=validation_steps,
        epochs=epochs,
        patience=patience,
        model=model,
    )
    
    # Save model to model folder
    #model_save_path = f"{models_folder}/{model_name}/{model_name}.keras" # save as new
    #model.save(model_save_path)

    # Compare performance with old
    # Load the previous model
    old_model = load_pretrained_model(
        model_name=model_name, models_path=f"{models_folder}/{model_name}"
    )
    
    # Evaluate the old model on the validation data
    new_model_perf = model.evaluate(val_generator, steps=validation_steps, verbose=0)[3]
    old_model_perf = old_model.evaluate(val_generator, steps=validation_steps, verbose=0)[3]

    # Compare the performance
    if new_model_perf > old_model_perf:
        # New model is better, save it and replace the old model
        model.save(model_save_path)
        # Save history for registracion on Azure
        with open(f'{models_folder}/{model_name}/model_train_history.json', 'w') as json_file:
            json.dump(hist.history, json_file)
        logger.info(f"New model saved. Replaced the old model with better performance (new val_iou: {new_model_perf}, old val_iou: {old_model_perf}).")
    else:
        # Old model is better, revert new model and discard it
        logger.info(f"Old model retained as it performs better (new val_iou: {new_model_perf}, old val_iou: {old_model_perf}).")

    return hist


if __name__ == "__main__":
    main()
