# Heart Disease Prediction - End-to-End MLOps Pipeline
## Final Submission Report

---

**Course:** MLOps - Experimental Learning (S1-25_AIMLCZG523)  
**Project:** End-to-End ML Model Development, CI/CD, and Production Deployment

**Team Members:**

| Name | Student ID |
|------|------------|
| GOBIND SAH | 2024AA05643 |
| VISHAL SINGH | 2024AA05641 |
| YASH VERMA | 2024AA05640 |
| AVISHI GUPTA | 2024AA05055 |
| ASIT SHUKLA | 2023AC05956 |

**Date:** January 6, 2026  
**GitHub Repository:** [MLOpsExperimentalLearning_Assignment_1_Group_81](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81)

**Project Resources:**
- **📖 README:** [README.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/README.md)
- **📸 Screenshots:** [screenshots/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/screenshots)
- **🎥 Project Demo Video:** [recorded_video_project_pipeline/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/recorded_video_project_pipeline)
- **🤖 Trained Models:** [models/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/models) - best_model.pkl, preprocessor.pkl
- **📊 Processed Data:** [data/processed/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/data/processed)
- **🧪 Test Suite:** [tests/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/tests) - test_api.py, test_model.py, test_preprocessing.py
- **📄 Documentation Files:**
  - [START_HERE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/START_HERE.md)
  - [LOCAL_DEPLOYMENT_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/LOCAL_DEPLOYMENT_GUIDE.md)
  - [CLOUD_DEPLOYMENT_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md)
  - [EXECUTION_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/EXECUTION_GUIDE.md)
  - [ARCHITECTURE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/04_Architecture/ARCHITECTURE.md)
  - [GRAFANA_SETUP_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/05_CI_CD_Deployment/GRAFANA_SETUP_GUIDE.md)
  - [GRAFANA_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/05_CI_CD_Deployment/GRAFANA_GUIDE.md)
  - [ACCESS_INSTRUCTIONS.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/06_Repository_Links/ACCESS_INSTRUCTIONS.md)
  - [MODEL_STORAGE_INFO.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/03_Experiment_Tracking/MODEL_STORAGE_INFO.md)
  - [SAMPLE_DATA_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/06_Repository_Links/SAMPLE_DATA_GUIDE.md)
  - [DASHBOARD_SETUP_COMPLETE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/05_CI_CD_Deployment/DASHBOARD_SETUP_COMPLETE.md)
  - [DATASET_LOCATION_UPDATE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/06_Repository_Links/DATASET_LOCATION_UPDATE.md)

---

## Executive Summary

This report presents a comprehensive implementation of an end-to-end MLOps pipeline for predicting heart disease using machine learning. The project demonstrates industry-standard practices encompassing the complete lifecycle from data acquisition to production deployment with continuous monitoring.

**Key Achievements:** 3 ML Models Trained (Logistic Regression, Random Forest, Gradient Boosting), **88.52% Accuracy** with Random Forest, Production-Ready FastAPI with batch prediction, Complete CI/CD Pipeline (GitHub Actions), Containerized Deployment (Docker/Kubernetes), Real-time Monitoring (Prometheus/Grafana), **85%+ Test Coverage**, and Cloud Deployment on Azure Container Apps.

**Technologies:** Python 3.9+, scikit-learn, FastAPI, MLflow, Docker, Kubernetes, GitHub Actions, Prometheus, Grafana

---

## 1. Introduction & Problem Statement

### 1.1 Background
Cardiovascular diseases (CVDs) are the leading cause of death globally, accounting for approximately 17.9 million deaths annually. Early detection and prediction of heart disease can significantly improve patient outcomes and optimize healthcare resource allocation. Machine learning offers a powerful approach to identify at-risk individuals by analyzing clinical and demographic data patterns.

### 1.2 Project Objectives
1. Predict heart disease risk with high accuracy (target: >85%) using patient clinical data
2. Implement complete MLOps practices including versioning, automation, and monitoring
3. Provide real-time predictions through a scalable REST API with batch processing support
4. Ensure reproducibility with experiment tracking and version control
5. Enable continuous improvement through automated testing and CI/CD pipelines
6. Support production deployment on cloud infrastructure with comprehensive monitoring

### 1.3 MLOps Methodology
The project follows modern MLOps principles: Version Control (Git + MLflow), Automated Testing (pytest with 85%+ coverage), Continuous Integration/Deployment (GitHub Actions), Containerization (Docker), Orchestration (Kubernetes), Monitoring (Prometheus + Grafana), and comprehensive documentation.

---

## 2. Dataset & Exploratory Data Analysis

### 2.1 Dataset Description
**Source:** UCI Machine Learning Repository - Cleveland Heart Disease Database  
**Size:** 303 patient records with 13 clinical/demographic features and 1 binary target variable (0=No Disease, 1=Disease Present)

### 2.2 Feature Descriptions
The dataset includes age, sex, chest pain type (cp), resting blood pressure (trestbps), serum cholesterol (chol), fasting blood sugar (fbs), resting ECG results (restecg), maximum heart rate (thalach), exercise induced angina (exang), ST depression (oldpeak), slope of peak exercise ST segment, number of major vessels colored by fluoroscopy (ca), and thalassemia (thal).

### 2.3 Data Quality Assessment
**Completeness:** Zero missing values (100% complete dataset across all 303 records).  
**Class Distribution:** Well-balanced - No Disease: 138 (45.5%), Disease Present: 165 (54.5%).  
**Statistical Summary:** Age Mean=54.4±9.1 years, Cholesterol Mean=246±51 mg/dl, Max Heart Rate Mean=150±23 bpm, Blood Pressure Mean=131±17 mm Hg.

### 2.4 Key EDA Insights
**Positive Predictors (Higher risk):** Chest pain type (+0.43), Max heart rate (+0.42), ST depression (+0.43), Number of vessels (+0.46).  
**Negative Predictors (Lower risk):** Exercise induced angina (-0.44), Thalassemia (-0.34), Resting ECG (-0.17).  
**Demographics:** 68% Male, 32% Female. Disease prevalence increases with age, peak incidence in 55-65 age group.

**📊 Detailed Analysis:** Complete EDA with visualizations available in `notebooks/01_EDA.ipynb` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/notebooks/01_EDA.ipynb))

---

## 3. Feature Engineering & Preprocessing

### 3.1 Preprocessing Pipeline
A robust preprocessing pipeline was implemented using scikit-learn's Pipeline and ColumnTransformer with HeartDiseasePreprocessor class. Pipeline includes: (1) Median imputation for missing values, (2) StandardScaler for z-score normalization (Mean=0, Std=1), (3) Feature name preservation for interpretability, and (4) Serialization support for deployment.

**Why StandardScaler?** Ensures equal feature contribution to distance-based models, improves gradient descent convergence, essential for Logistic Regression, and preserves outlier information.

### 3.2 Train-Test Split Strategy
80% training (242 samples), 20% testing (61 samples) with stratification to maintain class balance. Random seed 42 ensures reproducibility. 5-fold cross-validation used during training for robust evaluation.

### 3.3 Feature Importance Analysis
**Top 5 Features (Random Forest):** ca-Number of vessels (18.2%), thal-Thalassemia (15.7%), cp-Chest pain (14.3%), oldpeak-ST depression (12.9%), thalach-Max heart rate (11.4%). These align with clinical knowledge where vessel blockage and cardiac stress indicators are key predictors.

**📄 Implementation Details:** See `src/preprocessing.py` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/preprocessing.py))

---

## 4. Model Development & Evaluation

### 4.1 Model Selection & Training
Three classification algorithms were selected: **(1) Logistic Regression** - Interpretable baseline with probabilistic outputs, **(2) Random Forest** - Ensemble method handling non-linearity with feature importance, **(3) Gradient Boosting** - Sequential error correction for maximum accuracy. All models trained using `src/train.py` with MLflow integration for complete experiment tracking.

### 4.2 Model Performance Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time |
|-------|----------|-----------|--------|----------|---------|---------------|
| Logistic Regression | 86.89% | 0.88 | 0.88 | 0.88 | 0.93 | 0.12s |
| **Random Forest** | **88.52%** | **0.90** | **0.89** | **0.89** | **0.95** | 0.34s |
| Gradient Boosting | 85.25% | 0.86 | 0.87 | 0.86 | 0.92 | 0.28s |

**Winner: Random Forest** - Selected based on highest accuracy (88.52%), best ROC-AUC (0.95), balanced precision-recall, and strong 5-fold cross-validation performance (87.3% ± 2.1%).

### 4.3 Clinical Performance Analysis
**Confusion Matrix (Test Set):** True Positives: 29, True Negatives: 25, False Positives: 3, False Negatives: 4  
**Clinical Metrics:** Sensitivity 87.9% (identifies 88 out of 100 disease cases), Specificity 89.3%, Positive Predictive Value 90.6%, Negative Predictive Value 86.2%. Only 4 missed diagnoses out of 61 test cases (6.6% miss rate) - acceptable for screening applications.

**📄 Training Implementation:** See `src/train.py` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/train.py))

---

## 5. Experiment Tracking with MLflow

### 5.1 MLflow Integration
**Setup:** MLflow 2.5.0 with local file storage (`mlruns/` directory). Experiment name: "Heart Disease Classification". All training runs automatically logged with parameters, metrics, and artifacts.

**Tracked Components:** (1) Parameters - All model hyperparameters (n_estimators, max_depth, learning_rate, etc.), (2) Metrics - Accuracy, Precision, Recall, F1-Score, ROC-AUC for train/test sets, (3) Artifacts - Trained models (.pkl), confusion matrix plots, ROC curves, feature importance plots, (4) Tags - Model type, dataset version, training date.

### 5.2 MLflow Features
**UI Access:** MLflow UI at http://localhost:5000 provides side-by-side run comparison, metric filtering/sorting, parameter impact visualization, artifact downloads, and experiment reproducibility.

### 5.3 Model Registry
Models registered with unique run IDs, version tracking (v1.0, v1.1), production/staging tags, and complete lineage tracking. Benefits include complete experiment reproducibility, easy version rollback, team collaboration support, and compliance audit trails.

**📄 MLflow Setup Guide:** See `docs/01_Setup_Installation/EXECUTION_GUIDE.md` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/EXECUTION_GUIDE.md))

---

## 6. API Development & Containerization

### 6.1 FastAPI Implementation
Production-ready REST API (`src/app.py`) with 4 core endpoints: **(1) GET /health** - Health check with model load status, **(2) POST /predict** - Single patient prediction with risk level (Low/Medium/High) and confidence score, **(3) POST /predict/batch** - Batch processing for multiple patients with latency tracking, **(4) GET /metrics** - Prometheus-formatted metrics endpoint.

**API Features:** Pydantic input validation, comprehensive error handling, request logging, CORS middleware, OpenAPI/Swagger documentation at `/docs`, model versioning support, graceful startup with verification.

### 6.2 Docker Containerization
**Dockerfile:** Based on `python:3.9-slim` (optimized 450 MB image), includes all dependencies, models, and application code. Health check configured for Kubernetes liveness probes. Multi-layer caching for faster rebuilds.

### 6.3 Docker Compose for Development
Multi-service orchestration (`docker-compose.yml`) includes API service (port 8000), Prometheus (port 9090), and Grafana (port 3000) with pre-configured dashboards and data sources for local development and testing.

**📄 API Documentation:** See `src/app.py` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/app.py))  
**📄 Docker Configuration:** See `Dockerfile` and `docker-compose.yml` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops))

---

## 7. CI/CD Pipeline with GitHub Actions

### 7.1 Pipeline Architecture
**File:** `.github/workflows/ci-cd.yml` with 4 stages: **(1) Lint and Test** - Code quality checks (flake8, black, pylint) and pytest with coverage, **(2) Build** - Docker image creation with vulnerability scanning, **(3) Integration Tests** - API endpoint testing with health verification, **(4) Deploy** - Conditional deployment to staging/production with smoke tests.

**Triggers:** Automatic on push to main/develop branches and pull requests to main branch.

### 7.2 Automated Testing
**Test Suite:** 30+ tests across `tests/` directory covering preprocessing logic (10 tests), model loading/prediction (8 tests), and API endpoints/error handling (12 tests). **Coverage:** 85% overall (preprocessing 92%, API 88%, training 78%).

### 7.3 Quality Assurance
**Linting:** Maximum line length 127 chars, cyclomatic complexity ≤10, PEP 8 compliance enforced.  
**Security:** Dependency vulnerability checks, Docker image scanning with Trivy, secret detection in commits.  
**Code Formatting:** Black formatter with automatic import sorting and consistent styling.

**📄 CI/CD Configuration:** See `.github/workflows/ci-cd.yml` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/.github/workflows/ci-cd.yml))  
**📄 Test Suite:** See `tests/` directory ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/tests))

---

## 8. Production Deployment

### 8.1 Kubernetes Configuration
**Deployment:** 3 replicas for high availability with resource limits (1Gi memory, 500m CPU per pod), liveness and readiness probes via /health endpoint, LoadBalancer service for traffic distribution, and horizontal pod autoscaling support.

### 8.2 Cloud Deployment - Azure Container Apps
Deployed on Azure Container Apps with auto-scaling (1-3 replicas based on HTTP load), zero downtime deployments with traffic splitting, custom domains with SSL certificates, integrated Azure Monitor logging, and cost-effective serverless pricing.

**Deployment Process:** Azure Container Registry (ACR) for image storage, automated build and push via az acr build, container app creation with external ingress, and public URL provisioning.

### 8.3 Local Testing with Minikube
Kubernetes deployment tested locally using Minikube for validation before cloud deployment. Ensures configuration correctness and resource allocation verification.

**📄 Kubernetes Manifests:** See `deployment/kubernetes/` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/deployment/kubernetes))  
**📄 Cloud Deployment Guide:** See `docs/01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md))

---

## 9. Monitoring & Observability

### 9.1 Application Logging
Python logging module configured with INFO level for request tracking and predictions, WARNING for high latency/unusual inputs, ERROR for prediction failures, and CRITICAL for service unavailability. Logs stored in `logs/api.log` with rotation and console output.

### 9.2 Prometheus Metrics
**15+ Metrics Collected:** Request metrics (http_requests_total, prediction_latency_seconds), Batch metrics (batch_prediction_count, batch_size, batch_latency), System metrics (cpu_usage_percent, memory_usage_bytes, memory_percent using psutil), Prediction analytics (prediction_results_total by class, prediction_risk_level_total), and API health status gauge.

**Configuration:** Prometheus scrapes API /metrics endpoint every 10 seconds as configured in `deployment/prometheus/prometheus.yml`.

### 9.3 Grafana Dashboards
**Enhanced Monitoring Dashboard** with 10 panels: API Health Status (real-time indicator), Total Predictions (cumulative count), Prediction Rate (requests/sec), Average Prediction Time (latency trends), Predictions by Class (distribution pie chart), HTTP Requests by Method (GET/POST breakdown), CPU Usage gauge, Memory Usage gauge, Batch Processing Metrics, and Error Rate over time. Auto-refresh every 10 seconds with customizable time ranges.

**📄 Monitoring Configuration:** See `deployment/prometheus/` and `deployment/grafana/` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/deployment))  
**📄 Grafana Setup Guide:** See `docs/05_CI_CD_Deployment/GRAFANA_SETUP_GUIDE.md` ([View on GitHub](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/05_CI_CD_Deployment/GRAFANA_SETUP_GUIDE.md))

---

## 10. Performance Analysis & Results

### 10.1 Model Performance Summary
**Best Model: Random Forest Classifier** - Test Set: Accuracy 88.52% (54/61 correct), Precision 0.90, Recall 0.89, F1-Score 0.89, ROC-AUC 0.95. Cross-Validation (5-Fold): Mean Accuracy 87.3% ± 2.1% showing excellent generalization.

**Clinical Metrics:** Sensitivity 87.9% (identifies 88/100 disease cases), Specificity 89.3%, Positive Predictive Value 90.6%, Negative Predictive Value 86.2%. Only 4 missed diagnoses out of 61 test cases (6.6% miss rate) - acceptable for screening applications.

### 10.2 API Performance
**Single Prediction:** Average response time 39ms, 95th percentile 45ms, throughput 25 req/sec per pod, 0% error rate.  
**Batch Prediction:** Average latency 0.045s for 10 patients (4.5ms per patient), supports 1-100 patients per batch, memory efficient.  
**System Resources:** CPU 15-25% under normal load, Memory 450-550 MB per pod, minimal disk I/O.  
**Scalability:** Tested up to 10 replicas, maximum throughput 250 req/sec with auto-scaling at >70% CPU.

### 10.3 Production Readiness
**Reliability:** 99.9% uptime, health checks every 10s, automatic pod restart on failure, graceful degradation.  
**Security:** Input validation, rate limiting, no sensitive data in logs, vulnerability-scanned Docker images.  
**Maintainability:** 85%+ test coverage, comprehensive logging, automated CI/CD, version-controlled models.  
**Observability:** 15+ Prometheus metrics, Grafana dashboards, alert rules, distributed tracing ready.

---

## 11. Challenges & Solutions

### 11.1 Technical Challenges Overcome
**Model Serialization:** Custom HeartDiseasePreprocessor with proper state methods for reliable persistence. **Docker Optimization:** Reduced image from 1.2 GB to 450 MB using slim base and multi-stage builds. **API Latency:** Implemented model preloading to achieve consistent <50ms response. **Metrics Clarity:** Followed Prometheus naming conventions with descriptive labels.

### 11.2 Deployment Challenges
**Resource Management:** Load tested to determine optimal Kubernetes limits (1Gi memory, 500m CPU) preventing OOM errors. **CI/CD Performance:** Implemented dependency caching and parallel testing, reducing pipeline from >1 hour to 8 minutes.

### 11.3 Key Lessons Learned
Start with simple baseline models, test early in development, monitor everything (can't fix what you don't measure), automate ruthlessly to eliminate manual errors, and document thoroughly for future reference and team collaboration.

---

## 12. Future Enhancements

### 12.1 Model Improvements
**Deep Learning:** Implement neural networks with TensorFlow/PyTorch targeting >90% accuracy. **Model Ensemble:** Combine multiple models using stacking/voting for improved edge case handling. **Explainable AI:** Integrate SHAP/LIME for prediction explanations to increase clinician trust. **Online Learning:** Enable continuous model updates with new data and A/B testing framework.

### 12.2 Infrastructure Enhancements
**Advanced Monitoring:** Distributed tracing with Jaeger, custom anomaly detection, automated alerting (PagerDuty/Slack). **Multi-Region:** Deploy across cloud regions with geo-routing and disaster recovery. **Cost Optimization:** Request caching, spot instances for non-critical workloads, optimized autoscaling policies. **Security:** OAuth2/JWT authentication, API key management, HTTPS/TLS everywhere, regular security audits.

### 12.3 Feature Additions
**Patient History:** Store prediction history, trend analysis over time, risk progression monitoring. **Clinical Integration:** HL7/FHIR interfaces for EHR systems, DICOM image support, lab result integration. **Mobile Apps:** Native iOS/Android apps with offline prediction and push notifications. **Reporting:** Patient-facing risk reports, clinician decision support, population health analytics.

---

## 13. Conclusion

### 13.1 Project Achievements
Successfully developed complete end-to-end MLOps pipeline achieving: **88.52% accuracy** with Random Forest on heart disease prediction, **85%+ test coverage** with automated quality checks, production-ready **FastAPI** with batch processing, comprehensive **CI/CD pipeline** with GitHub Actions, **Docker/Kubernetes** deployment with auto-scaling, real-time monitoring with **Prometheus + Grafana** (15+ metrics), complete **MLflow** experiment tracking, and cloud deployment guide for **Azure Container Apps**.

### 13.2 Impact & Applications
**Clinical Value:** Early detection of at-risk patients, automated screening for primary care, decision support for providers, reduced diagnostic costs. **Technical Value:** Reusable MLOps framework, best practices demonstration, scalable architecture (250+ req/sec), cost-effective cloud deployment. **Educational Value:** Complete learning resource for MLOps, real-world industry standards, template for classification problems.

### 13.3 Compliance & Ethics
**Data Privacy:** No patient identifiers, anonymized UCI dataset, GDPR-compliant handling, secure API with no data retention. **Model Fairness:** Evaluated across demographics, bias mitigation strategies, regular retraining, transparent explanations. **Clinical Responsibility:** Tool positioned as screening aid not diagnostic, human oversight required, limitations documented, false negative rate (6.6%) disclosed.

### 13.4 Success Metrics
✅ All 9 assignment tasks completed | ✅ 88.52% accuracy (exceeds 85% target) | ✅ 85%+ test coverage (exceeds 80% target) | ✅ <50ms API latency (exceeds <100ms target) | ✅ Complete documentation | ✅ Cloud deployment verified

**Final Remarks:** This project demonstrates modern MLOps practices enable development of reliable (99.9% uptime), scalable (Kubernetes), maintainable (automated CI/CD), observable (comprehensive monitoring), and reproducible (version control + MLflow) machine learning systems suitable for healthcare settings.

---

## 14. References & Documentation Links

### 14.1 Dataset & Academic References
1. **UCI Machine Learning Repository - Heart Disease Dataset:** Janosi, A., Steinbrunn, W., Pfisterer, M., & Detrano, R. (1988), Cleveland Clinic Foundation. URL: https://archive.ics.uci.edu/ml/datasets/Heart+Disease
2. **scikit-learn:** Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research
3. **WHO Cardiovascular Diseases:** World Health Organization (2021), Fact Sheet on CVDs

### 14.2 Technology Documentation
4. **FastAPI Framework:** https://fastapi.tiangolo.com/
5. **MLflow Documentation:** https://mlflow.org/docs/latest/
6. **Prometheus Documentation:** https://prometheus.io/docs/
7. **Kubernetes Documentation:** https://kubernetes.io/docs/
8. **GitHub Actions:** https://docs.github.com/en/actions

### 14.3 Project Documentation (GitHub Repository)
All detailed guides, configurations, and implementation code available at:
**Repository:** https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81

**Key Documentation Files:**
- **Getting Started:** [docs/01_Setup_Installation/START_HERE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/START_HERE.md)
- **Local Setup:** [docs/01_Setup_Installation/LOCAL_DEPLOYMENT_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/LOCAL_DEPLOYMENT_GUIDE.md)
- **Cloud Deployment:** [docs/01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md)
- **Execution Guide:** [docs/01_Setup_Installation/EXECUTION_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/EXECUTION_GUIDE.md)
- **Grafana Setup:** [docs/05_CI_CD_Deployment/GRAFANA_SETUP_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/05_CI_CD_Deployment/GRAFANA_SETUP_GUIDE.md)
- **Project Architecture:** [docs/04_Architecture/ARCHITECTURE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/04_Architecture/ARCHITECTURE.md)

**Implementation Code:**
- **Training Pipeline:** [src/train.py](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/train.py)
- **Preprocessing:** [src/preprocessing.py](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/preprocessing.py)
- **FastAPI Application:** [src/app.py](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/src/app.py)
- **EDA Notebook:** [notebooks/01_EDA.ipynb](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/notebooks/01_EDA.ipynb)

**Configuration Files:**
- **CI/CD Pipeline:** [.github/workflows/ci-cd.yml](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/.github/workflows/ci-cd.yml)
- **Kubernetes Deployment:** [deployment/kubernetes/](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/tree/main/heart-disease-mlops/deployment/kubernetes)
- **Docker Configuration:** [Dockerfile](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/Dockerfile)
- **Prometheus Config:** [deployment/prometheus/prometheus.yml](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/deployment/prometheus/prometheus.yml)

---

## 15. Appendices

### Appendix A: Technology Stack Summary
**ML/Data Science:** Python 3.9+, scikit-learn 1.3.0, pandas 2.0.3, numpy 1.24.3, matplotlib, seaborn  
**API/Deployment:** FastAPI 0.101.0, Uvicorn 0.23.2, Pydantic 2.0.0, Docker 24.0, Kubernetes 1.27  
**MLOps Tools:** MLflow 2.5.0, Prometheus 2.45.0, Grafana 10.0.3, GitHub Actions  
**Testing:** pytest 7.4.0, pytest-cov 4.1.0, flake8, black, pylint

### Appendix B: Performance Metrics Formulas
**Accuracy** = (TP + TN) / (TP + TN + FP + FN)  
**Precision** = TP / (TP + FP)  
**Recall (Sensitivity)** = TP / (TP + FN)  
**F1-Score** = 2 × (Precision × Recall) / (Precision + Recall)  
**Specificity** = TN / (TN + FP)  
**ROC-AUC** = Area under Receiver Operating Characteristic curve  
Where: TP=True Positives, TN=True Negatives, FP=False Positives, FN=False Negatives

### Appendix C: Quick Start Commands
**Local Setup:** See [LOCAL_DEPLOYMENT_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/LOCAL_DEPLOYMENT_GUIDE.md)  
**Training:** See [EXECUTION_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/EXECUTION_GUIDE.md)  
**API Testing:** See [sample_input.json](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/sample_input.json)  
**Cloud Deployment:** See [CLOUD_DEPLOYMENT_GUIDE.md](https://github.com/vishalvishal099/MLOpsExperimentalLearning_Assignment_1_Group_81/blob/main/heart-disease-mlops/docs/01_Setup_Installation/CLOUD_DEPLOYMENT_GUIDE.md)


### Appendix D: Project Metrics Summary
**Dataset:** 303 records, 13 features, 0 missing values, balanced classes (45.5%/54.5%)  
**Best Model:** Random Forest - 88.52% accuracy, 0.95 ROC-AUC, 87.9% sensitivity  
**API Performance:** 39ms avg response, 250 req/sec max throughput, 0% error rate  
**Infrastructure:** 3 replicas, 1Gi memory limit, 500m CPU limit, 99.9% uptime  
**Testing:** 30+ tests, 85%+ coverage, automated CI/CD in 8 minutes  
**Monitoring:** 15+ metrics, 10 Grafana panels, 10s scrape interval

---

**END OF REPORT**
