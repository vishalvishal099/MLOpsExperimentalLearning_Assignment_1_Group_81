# Heart Disease Prediction - MLOps Project

![Python](https://img.shields.io/badge/Python-3.9-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.101.0-green)
![MLflow](https://img.shields.io/badge/MLflow-2.5.0-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue)

## 📋 Project Overview

This project implements an end-to-end MLOps pipeline for predicting heart disease risk using the UCI Heart Disease dataset. The solution includes data preprocessing, model training with experiment tracking, containerization, CI/CD pipelines, and production deployment with monitoring.

### Key Features

- ✅ **Data Processing**: Automated data acquisition and preprocessing pipeline
- ✅ **Model Training**: Multiple ML models (Logistic Regression, Random Forest, Gradient Boosting)
- ✅ **Experiment Tracking**: MLflow integration for comprehensive experiment management
- ✅ **API Service**: FastAPI-based REST API for real-time predictions
- ✅ **Containerization**: Docker containerization for reproducibility
- ✅ **CI/CD**: Automated GitHub Actions pipeline
- ✅ **Deployment**: Kubernetes manifests for cloud deployment
- ✅ **Monitoring**: Prometheus and Grafana integration
- ✅ **Testing**: Comprehensive unit and integration tests

## 📊 Dataset

**Source**: UCI Machine Learning Repository - Heart Disease Dataset

- **Instances**: 303 patients from Cleveland Clinic Foundation
- **Features**: 13 clinical features
- **Target**: Binary classification (presence/absence of heart disease)

### Features

| Feature | Description | Type |
|---------|-------------|------|
| age | Age in years | Continuous |
| sex | Sex (1=male, 0=female) | Binary |
| cp | Chest pain type (1-4) | Categorical |
| trestbps | Resting blood pressure (mm Hg) | Continuous |
| chol | Serum cholesterol (mg/dl) | Continuous |
| fbs | Fasting blood sugar > 120 mg/dl | Binary |
| restecg | Resting ECG results (0-2) | Categorical |
| thalach | Maximum heart rate achieved | Continuous |
| exang | Exercise induced angina | Binary |
| oldpeak | ST depression induced by exercise | Continuous |
| slope | Slope of peak exercise ST segment | Categorical |
| ca | Number of major vessels (0-3) | Discrete |
| thal | Thalassemia (3, 6, 7) | Categorical |

## 🏗️ Project Structure

**Important:** The project expects the following directory structure:

```
<parent_directory>/
├── heart-disease-mlops/              # Main project directory (this repo)
│   ├── .github/
│   │   └── workflows/
│   │       └── ci-cd.yml            # GitHub Actions CI/CD pipeline
│   ├── data/
│   │   ├── raw/                     # Raw data files (auto-generated)
│   │   └── processed/               # Processed data files (auto-generated)
│   ├── deployment/
│   │   └── kubernetes/
│   │       ├── deployment.yaml      # Kubernetes deployment
│   │       ├── ingress.yaml         # Ingress configuration
│   │       └── monitoring.yaml      # Prometheus & Grafana setup
│   ├── docs/
│   │   └── architecture_diagram.png # System architecture
│   ├── models/
│   │   ├── best_model.pkl          # Trained model (auto-generated)
│   │   └── preprocessor.pkl        # Data preprocessor (auto-generated)
│   ├── notebooks/
│   │   ├── 01_EDA.ipynb            # Exploratory Data Analysis
│   │   ├── 02_Model_Training.ipynb # Model training experiments
│   │   └── 03_Model_Evaluation.ipynb # Model evaluation
│   ├── screenshots/                 # Screenshots for documentation
│   ├── src/
│   │   ├── app.py                  # FastAPI application
│   │   ├── download_data.py        # Data acquisition script
│   │   ├── preprocessing.py        # Data preprocessing module
│   │   └── train.py                # Model training module
│   ├── tests/
│   │   ├── test_preprocessing.py   # Preprocessing tests
│   │   ├── test_model.py           # Model tests
│   │   └── test_api.py             # API tests
│   ├── .gitignore
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── raw_dataSet/                      # Dataset directory (inside project)
│   └── heart+disease/
│       ├── processed.cleveland.data  # Main dataset file
│       ├── cleveland.data
│       └── heart-disease.names
```

**Note:** The UCI Heart Disease dataset is now located in `raw_dataSet/heart+disease/` within the project directory. The `src/download_data.py` script will copy files from there to the project's `data/` directory.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Docker (for containerization)
- Kubernetes cluster (for deployment)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/heart-disease-mlops.git
cd heart-disease-mlops
```

2. **Setup dataset directory**
```bash
# Ensure dataset is placed in the correct location:
# raw_dataSet/heart+disease/ (within project directory)
ls raw_dataSet/heart+disease/
```

3. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download and prepare data**
```bash
python src/download_data.py
```

### Usage

#### 1. Exploratory Data Analysis

```bash
jupyter notebook notebooks/01_EDA.ipynb
```

#### 2. Train Models

```bash
# Train with default parameters
python src/train.py

# View MLflow UI
mlflow ui
# Access at http://localhost:5000
```

#### 3. Run API Locally

```bash
# Start the API
uvicorn src.app:app --reload

# Access API docs at http://localhost:8000/docs
```

#### 4. Make Predictions

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

#### 5. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html
```

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t heart-disease-api:latest .
```

### Run Docker Container

```bash
docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest
```

### Test Docker Container

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @sample_input.json
```

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Apply deployment
kubectl apply -f deployment/kubernetes/deployment.yaml

# Apply ingress
kubectl apply -f deployment/kubernetes/ingress.yaml

# Deploy monitoring stack
kubectl apply -f deployment/kubernetes/monitoring.yaml

# Check deployment status
kubectl get pods
kubectl get services
```

### Access Services

```bash
# Get external IP
kubectl get svc heart-disease-api-service

# Port forward for local testing
kubectl port-forward svc/heart-disease-api-service 8000:80
```

## 📈 Monitoring

### Prometheus Metrics

Access Prometheus at: `http://<prometheus-service-ip>:9090`

Available metrics:
- `prediction_requests_total` - Total prediction requests
- `prediction_latency_seconds` - Prediction latency histogram
- `predictions_by_class` - Predictions grouped by class

### Grafana Dashboards

Access Grafana at: `http://<grafana-service-ip>:3000`

Default credentials:
- Username: `admin`
- Password: `admin`

## 🧪 Testing

### Unit Tests

```bash
# Test preprocessing
pytest tests/test_preprocessing.py -v

# Test model training
pytest tests/test_model.py -v

# Test API
pytest tests/test_api.py -v
```

### Integration Tests

```bash
pytest tests/ -v --integration
```

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|-------|----------|-----------|--------|----------|---------|
| Logistic Regression | 85.2% | 84.1% | 83.7% | 83.9% | 0.91 |
| Random Forest | 87.5% | 86.8% | 85.9% | 86.3% | 0.94 |
| Gradient Boosting | 88.1% | 87.3% | 86.5% | 86.9% | 0.95 |

*Note: Actual results will be generated after training*

## 🔄 CI/CD Pipeline

The GitHub Actions pipeline includes:

1. **Lint & Test**: Code quality checks and unit tests
2. **Train Model**: Automated model training with MLflow tracking
3. **Build Docker**: Container image creation and testing
4. **Deploy**: Deployment to production (when merged to main)

## 📝 API Endpoints

### Health Check
```
GET /health
```

### Predict Single
```
POST /predict
Body: PatientData JSON
Response: PredictionResponse
```

### Predict Batch
```
POST /predict/batch
Body: List[PatientData]
Response: List[PredictionResponse]
```

### Metrics
```
GET /metrics
Response: Prometheus metrics
```

## 🏆 MLOps Best Practices Implemented

- ✅ Version control for code and data
- ✅ Experiment tracking with MLflow
- ✅ Reproducible preprocessing pipelines
- ✅ Automated testing (unit and integration)
- ✅ Continuous integration/deployment
- ✅ Containerization for consistency
- ✅ Kubernetes orchestration
- ✅ Model monitoring and logging
- ✅ API documentation (OpenAPI/Swagger)
- ✅ Comprehensive documentation

## 📄 License

This project is licensed under the MIT License.

## 👥 Contributors

- Your Name - Initial work

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the dataset
- Cleveland Clinic Foundation for data collection
- FastAPI and MLflow communities

## 📧 Contact

For questions or feedback, please reach out to: your.email@example.com

---

**Note**: This project is part of an MLOps assignment demonstrating end-to-end ML deployment practices.
