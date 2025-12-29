"""
Model training module with MLflow tracking
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report, roc_curve
)
import mlflow
import mlflow.sklearn
from pathlib import Path
import joblib
import logging
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Model training class with MLflow integration
    """
    
    def __init__(self, experiment_name="heart_disease_prediction"):
        """Initialize trainer with MLflow experiment"""
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name
        logger.info(f"MLflow experiment: {experiment_name}")
        
    def train_logistic_regression(self, X_train, y_train, X_test, y_test, params=None):
        """Train Logistic Regression model"""
        if params is None:
            params = {
                'max_iter': 1000,
                'random_state': 42,
                'solver': 'lbfgs'
            }
        
        with mlflow.start_run(run_name="Logistic_Regression"):
            # Log parameters
            mlflow.log_params(params)
            
            # Train model
            logger.info("Training Logistic Regression...")
            model = LogisticRegression(**params)
            model.fit(X_train, y_train)
            
            # Evaluate
            metrics = self._evaluate_model(model, X_train, y_train, X_test, y_test)
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            logger.info("Logistic Regression training complete!")
            return model, metrics
    
    def train_random_forest(self, X_train, y_train, X_test, y_test, params=None):
        """Train Random Forest model"""
        if params is None:
            params = {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42,
                'n_jobs': -1
            }
        
        with mlflow.start_run(run_name="Random_Forest"):
            # Log parameters
            mlflow.log_params(params)
            
            # Train model
            logger.info("Training Random Forest...")
            model = RandomForestClassifier(**params)
            model.fit(X_train, y_train)
            
            # Evaluate
            metrics = self._evaluate_model(model, X_train, y_train, X_test, y_test)
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log feature importances
            self._log_feature_importances(model, X_train.columns)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            logger.info("Random Forest training complete!")
            return model, metrics
    
    def train_gradient_boosting(self, X_train, y_train, X_test, y_test, params=None):
        """Train Gradient Boosting model"""
        if params is None:
            params = {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 5,
                'min_samples_split': 5,
                'min_samples_leaf': 2,
                'random_state': 42
            }
        
        with mlflow.start_run(run_name="Gradient_Boosting"):
            # Log parameters
            mlflow.log_params(params)
            
            # Train model
            logger.info("Training Gradient Boosting...")
            model = GradientBoostingClassifier(**params)
            model.fit(X_train, y_train)
            
            # Evaluate
            metrics = self._evaluate_model(model, X_train, y_train, X_test, y_test)
            
            # Log metrics
            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, metric_value)
            
            # Log feature importances
            self._log_feature_importances(model, X_train.columns)
            
            # Log model
            mlflow.sklearn.log_model(model, "model")
            
            logger.info("Gradient Boosting training complete!")
            return model, metrics
    
    def _evaluate_model(self, model, X_train, y_train, X_test, y_test):
        """Evaluate model and return metrics"""
        # Predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        y_test_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'train_accuracy': accuracy_score(y_train, y_train_pred),
            'test_accuracy': accuracy_score(y_test, y_test_pred),
            'test_precision': precision_score(y_test, y_test_pred, zero_division=0),
            'test_recall': recall_score(y_test, y_test_pred),
            'test_f1': f1_score(y_test, y_test_pred),
            'test_roc_auc': roc_auc_score(y_test, y_test_proba)
        }
        
        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
        metrics['cv_accuracy_mean'] = cv_scores.mean()
        metrics['cv_accuracy_std'] = cv_scores.std()
        
        # Log confusion matrix
        cm = confusion_matrix(y_test, y_test_pred)
        self._log_confusion_matrix(cm)
        
        # Log ROC curve
        self._log_roc_curve(y_test, y_test_proba)
        
        return metrics
    
    def _log_feature_importances(self, model, feature_names):
        """Log feature importances plot"""
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            plt.figure(figsize=(10, 6))
            plt.title("Feature Importances")
            plt.bar(range(len(importances)), importances[indices])
            plt.xticks(range(len(importances)), 
                      [feature_names[i] for i in indices], 
                      rotation=45, ha='right')
            plt.tight_layout()
            
            # Save and log
            plt.savefig("feature_importances.png")
            mlflow.log_artifact("feature_importances.png")
            plt.close()
    
    def _log_confusion_matrix(self, cm):
        """Log confusion matrix plot"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['No Disease', 'Disease'],
                   yticklabels=['No Disease', 'Disease'])
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        
        # Save and log
        plt.savefig("confusion_matrix.png")
        mlflow.log_artifact("confusion_matrix.png")
        plt.close()
    
    def _log_roc_curve(self, y_true, y_proba):
        """Log ROC curve plot"""
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        auc = roc_auc_score(y_true, y_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, linewidth=2, label=f'ROC curve (AUC = {auc:.3f})')
        plt.plot([0, 1], [0, 1], 'k--', linewidth=2, label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        # Save and log
        plt.savefig("roc_curve.png")
        mlflow.log_artifact("roc_curve.png")
        plt.close()
    
    def hyperparameter_tuning(self, model_type, X_train, y_train, param_grid):
        """Perform hyperparameter tuning with GridSearchCV"""
        logger.info(f"Starting hyperparameter tuning for {model_type}...")
        
        if model_type == 'logistic_regression':
            base_model = LogisticRegression(max_iter=1000, random_state=42)
        elif model_type == 'random_forest':
            base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        elif model_type == 'gradient_boosting':
            base_model = GradientBoostingClassifier(random_state=42)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        grid_search = GridSearchCV(
            base_model, param_grid, cv=5, scoring='roc_auc', 
            n_jobs=-1, verbose=1
        )
        grid_search.fit(X_train, y_train)
        
        logger.info(f"Best parameters: {grid_search.best_params_}")
        logger.info(f"Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_, grid_search.best_params_


def save_model(model, preprocessor, model_path, preprocessor_path):
    """Save model and preprocessor"""
    model_path = Path(model_path)
    preprocessor_path = Path(preprocessor_path)
    
    model_path.parent.mkdir(parents=True, exist_ok=True)
    preprocessor_path.parent.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, model_path)
    joblib.dump(preprocessor, preprocessor_path)
    
    logger.info(f"Model saved to: {model_path}")
    logger.info(f"Preprocessor saved to: {preprocessor_path}")


def load_model(model_path, preprocessor_path):
    """Load model and preprocessor"""
    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    logger.info("Model and preprocessor loaded successfully!")
    return model, preprocessor


if __name__ == "__main__":
    from preprocessing import prepare_data
    
    # Prepare data
    BASE_DIR = Path(__file__).parent.parent
    DATA_PATH = BASE_DIR / "data" / "processed" / "heart_disease.csv"
    
    X_train, X_test, y_train, y_test, preprocessor = prepare_data(DATA_PATH)
    
    # Train models
    trainer = ModelTrainer()
    
    # Logistic Regression
    lr_model, lr_metrics = trainer.train_logistic_regression(
        X_train, y_train, X_test, y_test
    )
    
    # Random Forest
    rf_model, rf_metrics = trainer.train_random_forest(
        X_train, y_train, X_test, y_test
    )
    
    print("\n" + "="*80)
    print("MODEL COMPARISON")
    print("="*80)
    print("\nLogistic Regression:")
    for metric, value in lr_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    print("\nRandom Forest:")
    for metric, value in rf_metrics.items():
        print(f"  {metric}: {value:.4f}")
    print("="*80)
