"""
FastAPI application for heart disease prediction
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('prediction_requests_total', 'Total prediction requests')
REQUEST_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
PREDICTION_COUNTER = Counter('predictions_by_class', 'Predictions by class', ['prediction'])

# Initialize FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease risk using machine learning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and preprocessor
BASE_DIR = Path(__file__).parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    logger.info("Model and preprocessor loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None
    preprocessor = None


class PatientData(BaseModel):
    """Input schema for patient data"""
    age: float = Field(..., description="Age in years", ge=0, le=120)
    sex: int = Field(..., description="Sex (1 = male, 0 = female)", ge=0, le=1)
    cp: int = Field(..., description="Chest pain type (1-4)", ge=1, le=4)
    trestbps: float = Field(..., description="Resting blood pressure (mm Hg)", ge=0)
    chol: float = Field(..., description="Serum cholesterol (mg/dl)", ge=0)
    fbs: int = Field(..., description="Fasting blood sugar > 120 mg/dl (1=true, 0=false)", ge=0, le=1)
    restecg: int = Field(..., description="Resting ECG results (0-2)", ge=0, le=2)
    thalach: float = Field(..., description="Maximum heart rate achieved", ge=0, le=250)
    exang: int = Field(..., description="Exercise induced angina (1=yes, 0=no)", ge=0, le=1)
    oldpeak: float = Field(..., description="ST depression induced by exercise", ge=0)
    slope: int = Field(..., description="Slope of peak exercise ST segment (1-3)", ge=1, le=3)
    ca: float = Field(..., description="Number of major vessels colored by fluoroscopy (0-3)", ge=0, le=3)
    thal: float = Field(..., description="Thalassemia (3=normal, 6=fixed defect, 7=reversible defect)")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }


class PredictionResponse(BaseModel):
    """Output schema for prediction"""
    prediction: int = Field(..., description="0 = No disease, 1 = Disease present")
    probability: float = Field(..., description="Probability of disease presence")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")
    timestamp: str = Field(..., description="Prediction timestamp")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API status"""
    return {
        "message": "Heart Disease Prediction API",
        "version": "1.0.0",
        "status": "healthy" if model is not None else "unhealthy",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "metrics": "/metrics"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "preprocessor_loaded": preprocessor is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/metrics", response_class=PlainTextResponse, tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(patient_data: PatientData):
    """
    Predict heart disease risk for a patient
    
    Returns:
    - prediction: 0 (no disease) or 1 (disease present)
    - probability: Probability of disease presence (0-1)
    - risk_level: Low (<0.3), Medium (0.3-0.7), or High (>0.7)
    """
    start_time = time.time()
    REQUEST_COUNT.inc()
    
    # Check if model is loaded
    if model is None or preprocessor is None:
        logger.error("Model or preprocessor not loaded")
        raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        # Convert input to DataFrame
        input_data = pd.DataFrame([patient_data.dict()])
        logger.info(f"Received prediction request: {input_data.to_dict('records')[0]}")
        
        # Preprocess
        input_processed = preprocessor.transform(input_data)
        
        # Predict
        prediction = model.predict(input_processed)[0]
        probability = model.predict_proba(input_processed)[0][1]
        
        # Determine risk level
        if probability < 0.3:
            risk_level = "Low"
        elif probability < 0.7:
            risk_level = "Medium"
        else:
            risk_level = "High"
        
        # Log prediction
        PREDICTION_COUNTER.labels(prediction=str(prediction)).inc()
        logger.info(f"Prediction: {prediction}, Probability: {probability:.4f}, Risk: {risk_level}")
        
        # Record latency
        latency = time.time() - start_time
        REQUEST_LATENCY.observe(latency)
        
        return PredictionResponse(
            prediction=int(prediction),
            probability=float(probability),
            risk_level=risk_level,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(patients: list[PatientData]):
    """
    Predict heart disease risk for multiple patients
    """
    if model is None or preprocessor is None:
        raise HTTPException(status_code=503, detail="Model not available")
    
    try:
        predictions = []
        for patient_data in patients:
            # Convert to DataFrame
            input_data = pd.DataFrame([patient_data.dict()])
            
            # Preprocess and predict
            input_processed = preprocessor.transform(input_data)
            prediction = model.predict(input_processed)[0]
            probability = model.predict_proba(input_processed)[0][1]
            
            # Determine risk level
            if probability < 0.3:
                risk_level = "Low"
            elif probability < 0.7:
                risk_level = "Medium"
            else:
                risk_level = "High"
            
            predictions.append({
                "prediction": int(prediction),
                "probability": float(probability),
                "risk_level": risk_level
            })
        
        logger.info(f"Batch prediction completed for {len(patients)} patients")
        return {"predictions": predictions, "count": len(predictions)}
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
