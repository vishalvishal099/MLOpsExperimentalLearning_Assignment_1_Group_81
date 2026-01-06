# Heart Disease MLOps Project - Documentation Index

## 📚 Assignment Submission Structure

This documentation is organized according to the assignment requirements. Navigate through each section below:

---

## 1️⃣ Setup/Install Instructions
**Location:** `01_Setup_Installation/`

Essential guides for setting up the project environment and running the application:

- **[START_HERE.md](01_Setup_Installation/START_HERE.md)** - Quick start guide to get the project running
- **[LOCAL_DEPLOYMENT_GUIDE.md](01_Setup_Installation/LOCAL_DEPLOYMENT_GUIDE.md)** - Complete local setup with virtual environment, dependencies, and model training
- **[EXECUTION_GUIDE.md](01_Setup_Installation/EXECUTION_GUIDE.md)** - Step-by-step execution instructions for the entire pipeline
- **[CLOUD_DEPLOYMENT_GUIDE.md](01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md)** - Azure Container Apps deployment setup and configuration

---

## 2️⃣ EDA and Modelling Choices
**Location:** `02_EDA_Modelling/`

Exploratory data analysis and model development documentation:

- **[01_EDA.ipynb](02_EDA_Modelling/01_EDA.ipynb)** - Jupyter notebook with complete exploratory data analysis, visualizations, and statistical summaries
- **Model Selection:** Logistic Regression, Random Forest, Gradient Boosting
- **Best Model:** Random Forest (88.52% accuracy, 0.95 ROC-AUC)
- **Feature Engineering:** StandardScaler preprocessing pipeline
- **Performance Metrics:** See FINAL_SUBMISSION_REPORT.md Section 4

📊 **Key Insights:**
- 303 patient records, 13 features, 0 missing values
- Balanced dataset (45.5% no disease, 54.5% disease)
- Top predictors: chest pain type, ST depression, number of vessels
- 5-fold cross-validation for robust evaluation

---

## 3️⃣ Experiment Tracking Summary
**Location:** `03_Experiment_Tracking/`

MLflow experiment tracking and model versioning:

- **[MODEL_STORAGE_INFO.md](03_Experiment_Tracking/MODEL_STORAGE_INFO.md)** - Model storage locations, versioning strategy, and cloud upload guide

🔬 **Experiment Tracking Details:**
- **MLflow Version:** 2.5.0
- **Experiments Logged:** 3 models with all hyperparameters
- **Metrics Tracked:** Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Artifacts Stored:** Trained models (.pkl), confusion matrices, ROC curves, feature importance plots
- **UI Access:** http://localhost:5000
- **Model Registry:** Complete version control and lineage tracking

📁 **Model Storage:**
- Local: `models/best_model.pkl`, `models/preprocessor.pkl`
- MLflow: `mlruns/` directory with complete experiment history
- Production: Version-tagged models ready for deployment

---

## 4️⃣ Architecture Diagram
**Location:** `04_Architecture/`

System architecture and component design:

- **[ARCHITECTURE.md](04_Architecture/ARCHITECTURE.md)** - Comprehensive system architecture documentation with component descriptions

🏗️ **Architecture Overview:**
- **API Layer:** FastAPI with 4 endpoints (/health, /predict, /predict/batch, /metrics)
- **Model Layer:** Random Forest classifier with preprocessing pipeline
- **Data Layer:** UCI Heart Disease dataset with feature engineering
- **Deployment:** Docker containers orchestrated by Kubernetes
- **Monitoring:** Prometheus + Grafana with 15+ metrics
- **CI/CD:** GitHub Actions with automated testing and deployment
- **Cloud:** Azure Container Apps with auto-scaling

📐 **Key Components:**
1. FastAPI REST API (Port 8000)
2. Prometheus Metrics Server (Port 9090)
3. Grafana Dashboard (Port 3000)
4. MLflow Tracking Server (Port 5000)
5. Kubernetes Cluster (3 replicas, LoadBalancer)

---

## 5️⃣ CI/CD and Deployment Workflow Screenshots
**Location:** `05_CI_CD_Deployment/`

Visual documentation and deployment guides:

- **[GRAFANA_SETUP_GUIDE.md](05_CI_CD_Deployment/GRAFANA_SETUP_GUIDE.md)** - Grafana dashboard setup with monitoring panels
- **[GRAFANA_GUIDE.md](05_CI_CD_Deployment/GRAFANA_GUIDE.md)** - Dashboard usage and metric interpretation
- **[DASHBOARD_SETUP_COMPLETE.md](05_CI_CD_Deployment/DASHBOARD_SETUP_COMPLETE.md)** - Monitoring stack configuration

📸 **Screenshots Available in:** `../screenshots/`
- GitHub Actions workflow runs
- MLflow experiment tracking UI
- Grafana monitoring dashboards
- API Swagger documentation
- Kubernetes deployment status
- Docker containers running
- Test coverage reports

🎥 **Video Demonstration:** `../recorded_video_project_pipeline/`

🔄 **CI/CD Pipeline Stages:**
1. **Lint & Test:** flake8, black, pylint + pytest (85%+ coverage)
2. **Build:** Docker image creation with vulnerability scanning
3. **Integration Tests:** API endpoint testing with health verification
4. **Deploy:** Conditional deployment to staging/production

---

## 6️⃣ Link to Code Repository
**Location:** `06_Repository_Links/`

Access instructions and repository navigation:

- **[ACCESS_INSTRUCTIONS.md](06_Repository_Links/ACCESS_INSTRUCTIONS.md)** - How to access all deployed services and UIs
- **[SAMPLE_DATA_GUIDE.md](06_Repository_Links/SAMPLE_DATA_GUIDE.md)** - Test data usage and API testing guide
- **[DATASET_LOCATION_UPDATE.md](06_Repository_Links/DATASET_LOCATION_UPDATE.md)** - Dataset location and download information

🔗 **GitHub Repository:** [MLOpsExperimentalLearning_Assignment_1_Group_81](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81)

📂 **Key Repository Links:**

**Source Code:**
- [src/train.py](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/train.py) - Model training pipeline
- [src/app.py](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/app.py) - FastAPI application
- [src/preprocessing.py](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/preprocessing.py) - Data preprocessing

**CI/CD:**
- [.github/workflows/ci-cd.yml](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/.github/workflows/ci-cd.yml) - GitHub Actions pipeline

**Infrastructure:**
- [Dockerfile](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/Dockerfile) - Container configuration
- [deployment/kubernetes/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/deployment/kubernetes) - K8s manifests
- [deployment/prometheus/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/deployment/prometheus) - Prometheus config
- [deployment/grafana/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/deployment/grafana) - Grafana dashboards

**Tests:**
- [tests/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/tests) - Test suite (30+ tests, 85%+ coverage)

**Models & Data:**
- [models/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/models) - Trained models (best_model.pkl, preprocessor.pkl)
- [data/processed/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/data/processed) - Processed dataset

**Documentation:**
- [README.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/README.md) - Main project README

---

## 📄 Main Submission Report

**[FINAL_SUBMISSION_REPORT.md](FINAL_SUBMISSION_REPORT.md)** - Comprehensive 10-page final report covering:
- Executive Summary
- Complete MLOps methodology
- Dataset analysis and EDA insights
- Model development and evaluation (88.52% accuracy)
- Experiment tracking with MLflow
- API development and containerization
- CI/CD pipeline implementation
- Production deployment (Kubernetes + Azure)
- Monitoring and observability (Prometheus + Grafana)
- Performance analysis and results
- Challenges, solutions, and lessons learned
- Future enhancements
- Complete reference links

---

## 🎯 Quick Navigation

| Requirement | Primary Document | Supporting Files |
|-------------|-----------------|------------------|
| **Setup Instructions** | LOCAL_DEPLOYMENT_GUIDE.md | START_HERE.md, EXECUTION_GUIDE.md |
| **EDA & Modelling** | 01_EDA.ipynb | FINAL_SUBMISSION_REPORT.md (Sec 2-4) |
| **Experiment Tracking** | MODEL_STORAGE_INFO.md | EXECUTION_GUIDE.md (MLflow section) |
| **Architecture** | ARCHITECTURE.md | FINAL_SUBMISSION_REPORT.md (Sec 8-9) |
| **CI/CD Screenshots** | screenshots/ folder | GRAFANA_SETUP_GUIDE.md, DASHBOARD_SETUP_COMPLETE.md |
| **Repository Links** | FINAL_SUBMISSION_REPORT.md | ACCESS_INSTRUCTIONS.md |

---

## 📊 Project Statistics

- **Models Trained:** 3 (Logistic Regression, Random Forest, Gradient Boosting)
- **Best Accuracy:** 88.52% (Random Forest)
- **Test Coverage:** 85%+ (30+ tests)
- **API Endpoints:** 4 (/health, /predict, /predict/batch, /metrics)
- **Monitoring Metrics:** 15+ Prometheus metrics
- **Deployment:** 3 Kubernetes replicas with auto-scaling
- **API Performance:** <50ms average response time, 250 req/sec max throughput
- **Uptime:** 99.9% reliability

---

## 🚀 Getting Started

1. Start with **[START_HERE.md](01_Setup_Installation/START_HERE.md)** for quick setup
2. Follow **[LOCAL_DEPLOYMENT_GUIDE.md](01_Setup_Installation/LOCAL_DEPLOYMENT_GUIDE.md)** for complete setup
3. Review **[01_EDA.ipynb](02_EDA_Modelling/01_EDA.ipynb)** for data insights
4. Check **[ARCHITECTURE.md](04_Architecture/ARCHITECTURE.md)** for system design
5. Read **[FINAL_SUBMISSION_REPORT.md](FINAL_SUBMISSION_REPORT.md)** for comprehensive overview

---

## 👥 Team Members

| Name | Student ID |
|------|------------|
| GOBIND SAH | 2024AA05643 |
| VISHAL SINGH | 2024AA05641 |
| YASH VERMA | 2024AA05640 |
| AVISHI GUPTA | 2024AA05055 |
| ASIT SHUKLA | 2023AC05956 |

---

**Date:** January 6, 2026  
**Course:** MLOps - Experimental Learning (S1-25_AIMLCZG523)  
**Status:** ✅ Final Submission Ready

---

**END OF INDEX**
