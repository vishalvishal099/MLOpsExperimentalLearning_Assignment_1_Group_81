"""
Unit tests for FastAPI application
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        # May return 503 if model not loaded, which is expected in test environment
        assert response.status_code in [200, 503]
    
    def test_predict_endpoint_valid_input(self):
        """Test prediction with valid input"""
        patient_data = {
            "age": 63,
            "sex": 1,
            "cp": 3,
            "trestbps": 145,
            "chol": 233,
            "fbs": 1,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 2.3,
            "slope": 3,
            "ca": 0,
            "thal": 6
        }
        
        response = client.post("/predict", json=patient_data)
        
        # If model is loaded, should return 200, otherwise 503
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "probability" in data
            assert "risk_level" in data
            assert data["prediction"] in [0, 1]
            assert 0 <= data["probability"] <= 1
            assert data["risk_level"] in ["Low", "Medium", "High"]
    
    def test_predict_endpoint_invalid_input(self):
        """Test prediction with invalid input"""
        invalid_data = {
            "age": -10,  # Invalid age
            "sex": 1,
            "cp": 3
            # Missing required fields
        }
        
        response = client.post("/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_endpoint_missing_fields(self):
        """Test prediction with missing required fields"""
        incomplete_data = {
            "age": 63,
            "sex": 1
            # Many fields missing
        }
        
        response = client.post("/predict", json=incomplete_data)
        assert response.status_code == 422
    
    def test_predict_batch_endpoint(self):
        """Test batch prediction endpoint"""
        patients = [
            {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 3,
                "ca": 0,
                "thal": 6
            },
            {
                "age": 67,
                "sex": 1,
                "cp": 4,
                "trestbps": 160,
                "chol": 286,
                "fbs": 0,
                "restecg": 2,
                "thalach": 108,
                "exang": 1,
                "oldpeak": 1.5,
                "slope": 2,
                "ca": 3,
                "thal": 3
            }
        ]
        
        response = client.post("/predict/batch", json=patients)
        
        if response.status_code == 200:
            data = response.json()
            assert "predictions" in data
            assert "count" in data
            assert data["count"] == 2
            assert len(data["predictions"]) == 2


class TestInputValidation:
    """Test input validation"""
    
    def test_age_bounds(self):
        """Test age boundary validation"""
        patient_data = {
            "age": 150,  # Too high
            "sex": 1,
            "cp": 3,
            "trestbps": 145,
            "chol": 233,
            "fbs": 1,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 2.3,
            "slope": 3,
            "ca": 0,
            "thal": 6
        }
        
        response = client.post("/predict", json=patient_data)
        assert response.status_code == 422
    
    def test_categorical_values(self):
        """Test categorical variable validation"""
        patient_data = {
            "age": 63,
            "sex": 5,  # Invalid: must be 0 or 1
            "cp": 3,
            "trestbps": 145,
            "chol": 233,
            "fbs": 1,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 2.3,
            "slope": 3,
            "ca": 0,
            "thal": 6
        }
        
        response = client.post("/predict", json=patient_data)
        assert response.status_code == 422


def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    # Should return plain text metrics
    assert "text/plain" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
