"""
Configuration settings for the Heart Disease Prediction API
"""
import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# Data paths
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATASET_FILE = PROCESSED_DATA_DIR / "heart_disease.csv"

# Model paths
MODEL_FILE = MODELS_DIR / "best_model.pkl"
PREPROCESSOR_FILE = MODELS_DIR / "preprocessor.pkl"

# MLflow settings
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "./mlruns")
MLFLOW_EXPERIMENT_NAME = "heart_disease_prediction"

# API settings
API_TITLE = "Heart Disease Prediction API"
API_VERSION = "1.0.0"
API_DESCRIPTION = "API for predicting heart disease risk using machine learning"
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Model settings
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5

# Feature names
FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

TARGET_NAME = 'target'

# Logging settings
LOG_FILE = LOGS_DIR / "api_logs.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, LOGS_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
