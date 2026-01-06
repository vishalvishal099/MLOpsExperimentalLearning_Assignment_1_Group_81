# Quick Reference Card - Heart Disease MLOps

## 🚀 Common Commands

### Setup & Installation
```bash
# Initial setup
./setup.sh

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Data & Training
```bash
# Download data
python src/download_data.py

# Train models
python src/train.py

# View MLflow
mlflow ui --port 5000
```

### API Operations
```bash
# Start API
uvicorn src.app:app --reload

# Test health
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @sample_input.json
```

### Testing
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src --cov-report=html

# Specific test file
pytest tests/test_api.py -v
```

### Docker Commands
```bash
# Build image
docker build -t heart-disease-api:latest .

# Run container
docker run -d -p 8000:8000 --name heart-api heart-disease-api:latest

# View logs
docker logs -f heart-api

# Stop container
docker stop heart-api && docker rm heart-api

# Full stack
docker-compose up -d
docker-compose down
```

### Kubernetes Commands
```bash
# Deploy application
kubectl apply -f deployment/kubernetes/deployment.yaml

# Check status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f <pod-name>

# Port forward
kubectl port-forward svc/heart-disease-api-service 8000:80

# Delete deployment
kubectl delete -f deployment/kubernetes/deployment.yaml
```

### Code Quality
```bash
# Lint code
flake8 src/ --max-line-length=127

# Format code
black src/ tests/

# Type checking (if using mypy)
mypy src/
```

---

## 📁 Important File Locations

| Component | Location |
|-----------|----------|
| API Code | `src/app.py` |
| Training | `src/train.py` |
| Preprocessing | `src/preprocessing.py` |
| Tests | `tests/` |
| Models | `models/` |
| Data | `data/processed/` |
| Notebooks | `notebooks/` |
| Docker | `Dockerfile` |
| K8s Manifests | `deployment/kubernetes/` |
| CI/CD | `.github/workflows/ci-cd.yml` |
| Documentation | `docs/` |

---

## 🌐 Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| API Documentation | http://localhost:8000/docs | - |
| MLflow UI | http://localhost:5000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin/admin |

---

## 📊 API Request Examples

### Health Check
```bash
curl http://localhost:8000/health
```

### Single Prediction
```bash
curl -X POST http://localhost:8000/predict \
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

### Using Python
```python
import requests

url = "http://localhost:8000/predict"
data = {
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

response = requests.post(url, json=data)
print(response.json())
```

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Docker Issues
```bash
# Clear everything
docker system prune -a

# Rebuild without cache
docker build --no-cache -t heart-disease-api:latest .
```

### Python Import Errors
```bash
# Add src to path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or reinstall
pip install -e .
```

### Model Not Found
```bash
# Train models
python src/train.py

# Check models directory
ls -la models/
```

---

## 📝 Project Structure Quick View

```
heart-disease-mlops/
├── src/              # Source code
├── tests/            # Unit tests
├── notebooks/        # Jupyter notebooks
├── models/           # Trained models
├── data/             # Datasets
├── deployment/       # K8s manifests
├── docs/             # Documentation
├── .github/          # CI/CD workflows
└── screenshots/      # Screenshots
```

---

## ⚡ Make Commands

```bash
make help           # Show all commands
make install        # Install dependencies
make data           # Download data
make train          # Train models
make test           # Run tests
make api            # Start API
make docker-build   # Build Docker image
make docker-run     # Run Docker container
make compose-up     # Start full stack
make k8s-deploy     # Deploy to K8s
make clean          # Clean temporary files
```

---

## 📋 Pre-Submission Checklist

- [ ] All code runs without errors
- [ ] All tests pass (`make test`)
- [ ] Docker image builds (`make docker-build`)
- [ ] API works (`make api`)
- [ ] MLflow experiments tracked
- [ ] Screenshots captured
- [ ] Documentation complete
- [ ] GitHub repository ready
- [ ] Video demo recorded
- [ ] Final report written

---

## 🆘 Getting Help

1. Check documentation in `docs/`
2. Review `EXECUTION_GUIDE.md`
3. Check API docs at `/docs`
4. Review error logs
5. Consult `ARCHITECTURE.md`

---

## 📞 Quick Links

- [README](README.md) - Project overview
- [Execution Guide](docs/EXECUTION_GUIDE.md) - Step-by-step instructions
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Deployment details
- [Architecture](docs/ARCHITECTURE.md) - System architecture
- [Project Summary](PROJECT_SUMMARY.md) - Complete summary

---

**Last Updated:** December 2024
**Version:** 1.0.0
