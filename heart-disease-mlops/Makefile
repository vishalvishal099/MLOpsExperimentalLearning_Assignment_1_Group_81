.PHONY: help install clean test train api docker k8s monitor lint format

help:
	@echo "Heart Disease MLOps - Available Commands:"
	@echo ""
	@echo "  make install       - Install dependencies"
	@echo "  make data          - Download and prepare dataset"
	@echo "  make train         - Train models with MLflow"
	@echo "  make test          - Run all tests"
	@echo "  make api           - Start FastAPI server"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make docker-stop   - Stop Docker container"
	@echo "  make compose-up    - Start full stack (API + Monitoring)"
	@echo "  make compose-down  - Stop full stack"
	@echo "  make k8s-deploy    - Deploy to Kubernetes"
	@echo "  make k8s-delete    - Delete Kubernetes deployment"
	@echo "  make mlflow        - Start MLflow UI"
	@echo "  make lint          - Run code linting"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean temporary files"
	@echo ""

install:
	pip install --upgrade pip
	pip install -r requirements.txt

data:
	python src/download_data.py

train:
	python src/train.py

test:
	pytest tests/ -v --cov=src --cov-report=html

test-fast:
	pytest tests/ -v

api:
	uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

mlflow:
	mlflow ui --port 5000

docker-build:
	docker build -t heart-disease-api:latest .

docker-run:
	docker run -d --name heart-api -p 8000:8000 heart-disease-api:latest

docker-stop:
	docker stop heart-api || true
	docker rm heart-api || true

docker-logs:
	docker logs -f heart-api

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f

k8s-deploy:
	kubectl apply -f deployment/kubernetes/deployment.yaml

k8s-monitor:
	kubectl apply -f deployment/kubernetes/monitoring.yaml

k8s-delete:
	kubectl delete -f deployment/kubernetes/deployment.yaml
	kubectl delete -f deployment/kubernetes/monitoring.yaml

k8s-status:
	kubectl get pods
	kubectl get services

lint:
	flake8 src/ --max-line-length=127 --statistics
	pylint src/

format:
	black src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f api_logs.log

all: install data train test docker-build
	@echo "Complete setup finished!"
