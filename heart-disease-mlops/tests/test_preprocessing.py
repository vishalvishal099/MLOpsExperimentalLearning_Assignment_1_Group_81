"""
Unit tests for preprocessing module
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from preprocessing import HeartDiseasePreprocessor, prepare_data


@pytest.fixture
def sample_data():
    """Create sample heart disease data for testing"""
    data = {
        'age': [63, 67, 67, 37, 41],
        'sex': [1, 1, 1, 1, 0],
        'cp': [3, 4, 4, 3, 2],
        'trestbps': [145, 160, 120, 130, 130],
        'chol': [233, 286, 229, 250, 204],
        'fbs': [1, 0, 0, 0, 0],
        'restecg': [0, 2, 0, 0, 0],
        'thalach': [150, 108, 129, 187, 172],
        'exang': [0, 1, 1, 0, 0],
        'oldpeak': [2.3, 1.5, 2.6, 3.5, 1.4],
        'slope': [3, 2, 2, 3, 1],
        'ca': [0, 3, 2, 0, 0],
        'thal': [6, 3, 7, 3, 3],
        'target': [0, 1, 1, 0, 0]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_data_with_missing():
    """Create sample data with missing values"""
    data = {
        'age': [63, 67, np.nan, 37, 41],
        'sex': [1, 1, 1, 1, 0],
        'cp': [3, 4, 4, 3, 2],
        'trestbps': [145, np.nan, 120, 130, 130],
        'chol': [233, 286, 229, 250, 204],
        'fbs': [1, 0, 0, 0, 0],
        'restecg': [0, 2, 0, 0, 0],
        'thalach': [150, 108, 129, 187, 172],
        'exang': [0, 1, 1, 0, 0],
        'oldpeak': [2.3, 1.5, 2.6, 3.5, 1.4],
        'slope': [3, 2, 2, 3, 1],
        'ca': [0, np.nan, 2, 0, 0],
        'thal': [6, 3, 7, 3, 3],
        'target': [0, 1, 1, 0, 0]
    }
    return pd.DataFrame(data)


class TestHeartDiseasePreprocessor:
    """Test cases for HeartDiseasePreprocessor"""
    
    def test_initialization(self):
        """Test preprocessor initialization"""
        preprocessor = HeartDiseasePreprocessor()
        assert preprocessor.is_fitted == False
        assert preprocessor.feature_names is None
    
    def test_handle_missing_values(self, sample_data_with_missing):
        """Test missing value imputation"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data_with_missing.drop('target', axis=1)
        
        X_imputed = preprocessor.handle_missing_values(X)
        
        # Check no missing values remain
        assert X_imputed.isnull().sum().sum() == 0
        assert X_imputed.shape == X.shape
    
    def test_scale_features(self, sample_data):
        """Test feature scaling"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop('target', axis=1)
        
        X_scaled = preprocessor.scale_features(X)
        
        # Check shape preserved
        assert X_scaled.shape == X.shape
        
        # Check mean close to 0 and std close to 1
        assert np.allclose(X_scaled.mean(), 0, atol=0.1)
        assert np.allclose(X_scaled.std(), 1, atol=0.2)
    
    def test_fit_transform(self, sample_data):
        """Test fit_transform method"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop('target', axis=1)
        
        X_transformed = preprocessor.fit_transform(X)
        
        # Check fitting occurred
        assert preprocessor.is_fitted == True
        assert preprocessor.feature_names == X.columns.tolist()
        
        # Check output
        assert X_transformed.shape == X.shape
        assert isinstance(X_transformed, pd.DataFrame)
    
    def test_transform_after_fit(self, sample_data):
        """Test transform on new data after fitting"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop('target', axis=1)
        
        # Fit on data
        preprocessor.fit_transform(X)
        
        # Transform same data
        X_new = X.copy()
        X_transformed = preprocessor.transform(X_new)
        
        assert X_transformed.shape == X_new.shape
    
    def test_transform_before_fit_raises_error(self, sample_data):
        """Test that transform raises error if not fitted"""
        preprocessor = HeartDiseasePreprocessor()
        X = sample_data.drop('target', axis=1)
        
        with pytest.raises(ValueError):
            preprocessor.transform(X)


class TestPrepareData:
    """Test cases for prepare_data function"""
    
    def test_prepare_data_output(self, sample_data, tmp_path):
        """Test prepare_data returns correct outputs"""
        # Save sample data temporarily
        data_file = tmp_path / "test_data.csv"
        sample_data.to_csv(data_file, index=False)
        
        X_train, X_test, y_train, y_test, preprocessor = prepare_data(
            data_file, test_size=0.2, random_state=42
        )
        
        # Check outputs
        assert isinstance(X_train, pd.DataFrame)
        assert isinstance(X_test, pd.DataFrame)
        assert isinstance(y_train, pd.Series)
        assert isinstance(y_test, pd.Series)
        assert isinstance(preprocessor, HeartDiseasePreprocessor)
        
        # Check split proportions
        total_samples = len(sample_data)
        assert len(X_train) + len(X_test) == total_samples
        assert len(y_train) + len(y_test) == total_samples
    
    def test_prepare_data_stratification(self, sample_data, tmp_path):
        """Test that data split maintains class proportions"""
        # Save sample data
        data_file = tmp_path / "test_data.csv"
        sample_data.to_csv(data_file, index=False)
        
        X_train, X_test, y_train, y_test, preprocessor = prepare_data(
            data_file, test_size=0.2, random_state=42
        )
        
        # Check class distribution
        original_ratio = sample_data['target'].mean()
        train_ratio = y_train.mean()
        test_ratio = y_test.mean()
        
        # Ratios should be similar (allowing for small samples)
        assert abs(train_ratio - original_ratio) < 0.3
        assert abs(test_ratio - original_ratio) < 0.5


def test_feature_names_consistency(sample_data):
    """Test that feature names are preserved through preprocessing"""
    preprocessor = HeartDiseasePreprocessor()
    X = sample_data.drop('target', axis=1)
    
    original_features = X.columns.tolist()
    X_transformed = preprocessor.fit_transform(X)
    
    assert preprocessor.feature_names == original_features
    assert X_transformed.columns.tolist() == original_features


def test_preprocessing_reproducibility(sample_data):
    """Test that preprocessing gives same results with same input"""
    preprocessor = HeartDiseasePreprocessor()
    X = sample_data.drop('target', axis=1)
    
    X_transformed1 = preprocessor.fit_transform(X.copy())
    
    # Reset and do again
    preprocessor2 = HeartDiseasePreprocessor()
    X_transformed2 = preprocessor2.fit_transform(X.copy())
    
    # Results should be identical
    pd.testing.assert_frame_equal(X_transformed1, X_transformed2)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
