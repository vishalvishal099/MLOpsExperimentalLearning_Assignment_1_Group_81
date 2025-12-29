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
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from fastapi.responses import PlainTextResponse
import time
import psutil
import os

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
# Request counters
REQUEST_COUNT = Counter('prediction_requests_total', 'Total prediction requests')
HTTP_REQUESTS = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])

# Latency histograms
REQUEST_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
ENDPOINT_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

# Prediction metrics
PREDICTION_COUNTER = Counter('predictions_by_class', 'Predictions by class', ['prediction'])
PREDICTION_RESULTS = Counter('prediction_results_total', 'Total predictions by result', ['result'])
PREDICTION_RISK_LEVEL = Counter('prediction_risk_level_total', 'Predictions by risk level', ['risk_level'])

# Batch prediction metrics
BATCH_REQUEST_COUNT = Counter('batch_prediction_requests_total', 'Total batch prediction requests')
BATCH_SIZE = Histogram('batch_prediction_size', 'Batch prediction size')
BATCH_LATENCY = Histogram('batch_prediction_latency_seconds', 'Batch prediction latency')

# System metrics
CPU_USAGE = Gauge('api_cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('api_memory_usage_bytes', 'Memory usage in bytes')
MEMORY_PERCENT = Gauge('api_memory_usage_percent', 'Memory usage percentage')

# API health
API_HEALTH = Gauge('api_health_status', 'API health status (1=healthy, 0=unhealthy)')

# Get process for system metrics
process = psutil.Process(os.getpid())

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

# Middleware to track HTTP requests
@app.middleware("http")
async def track_requests(request, call_next):
    """Middleware to track all HTTP requests"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate latency
    latency = time.time() - start_time
    
    # Get endpoint path
    endpoint = request.url.path
    method = request.method
    status = response.status_code
    
    # Update metrics
    HTTP_REQUESTS.labels(method=method, endpoint=endpoint, status=str(status)).inc()
    ENDPOINT_LATENCY.labels(method=method, endpoint=endpoint).observe(latency)
    
    # Update system metrics
    try:
        CPU_USAGE.set(process.cpu_percent())
        mem_info = process.memory_info()
        MEMORY_USAGE.set(mem_info.rss)
        MEMORY_PERCENT.set(process.memory_percent())
    except:
        pass
    
    return response

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
        API_HEALTH.set(0)
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    API_HEALTH.set(1)
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
        
        # Log prediction and update metrics
        PREDICTION_COUNTER.labels(prediction=str(prediction)).inc()
        PREDICTION_RESULTS.labels(result=str(prediction)).inc()
        PREDICTION_RISK_LEVEL.labels(risk_level=risk_level).inc()
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
    
    Returns predictions for each patient in the batch
    """
    start_time = time.time()
    BATCH_REQUEST_COUNT.inc()
    BATCH_SIZE.observe(len(patients))
    
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
            
            # Update metrics
            PREDICTION_RESULTS.labels(result=str(prediction)).inc()
            PREDICTION_RISK_LEVEL.labels(risk_level=risk_level).inc()
            
            predictions.append({
                "prediction": int(prediction),
                "probability": float(probability),
                "risk_level": risk_level
            })
        
        # Record batch latency
        batch_latency = time.time() - start_time
        BATCH_LATENCY.observe(batch_latency)
        
        logger.info(f"Batch prediction completed for {len(patients)} patients in {batch_latency:.3f}s")
        return {
            "predictions": predictions, 
            "count": len(predictions),
            "batch_latency": batch_latency
        }
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
