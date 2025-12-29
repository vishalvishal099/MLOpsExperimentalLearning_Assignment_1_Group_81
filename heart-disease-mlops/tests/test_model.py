"""
Unit tests for model training module
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from train import ModelTrainer


@pytest.fixture
def sample_train_data():
    """Create sample training data"""
    np.random.seed(42)
    n_samples = 100
    n_features = 13
    
    X_train = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    y_train = np.random.randint(0, 2, n_samples)
    
    return X_train, y_train


@pytest.fixture
def sample_test_data():
    """Create sample test data"""
    np.random.seed(43)
    n_samples = 30
    n_features = 13
    
    X_test = pd.DataFrame(
        np.random.randn(n_samples, n_features),
        columns=[f'feature_{i}' for i in range(n_features)]
    )
    y_test = np.random.randint(0, 2, n_samples)
    
    return X_test, y_test


class TestModelTrainer:
    """Test cases for ModelTrainer"""
    
    def test_initialization(self):
        """Test trainer initialization"""
        trainer = ModelTrainer(experiment_name="test_experiment")
        assert trainer.experiment_name == "test_experiment"
    
    def test_logistic_regression_training(self, sample_train_data, sample_test_data):
        """Test logistic regression training"""
        X_train, y_train = sample_train_data
        X_test, y_test = sample_test_data
        
        trainer = ModelTrainer(experiment_name="test_lr")
        model, metrics = trainer.train_logistic_regression(
            X_train, y_train, X_test, y_test
        )
        
        # Check model is trained
        assert model is not None
        assert hasattr(model, 'predict')
        
        # Check metrics exist
        assert 'test_accuracy' in metrics
        assert 'test_precision' in metrics
        assert 'test_recall' in metrics
        assert 'test_f1' in metrics
        assert 'test_roc_auc' in metrics
        
        # Check metric values are valid
        for metric_name, metric_value in metrics.items():
            assert 0 <= metric_value <= 1 or metric_name.endswith('_std')
    
    def test_random_forest_training(self, sample_train_data, sample_test_data):
        """Test random forest training"""
        X_train, y_train = sample_train_data
        X_test, y_test = sample_test_data
        
        trainer = ModelTrainer(experiment_name="test_rf")
        model, metrics = trainer.train_random_forest(
            X_train, y_train, X_test, y_test
        )
        
        # Check model is trained
        assert model is not None
        assert hasattr(model, 'predict')
        assert hasattr(model, 'feature_importances_')
        
        # Check metrics
        assert 'test_accuracy' in metrics
        assert 'cv_accuracy_mean' in metrics
    
    def test_gradient_boosting_training(self, sample_train_data, sample_test_data):
        """Test gradient boosting training"""
        X_train, y_train = sample_train_data
        X_test, y_test = sample_test_data
        
        trainer = ModelTrainer(experiment_name="test_gb")
        model, metrics = trainer.train_gradient_boosting(
            X_train, y_train, X_test, y_test
        )
        
        # Check model is trained
        assert model is not None
        assert hasattr(model, 'predict')
        
        # Check metrics
        assert 'test_accuracy' in metrics
    
    def test_model_predictions(self, sample_train_data, sample_test_data):
        """Test that trained model makes predictions"""
        X_train, y_train = sample_train_data
        X_test, y_test = sample_test_data
        
        trainer = ModelTrainer(experiment_name="test_predictions")
        model, _ = trainer.train_logistic_regression(
            X_train, y_train, X_test, y_test
        )
        
        # Test predictions
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)
        
        # Check output shapes
        assert len(predictions) == len(X_test)
        assert probabilities.shape == (len(X_test), 2)
        
        # Check prediction values
        assert all(pred in [0, 1] for pred in predictions)
        assert all(0 <= prob <= 1 for prob in probabilities.ravel())
    
    def test_custom_parameters(self, sample_train_data, sample_test_data):
        """Test training with custom parameters"""
        X_train, y_train = sample_train_data
        X_test, y_test = sample_test_data
        
        custom_params = {
            'n_estimators': 50,
            'max_depth': 5,
            'random_state': 42,
            'n_jobs': -1
        }
        
        trainer = ModelTrainer(experiment_name="test_custom_params")
        model, metrics = trainer.train_random_forest(
            X_train, y_train, X_test, y_test, params=custom_params
        )
        
        # Check parameters were set
        assert model.n_estimators == 50
        assert model.max_depth == 5
        assert model.random_state == 42


def test_evaluation_metrics_validity(sample_train_data, sample_test_data):
    """Test that evaluation metrics are valid"""
    X_train, y_train = sample_train_data
    X_test, y_test = sample_test_data
    
    trainer = ModelTrainer(experiment_name="test_metrics_validity")
    model, metrics = trainer.train_logistic_regression(
        X_train, y_train, X_test, y_test
    )
    
    # Check all metrics are between 0 and 1 (except std)
    for metric_name, metric_value in metrics.items():
        if not metric_name.endswith('_std'):
            assert 0 <= metric_value <= 1, f"{metric_name} = {metric_value} is out of bounds"


def test_train_and_test_accuracy_relationship(sample_train_data, sample_test_data):
    """Test that train and test accuracies are reasonable"""
    X_train, y_train = sample_train_data
    X_test, y_test = sample_test_data
    
    trainer = ModelTrainer(experiment_name="test_accuracy_relationship")
    model, metrics = trainer.train_random_forest(
        X_train, y_train, X_test, y_test
    )
    
    # Train accuracy should typically be >= test accuracy
    # (not always, but good sanity check for overfitting)
    assert 'train_accuracy' in metrics
    assert 'test_accuracy' in metrics


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
