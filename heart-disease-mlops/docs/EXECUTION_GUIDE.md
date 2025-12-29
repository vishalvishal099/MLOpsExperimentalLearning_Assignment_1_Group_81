# Step-by-Step Execution Guide

This guide provides detailed instructions to execute the complete MLOps pipeline from scratch.

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] Git installed
- [ ] Docker installed (optional, for containerization)
- [ ] Jupyter Notebook installed
- [ ] Terminal/Command Prompt access

---

## Phase 1: Project Setup (15 minutes)

### Step 1.1: Clone or Navigate to Project

```bash
# Navigate to the heart-disease-mlops project directory
cd heart-disease-mlops
```

### Step 1.2: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify activation
which python  # Should show path in venv folder
```

### Step 1.3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list | grep scikit-learn
pip list | grep mlflow
pip list | grep fastapi
```

**Expected Output**: All packages listed with versions

---

## Phase 2: Data Acquisition & EDA (30 minutes)

### Step 2.1: Download Dataset

```bash
python src/download_data.py
```

**Expected Output**:
```
================================================================================
Heart Disease Dataset Download Script
================================================================================

✓ Found local dataset at: raw_dataSet/heart+disease
  ✓ Copied: processed.cleveland.data
  ✓ Copied: cleveland.data
  ✓ Copied: heart-disease.names

✓ Dataset files copied successfully!
...
✓ DATASET PREPARATION COMPLETE!
```

### Step 2.2: Verify Data

```bash
# Check data files
ls -la data/processed/

# Expected files:
# heart_disease.csv
```

### Step 2.3: Run EDA Notebook

```bash
# Start Jupyter
jupyter notebook notebooks/01_EDA.ipynb
```

**In the notebook, execute all cells to:**
- Load and explore data
- Handle missing values
- Create visualizations
- Analyze correlations
- Check class balance

**Save notebook with outputs for documentation**

---

## Phase 3: Model Training with MLflow (45 minutes)

### Step 3.1: Start MLflow Tracking Server

Open a new terminal window:

```bash
# Navigate to project directory
cd heart-disease-mlops

# Activate venv
source venv/bin/activate

# Start MLflow
mlflow ui --port 5000
```

Keep this terminal running. Access MLflow UI at: http://localhost:5000

### Step 3.2: Train Models

Return to original terminal:

```bash
# Train all models
python src/train.py
```

**Expected Output**:
```
INFO - MLflow experiment: heart_disease_prediction
INFO - Training Logistic Regression...
INFO - Logistic Regression training complete!
INFO - Training Random Forest...
INFO - Random Forest training complete!
INFO - Training Gradient Boosting...
INFO - Gradient Boosting training complete!

================================================================================
MODEL COMPARISON
================================================================================

Logistic Regression:
  train_accuracy: 0.8512
  test_accuracy: 0.8525
  test_precision: 0.8410
  test_recall: 0.8370
  test_f1: 0.8390
  test_roc_auc: 0.9102
  cv_accuracy_mean: 0.8456
  cv_accuracy_std: 0.0234

Random Forest:
  train_accuracy: 1.0000
  test_accuracy: 0.8750
  test_precision: 0.8680
  test_recall: 0.8590
  test_f1: 0.8630
  test_roc_auc: 0.9405
  cv_accuracy_mean: 0.8598
  cv_accuracy_std: 0.0287
================================================================================
```

### Step 3.3: Review MLflow Experiments

1. Open http://localhost:5000
2. Click on "heart_disease_prediction" experiment
3. Review runs for each model
4. Compare metrics across models
5. View logged artifacts (plots, confusion matrices)

**Take screenshots for documentation**

### Step 3.4: Save Best Model

The training script automatically saves models to `models/` directory.

Verify:
```bash
ls -la models/

# Expected files:
# best_model.pkl
# preprocessor.pkl
```

---

## Phase 4: API Development & Testing (30 minutes)

### Step 4.1: Test Preprocessing Module

```bash
pytest tests/test_preprocessing.py -v
```

**Expected**: All tests pass ✓

### Step 4.2: Test Model Module

```bash
pytest tests/test_model.py -v
```

**Expected**: All tests pass ✓

### Step 4.3: Start API Server

```bash
# Start FastAPI server
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 4.4: Test API Endpoints

Open a new terminal:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true,
  "timestamp": "2024-XX-XXTXX:XX:XX"
}

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @sample_input.json

# Expected response:
{
  "prediction": 0 or 1,
  "probability": 0.XX,
  "risk_level": "Low|Medium|High",
  "timestamp": "2024-XX-XXTXX:XX:XX"
}
```

### Step 4.5: Test API Documentation

1. Open browser: http://localhost:8000/docs
2. Try the interactive API documentation
3. Test `/predict` endpoint with sample data
4. **Take screenshots**

### Step 4.6: Run API Tests

```bash
pytest tests/test_api.py -v
```

---

## Phase 5: Docker Containerization (20 minutes)

### Step 5.1: Build Docker Image

```bash
# Build image
docker build -t heart-disease-api:latest .

# This may take 3-5 minutes
```

**Expected Output**:
```
Successfully built <image_id>
Successfully tagged heart-disease-api:latest
```

### Step 5.2: Run Docker Container

```bash
# Run container
docker run -d --name heart-api -p 8000:8000 heart-disease-api:latest

# Check container status
docker ps

# View logs
docker logs heart-api
```

### Step 5.3: Test Dockerized API

```bash
# Health check
curl http://localhost:8000/health

# Prediction test
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @sample_input.json
```

**Take screenshots of successful responses**

### Step 5.4: Stop Container

```bash
docker stop heart-api
docker rm heart-api
```

---

## Phase 6: Full Stack with Monitoring (25 minutes)

### Step 6.1: Start Full Stack

```bash
# Start API + Prometheus + Grafana
docker-compose up -d

# Check status
docker-compose ps
```

**Expected**: All 3 services running

### Step 6.2: Access Services

1. **API**: http://localhost:8000/docs
2. **Prometheus**: http://localhost:9090
3. **Grafana**: http://localhost:3000 (admin/admin)

### Step 6.3: Configure Grafana

1. Login to Grafana (admin/admin)
2. Add Prometheus data source:
   - URL: http://prometheus:9090
   - Click "Save & Test"
3. Create dashboard with panels for:
   - Request count: `prediction_requests_total`
   - Average latency: `rate(prediction_latency_seconds_sum[5m])`
   - Predictions by class: `predictions_by_class`

**Take screenshots of dashboards**

### Step 6.4: Generate Traffic

```bash
# Run multiple predictions to generate metrics
for i in {1..10}; do
  curl -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d @sample_input.json
  sleep 1
done
```

Check Prometheus and Grafana for updated metrics.

### Step 6.5: Stop Full Stack

```bash
docker-compose down
```

---

## Phase 7: Kubernetes Deployment (Optional, 30 minutes)

### Step 7.1: Verify Kubernetes

```bash
# Check kubectl
kubectl version --client

# Check cluster (Docker Desktop Kubernetes)
kubectl cluster-info
```

### Step 7.2: Deploy Application

```bash
# Deploy
kubectl apply -f deployment/kubernetes/deployment.yaml

# Wait for pods to be ready (may take 2-3 minutes)
kubectl get pods -w

# Check deployment
kubectl get deployments
kubectl get services
```

### Step 7.3: Access Application

```bash
# Port forward
kubectl port-forward svc/heart-disease-api-service 8000:80

# In another terminal, test
curl http://localhost:8000/health
```

### Step 7.4: Deploy Monitoring

```bash
# Deploy Prometheus and Grafana
kubectl apply -f deployment/kubernetes/monitoring.yaml

# Check status
kubectl get pods

# Access Prometheus
kubectl port-forward svc/prometheus-service 9090:9090

# Access Grafana
kubectl port-forward svc/grafana-service 3000:3000
```

**Take screenshots of running pods and services**

### Step 7.5: Cleanup

```bash
# Delete deployments
kubectl delete -f deployment/kubernetes/deployment.yaml
kubectl delete -f deployment/kubernetes/monitoring.yaml
```

---

## Phase 8: CI/CD Setup (20 minutes)

### Step 8.1: Initialize Git Repository

```bash
# Initialize repo (if not already done)
git init

# Add files
git add .

# Commit
git commit -m "Initial commit - Complete MLOps pipeline"
```

### Step 8.2: Create GitHub Repository

1. Go to GitHub.com
2. Create new repository: `heart-disease-mlops`
3. Don't initialize with README (we have one)

### Step 8.3: Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/heart-disease-mlops.git

# Push
git push -u origin main
```

### Step 8.4: Verify GitHub Actions

1. Go to repository on GitHub
2. Click "Actions" tab
3. Workflow should start automatically
4. Monitor workflow execution
5. **Take screenshots** of successful workflow

---

## Phase 9: Documentation & Screenshots (30 minutes)

### Step 9.1: Take Required Screenshots

Capture screenshots for:

1. **EDA Notebook**
   - Data overview
   - Correlation heatmap
   - Distribution plots
   - Class balance

2. **MLflow UI**
   - Experiment runs
   - Metrics comparison
   - Logged artifacts

3. **API Documentation**
   - Swagger UI at /docs
   - Successful prediction response

4. **Docker**
   - Docker build output
   - Running container
   - Docker logs

5. **Kubernetes**
   - Running pods
   - Services
   - Deployment details

6. **Monitoring**
   - Prometheus metrics
   - Grafana dashboard

7. **CI/CD**
   - GitHub Actions workflow
   - Successful pipeline run
   - Test results

Save all screenshots to: `screenshots/` directory

### Step 9.2: Update README

Review and update README.md with:
- Your actual model performance metrics
- Your GitHub repository URL
- Any modifications you made

### Step 9.3: Create Video Demo

Record a short video (5-10 minutes) showing:
1. Project structure walkthrough
2. Running the API
3. Making predictions
4. Viewing MLflow experiments
5. Docker deployment
6. Monitoring dashboard

---

## Phase 10: Final Report (60 minutes)

Create a comprehensive report document (10 pages) covering:

### 1. Executive Summary (1 page)
- Project overview
- Key achievements
- Technologies used

### 2. Data Acquisition & EDA (1.5 pages)
- Dataset description
- Preprocessing steps
- EDA findings with visualizations

### 3. Model Development (2 pages)
- Feature engineering
- Models trained
- Hyperparameter tuning
- Cross-validation results
- Model comparison

### 4. Experiment Tracking (1 page)
- MLflow setup
- Experiments conducted
- Results tracking

### 5. Model Packaging & Reproducibility (0.5 pages)
- Model serialization
- Preprocessing pipeline
- Reproducibility measures

### 6. CI/CD Pipeline (1 page)
- Pipeline architecture
- Stages and jobs
- Automated testing
- Workflow screenshots

### 7. Containerization & Deployment (2 pages)
- Docker setup
- Kubernetes deployment
- Architecture diagram
- Deployment screenshots

### 8. Monitoring & Logging (0.5 pages)
- Prometheus metrics
- Grafana dashboards
- Logging strategy

### 9. Conclusion & Future Work (0.5 pages)
- Summary of achievements
- Challenges faced
- Future improvements

### 10. Appendix
- API documentation
- Code snippets
- Links and references

---

## Validation Checklist

Before submission, verify:

- [ ] All code runs without errors
- [ ] All tests pass
- [ ] Docker container builds and runs
- [ ] API endpoints work correctly
- [ ] MLflow experiments are logged
- [ ] Screenshots are captured
- [ ] README is complete
- [ ] Documentation is thorough
- [ ] GitHub repository is public/accessible
- [ ] CI/CD pipeline runs successfully
- [ ] Video demo is recorded
- [ ] Final report is complete (10 pages)

---

## Troubleshooting Common Issues

### Issue: Module not found errors
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port already in use
```bash
# Solution: Use different port
uvicorn src.app:app --port 8001
```

### Issue: Docker build fails
```bash
# Solution: Clear cache and rebuild
docker system prune -a
docker build --no-cache -t heart-disease-api:latest .
```

### Issue: Kubernetes pods not starting
```bash
# Solution: Check pod status
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

---

## Time Estimates

| Phase | Estimated Time |
|-------|----------------|
| Project Setup | 15 min |
| Data & EDA | 30 min |
| Model Training | 45 min |
| API Development | 30 min |
| Docker | 20 min |
| Monitoring | 25 min |
| Kubernetes | 30 min |
| CI/CD | 20 min |
| Documentation | 30 min |
| Final Report | 60 min |
| **Total** | **~5 hours** |

---

## Next Steps After Completion

1. Share GitHub repository link
2. Submit final report
3. Upload video demonstration
4. Prepare for presentation/demo
5. Document lessons learned

---

**Good luck with your MLOps project! 🚀**
