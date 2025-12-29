"""
Data preprocessing module for heart disease prediction
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HeartDiseasePreprocessor:
    """
    Preprocessor for heart disease dataset
    Handles missing values, scaling, and feature encoding
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = None
        self.is_fitted = False
        
    def load_data(self, filepath):
        """Load data from CSV file"""
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        return df
    
    def handle_missing_values(self, X):
        """Handle missing values using median imputation"""
        if not self.is_fitted:
            X_imputed = self.imputer.fit_transform(X)
        else:
            X_imputed = self.imputer.transform(X)
        return pd.DataFrame(X_imputed, columns=X.columns, index=X.index)
    
    def scale_features(self, X):
        """Scale features using StandardScaler"""
        if not self.is_fitted:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    def fit_transform(self, X, y=None):
        """Fit and transform the data"""
        logger.info("Fitting preprocessor and transforming data...")
        self.feature_names = X.columns.tolist()
        
        # Handle missing values
        X_imputed = self.handle_missing_values(X)
        
        # Scale features
        X_scaled = self.scale_features(X_imputed)
        
        self.is_fitted = True
        logger.info("Preprocessing complete!")
        return X_scaled
    
    def transform(self, X):
        """Transform new data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Ensure columns match
        if self.feature_names is not None:
            X = X[self.feature_names]
        
        # Handle missing values
        X_imputed = self.handle_missing_values(X)
        
        # Scale features
        X_scaled = self.scale_features(X_imputed)
        
        return X_scaled
    
    def save(self, filepath):
        """Save preprocessor to file"""
        joblib.dump(self, filepath)
        logger.info(f"Preprocessor saved to {filepath}")
    
    @staticmethod
    def load(filepath):
        """Load preprocessor from file"""
        preprocessor = joblib.load(filepath)
        logger.info(f"Preprocessor loaded from {filepath}")
        return preprocessor


def prepare_data(data_path, test_size=0.2, random_state=42):
    """
    Prepare data for training
    
    Parameters:
    -----------
    data_path : str or Path
        Path to the CSV file
    test_size : float
        Proportion of data for testing
    random_state : int
        Random seed for reproducibility
    
    Returns:
    --------
    X_train, X_test, y_train, y_test, preprocessor
    """
    # Load data
    preprocessor = HeartDiseasePreprocessor()
    df = preprocessor.load_data(data_path)
    
    # Separate features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    logger.info(f"Train set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    logger.info(f"Class distribution in training: {y_train.value_counts().to_dict()}")
    
    # Fit and transform training data
    X_train_processed = preprocessor.fit_transform(X_train)
    
    # Transform test data
    X_test_processed = preprocessor.transform(X_test)
    
    return X_train_processed, X_test_processed, y_train, y_test, preprocessor


if __name__ == "__main__":
    # Test preprocessing
    from pathlib import Path
    
    BASE_DIR = Path(__file__).parent.parent
    DATA_PATH = BASE_DIR / "data" / "processed" / "heart_disease.csv"
    
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(DATA_PATH)
    
    print("\n" + "="*80)
    print("PREPROCESSING TEST")
    print("="*80)
    print(f"\nTrain shape: {X_train.shape}")
    print(f"Test shape: {X_test.shape}")
    print(f"\nFirst few rows of processed training data:")
    print(X_train.head())
    print("\n" + "="*80)
