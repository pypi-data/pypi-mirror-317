## Project Name: NPECCV6

This project is a comprehensive package for advanced data processing, predictive modeling, postprocessing of plant roots, and integration with Azure Machine Learning services. Below is an overview of the project structure and key details.
### Folder Structure

```bash
├── Azure_scripts/              # Scripts for interacting with Azure ML
├── dist/                       # Distributable Python packages
├── docs/                       # Documentation source and build files
├── tests/                      # Test cases for the project
├── Dockerfile                  # Docker container configuration
├── pyproject.toml              # Project configuration file
├── README.md                   # Project README file
└── npeccv6/                    # Main package folder
    ├── __init__.py                 # Package initialization
    ├── api.py                      # API functions for package operations
    ├── azure_scripts/              # Azure-specific scripts for pipeline
    ├── create_model.py             # Model creation logic
    ├── hyperparametetuning.py      # Hyperparameter tuning functionality
    ├── log/                        # Log files
    ├── mlruns/                     # MLflow experiment tracking files
    ├── model_func.py               # Core model-related functions
    ├── model_history.json          # Saved model history
    ├── postprocessing.py           # Postprocessing functions
    ├── predict.py                  # Prediction workflow
    ├── preprocessing.py            # Data preprocessing functionality
    ├── register.py                 # Model registration functions
    ├── scoring.py                  # Model scoring utilities
    ├── train.py                    # Model training logic
    ├── user_data/                  # User data for interacting with api
    └── utils.py                    # General utility functions
```

### Getting Started
#### Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_name>
```

2. Install the package using pip:

```bash
pip install dist/npeccv6-0.1.1-py3-none-any.whl
```

3. Install additional dependencies if required:
```bash
poetry install
```


### How to Use the CLI with Folder Structure
w

### Features

- Model Training and Scoring: Comprehensive scripts (train.py, scoring.py) for training and evaluating machine learning models.
- Data Preprocessing: Utilities for data cleaning, normalization, and augmentation (preprocessing.py).
- Azure ML Integration: Scripts to set up and interact with Azure ML resources (azure_scripts/).
- Logging: Centralized logging system for debugging and tracking (log/).
- Prediction and Postprocessing: Ready-to-use prediction pipeline (predict.py) and result enhancement tools (postprocessing.py).

### Documentation

Find the complete project documentation in the docs/ folder. Built documentation is available in the docs/build/html/ directory.

For API only documentation and interactions start fastapi
```bash
cd npeccv6
poetry run fastapi run api.py
```
and visit address shown in terminal. It sould begin with 127.0.0.1

### Contribution

1. Fork the repository and create your feature branch:

```bash
git checkout -b feature/new-feature
```

2. Commit your changes and push to the branch:
```bash
git commit -am 'Add new feature'
git push origin feature/new-feature
```
3. Create a pull request.


