import os
import shutil
import cv2
import base64
from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from npeccv6.preprocessing import preprocess_train
from npeccv6.model_func import load_pretrained_model
from npeccv6.create_model import create_model_main as create_model
from npeccv6.train import train_model, load_and_preprocess_data
from npeccv6.predict import predict_main as predict
from npeccv6.train import train_main as train
from npeccv6.utils import create_config_json, read_config, setup_logger


app = FastAPI()
logger = setup_logger()

# Move your existing prediction code here
# Ensure that `load_pretrained_model`, `predict`, and all other required functions are imported


class PredictionResult(BaseModel):
    success: bool
    image_data: Optional[str] = None  # Base64-encoded string of the predicted image
    mean_conf_score: float
    root_tip_coords: List[Tuple[int,int]]
    

class TrainResult(BaseModel):
    success: bool
    #hist: List[Dict[str, float]]


class ModelParams(BaseModel):
    success: bool
    model_name: str
    patch_size: int
    #output_classes: int
    #optimizer: str
    #loss: str
    output_activation: str
    learning_rate: float
    summary: bool
    models_folder: str
    class Config:
        # Disable the protected namespace check
        protected_namespaces = ()
        
class UploadResult(BaseModel):
    message: str
    file_paths: List[str]

# DONE
@app.post("/predict", response_model=List[PredictionResult])
async def predict_image_endpoint(
    model_name: str = "test",
    models_folder: str = "../models",
    save_path: str = "../saves",
    threshold: float = 0.8,
    user_folder: str = "../user_data/anonymous",
    files: List[UploadFile] = File(...),
) -> List[PredictionResult]:
    results = []
    try:
        print(model_name)
        print(models_folder)
        print(save_path)
        print(threshold)
        print(user_folder)
        print(files)
        for ifile in files:
            # Make sure folders exist
            print(ifile)
            os.makedirs(os.path.dirname(user_folder + "/images/"), exist_ok=True)
            os.makedirs(os.path.dirname(user_folder + "/masks/"), exist_ok=True)
            print("-----")
            # Save the uploaded file locally
            image_file_path = os.path.join(user_folder + "/images/", ifile.filename)
            print("path: " + image_file_path)
            with open(image_file_path, "wb") as f:
                f.write(await ifile.read())

            image = cv2.imread(image_file_path, cv2.IMREAD_GRAYSCALE)
            print("Predicting")
            success, marked_image_filename, mean_conf_score, root_tip_coords = predict(
                image = image,
                model_name = model_name,
                models_path = models_folder,
                save_path = save_path,
                threshold = threshold,
            )
            print("Predicted")
            
            # If prediction was successful, convert predicted image to base64
            if success==0:
                success = True
                predicted_image_path = f"{models_folder}/{model_name}/hist/{marked_image_filename}"  # Assuming `predict` saves output
                with open(predicted_image_path, "rb") as img_file:
                    image_data = base64.b64encode(img_file.read()).decode("utf-8")
            else:
                success = False
                image_data = None

            # Append result with success flag and encoded image data
            results.append(PredictionResult(success=success, image_data=image_data, mean_conf_score=mean_conf_score, root_tip_coords=root_tip_coords))

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

# DONE
@app.post("/create_model")
async def create_model_endpoint(
    model_name: str = "test",
    patch_size: int = 256,
    #output_classes: int = 1,
    #optimizer: str = "adam",
    #loss: str = "binary_crossentropy",
    output_activation: str = "sigmoid",
    learning_rate: float = 0.001,
    summary: bool = False,
    models_folder: str = "../models",
) -> ModelParams:
    try:
        success = create_model(
            model_name,
            patch_size,
            #output_classes,
            #optimizer,
            #loss,
            output_activation,
            learning_rate,
            summary,
            models_folder,
        )
        if success == 0:
            return ModelParams(
                success=True,
                model_name=model_name,
                patch_size=patch_size,
                #output_classes=output_classes,
                #optimizer=optimizer,
                #loss=loss,
                output_activation=output_activation,
                learning_rate=learning_rate,
                summary=summary,
                models_folder=models_folder,
            )
        else:
            return ModelParams(
                success=False,
                model_name=model_name,
                patch_size=patch_size,
                #output_classes=output_classes,
                #optimizer=optimizer,
                #loss=loss,
                output_activation=output_activation,
                learning_rate=learning_rate,
                summary=summary,
                models_folder=models_folder,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# DONE
@app.post("/train")
async def train_model_endpoint(
    model_name: str = "test",
    models_folder: str = "../models",
    folder: str = "",
    epochs: int = 20,
    patience: int = 10,
    mask_class: str = "root",
    clear_dest: bool = 0,
) -> TrainResult:
    try:
        if folder == '':
            folder = f'{models_folder}/{model_name}/data'

        hist = train(
            model_name = model_name,
            models_folder = models_folder,
            folder = folder,
            epochs = epochs,
            patience = patience,
            mask_class = mask_class,
            clear_dest = clear_dest,
        )

        return TrainResult(success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {e}")
        
@app.post("/upload/train_images")
async def upload_train_images(
    model_name: str = "test",
    models_folder: str = "../models",
    files: List[UploadFile] = File(...)
) -> UploadResult:
    saved_files = []
    try:
        for file in files:
            # Create a path to save the file
            file_path = os.path.join(f'{models_folder}/{model_name}/data/train/', file.filename)
        
            # Save the file to the disk
            with open(file_path, "wb") as f:
                f.write(await file.read())
        
            # Append the file path to the list of saved files
            saved_files.append(file_path)
    
        return UploadResult(message="Files uploaded successfully", file_paths=saved_files)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {e}")

@app.post("/upload/test_images")
async def upload_train_images(
    model_name: str = "test",
    models_folder: str = "../models",
    files: List[UploadFile] = File(...)
) -> UploadResult:
    saved_files = []
    try:
        for file in files:
            # Create a path to save the file
            file_path = os.path.join(f'{models_folder}/{model_name}/data/test/', file.filename)
        
            # Save the file to the disk
            with open(file_path, "wb") as f:
                f.write(await file.read())
        
            # Append the file path to the list of saved files
            saved_files.append(file_path)
    
        return UploadResult(message="Files uploaded successfully", file_paths=saved_files)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {e}")


@app.post("/upload/masks")
async def upload_train_images(
    model_name: str = "test",
    models_folder: str = "../models",
    files: List[UploadFile] = File(...)
) -> UploadResult:
    saved_files = []
    try:
        for file in files:
            # Create a path to save the file
            file_path = os.path.join(f'{models_folder}/{model_name}/data/masks/', file.filename)
        
            # Save the file to the disk
            with open(file_path, "wb") as f:
                f.write(await file.read())
        
            # Append the file path to the list of saved files
            saved_files.append(file_path)
    
        return UploadResult(message="Files uploaded successfully", file_paths=saved_files)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {e}")

