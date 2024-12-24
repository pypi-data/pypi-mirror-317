import optuna
from npeccv6.model_func import create_model
from npeccv6.preprocessing import preprocess_train
from npeccv6.train import load_and_preprocess_data
import datetime
import mlflow
from keras.callbacks import TensorBoard
from npeccv6.utils import setup_logger
import numpy as np
import argparse
import os

logger = setup_logger(debug=True)


def main():
    parser = argparse.ArgumentParser(
        description="Perform hyperparameter sweep."
    )
    parser.add_argument(
        "--n_trials",
        type=int,
        default=5,
        help="How many trials to perform"
    )
    parser.add_argument(
        "--data_folder",
        type=str,
        default='../models/test/patched_data',
        help="Path to location with preprocessed data"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=1,
        help="How many epochs to run each trial"
    )
    parser.add_argument(
        "--results_path",
        type=str,
        default="../models/hyperparameter_sweeps",
        help="Path the hyperparameter sweep results will be saved in"
    )

    args = parser.parse_args()

    n_trials = args.n_trials
    preprocessed_data_folder = args.data_folder
    epochs = args.epochs
    results_path = args.results_path
    
    hyperparametertuning_main(
        n_trials = n_trials,
        preprocessed_data_folder = preprocessed_data_folder,
        epochs = epochs,
        results_path = results_path,
    )

# Define the objective function for the hyperparameter sweep
def objective(trial: optuna.Trial,
              preprocessed_data_folder: str,
              epochs: int,
) -> float:
    """
    Authorship: Hubert Waleńczak
    Objective function for the hyperparameter optimization process. This function 
    trains a model using the hyperparameters suggested by the Optuna trial and 
    logs the results to MLflow.

    Parameters:
        - trial (optuna.Trial): The current trial from Optuna containing suggested hyperparameters.
        - preprocessed_data_folder (str): Path to the folder containing preprocessed training and validation data.
        - epochs (int): Number of epochs to train the model.

    Returns:
        - float: The validation IoU (Intersection over Union) score for the model, which is the optimization metric.
    """
    # Define hyperparameters to be optimized
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-5, 1e-1)

    # Load preprocessed data
    # User needs to prepare preprocessed data
    train_generator, val_generator, steps_per_epoch, validation_steps = load_and_preprocess_data(patch_dir=preprocessed_data_folder)

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #steps_per_epoch=3 #TO-DO: remove before prod
    #validation_steps=3 #TO-DO: remove before prod
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    
    Now = datetime.datetime.now()
    time = Now.strftime("%Y.%m.%d-%H.%M")
    model_name=f"sweep_{time}"
    # Start MLflow tracking
    mlflow.start_run()
    # mlflow.tensorflow.autolog()

    # TensorBoard callback
    log_dir = f"./logs/tensorboard/{time}"
    if not os.path.exists(log_dir):
        logger.info(f"Creating folder at {log_dir}")
        os.makedirs(log_dir)
    
    tb = TensorBoard(log_dir=log_dir, histogram_freq=1)
    # Log TensorBoard directory
    logger.info(
        f'Tensorboard of {model_name} at location {f"./logs/tensorboard/{time}"}'
    )
    
    # Create the model
    model = create_model(
        model_name=model_name,  # Use an actual model name
        patch_size=256,  # Adjust input shape based on data #TO-DO: get patch_size from loaded generator
        learning_rate=learning_rate,
        output_activation="sigmoid",  # Adjust based on your problem
    )
    
    # Train the model
    hist = model.fit(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=validation_steps,
        callbacks=[tb],
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
        }
    )

    # End the MLflow run
    mlflow.end_run()
    
    # Return validation accuracy as the optimization metric
    val_iou = hist.history["val_iou"][-1]
    return val_iou

def hyperparametertuning_main(
        n_trials: int = 5,
        preprocessed_data_folder: str = '../models/test/patched_data',
        epochs: int = 1,
        results_path: str = "../models/hyperparameter_sweeps",
    ) -> None:
    """
    Main function that performs the hyperparameter optimization using Optuna. 
    It creates an Optuna study, runs multiple trials, and saves the results.

    Args:
        - n_trials (int): The number of trials to run in the hyperparameter optimization process.
        - preprocessed_data_folder (str): Path to the folder containing preprocessed training and validation data.
        - epochs (int): Number of epochs to run each trial.
        - results_path (str): Path where the results of the hyperparameter sweep will be saved.

    Returns:
        None
    """

    Now = datetime.datetime.now()
    time = Now.strftime("%Y.%m.%d-%H.%M")

    # Create a study to optimize the hyperparameters
    study = optuna.create_study(direction="maximize")
    study.optimize(lambda trial: objective(trial, preprocessed_data_folder, epochs), n_trials=n_trials)
    
    # Print the best trial and hyperparameters
    best_trial = study.best_trial
    print(f"Best trial: {best_trial}")
    print(f"Best parameters: {best_trial.params}")
    
    #TO-DO: return best parameters
    #TO-DO: save hyperparameter sweep results somewhere logical
    # Optionally save the results to a CSV file
    if not os.path.exists(results_path):
        logger.info(f"Creating folder at {results_path}")
        os.makedirs(results_path)
    study.trials_dataframe().to_csv(f"{results_path}/hyperparameter_sweep_{time}_results_.csv")

if __name__=="__main__":
    main()
    #logger.Warning("Remove line 94 and 95 before release. Limit's number of steps for quicker developement")