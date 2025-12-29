# ☁️ Cloud Deployment Guide - Complete Beginner's Guide

## 🎯 Overview

This guide will teach you **step-by-step** how to deploy your Heart Disease Prediction MLOps project to the cloud, even if you've never done it before.

We'll cover **three popular cloud platforms** with complete instructions.

---

## 📋 Table of Contents

1. [Choose Your Cloud Platform](#choose-your-cloud-platform)
2. [Option A: Azure Container Apps (Recommended - Easiest)](#option-a-azure-container-apps)
3. [Option B: AWS (Amazon Web Services)](#option-b-aws-elastic-container-service)
4. [Option C: Google Cloud Platform](#option-c-google-cloud-run)
5. [Setup CI/CD Pipeline with GitHub Actions](#setup-cicd-pipeline)
6. [Testing Your Cloud Deployment](#testing-your-cloud-deployment)

---

## 🤔 Choose Your Cloud Platform

| Platform | Difficulty | Free Tier | Best For | Cost (Est.) |
|----------|-----------|-----------|----------|-------------|
| **Azure Container Apps** | ⭐ Easy | Yes ($200 credit) | Beginners, Quick setup | $5-10/month |
| **AWS ECS** | ⭐⭐ Medium | Yes (12 months) | AWS users | $5-15/month |
| **Google Cloud Run** | ⭐ Easy | Yes ($300 credit) | Pay-per-use | $3-8/month |

**Recommendation for Beginners:** Start with **Azure Container Apps** or **Google Cloud Run**

---

## 🔵 Option A: Azure Container Apps (RECOMMENDED)

### Why Azure Container Apps?
- ✅ Easiest to set up
- ✅ Automatic HTTPS
- ✅ Built-in CI/CD
- ✅ $200 free credit for students
- ✅ No server management

---

### Step 1: Create Azure Account

1. Go to: [azure.microsoft.com/free/students](https://azure.microsoft.com/free/students)
2. Click "Start Free" or "Activate Now"
3. Sign in with your school email
4. Complete verification (you'll get $200 credit)
5. Access Azure Portal: [portal.azure.com](https://portal.azure.com)

**Note:** Students get $100-200 free credit (no credit card required for students)

---

### Step 2: Install Azure CLI

#### For macOS:
```bash
brew install azure-cli
```

#### For Windows:
Download from: [aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows)

#### For Linux:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

#### Verify Installation:
```bash
az --version
```

---

### Step 3: Login to Azure

```bash
# Login
az login

# Set your subscription (if you have multiple)
az account list --output table
az account set --subscription "Your-Subscription-Name"

# Verify
az account show
```

---

### Step 4: Create Resource Group

```bash
# Create a resource group (like a folder for your resources)
az group create \
  --name heart-disease-rg \
  --location eastus

# Verify
az group list --output table
```

**Choose a location near you:**
- US: `eastus`, `westus2`
- Europe: `westeurope`, `northeurope`
- Asia: `southeastasia`, `eastasia`

---

### Step 5: Create Container Registry (To Store Your Docker Image)

```bash
# Create Azure Container Registry
az acr create \
  --resource-group heart-disease-rg \
  --name heartdiseaseacr \
  --sku Basic \
  --admin-enabled true

# Login to registry
az acr login --name heartdiseaseacr

# Get login server
az acr show --name heartdiseaseacr --query loginServer --output table
```

**Note:** Registry name must be globally unique. If taken, try: `heartdiseaseacr123`, `hdacr2024`, etc.

---

### Step 6: Build and Push Docker Image to Azure

```bash
# Navigate to your project
cd heart-disease-mlops

# Build and push in one command (Azure will do it for you!)
az acr build \
  --registry heartdiseaseacr \
  --image heart-disease-api:v1 \
  --file Dockerfile \
  .

# This will take 3-5 minutes
# Azure builds your Docker image in the cloud!
```

**Expected Output:**
```
Successfully tagged heartdiseaseacr.azurecr.io/heart-disease-api:v1
Successfully pushed heartdiseaseacr.azurecr.io/heart-disease-api:v1
```

---

### Step 7: Create Container App Environment

```bash
# Install Container Apps extension
az extension add --name containerapp --upgrade

# Register providers
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# Create environment (like a hosting space)
az containerapp env create \
  --name heart-disease-env \
  --resource-group heart-disease-rg \
  --location eastus
```

---

### Step 8: Deploy Your Container App

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name heartdiseaseacr --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name heartdiseaseacr --query passwords[0].value --output tsv)

# Deploy the container app
az containerapp create \
  --name heart-disease-api \
  --resource-group heart-disease-rg \
  --environment heart-disease-env \
  --image heartdiseaseacr.azurecr.io/heart-disease-api:v1 \
  --registry-server heartdiseaseacr.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 0.5 \
  --memory 1Gi

# Get the URL
az containerapp show \
  --name heart-disease-api \
  --resource-group heart-disease-rg \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

**You'll get a URL like:** `https://heart-disease-api.azurecontainerapps.io`

---

### Step 9: Test Your Cloud API

```bash
# Replace with your actual URL
export API_URL="https://heart-disease-api.azurecontainerapps.io"

# Test health endpoint
curl $API_URL/health

# Test prediction
curl -X POST "$API_URL/predict" \
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
    "slope": 0,
    "ca": 0,
    "thal": 1
  }'

# Open in browser
open "$API_URL/docs"
```

✅ **Your API is now live on the internet!**

---

### Step 10: View Logs and Monitor

```bash
# View logs
az containerapp logs show \
  --name heart-disease-api \
  --resource-group heart-disease-rg \
  --follow

# Check metrics in Azure Portal
# Go to: portal.azure.com → Resource Groups → heart-disease-rg → heart-disease-api
```

---

## 🟠 Option B: AWS Elastic Container Service

### Prerequisites
- AWS Account (12-month free tier)
- AWS CLI installed

---

### Step 1: Create AWS Account

1. Go to: [aws.amazon.com/free](https://aws.amazon.com/free)
2. Click "Create a Free Account"
3. Complete registration (credit card required but won't be charged for free tier)
4. Sign in to AWS Console: [console.aws.amazon.com](https://console.aws.amazon.com)

---

### Step 2: Install AWS CLI

#### macOS:
```bash
brew install awscli
```

#### Windows:
Download from: [aws.amazon.com/cli](https://aws.amazon.com/cli)

#### Linux:
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

---

### Step 3: Configure AWS CLI

```bash
# Configure AWS credentials
aws configure

# You'll be asked for:
# AWS Access Key ID: (Get from AWS Console → IAM → Users → Security credentials)
# AWS Secret Access Key: (Get from same place)
# Default region name: us-east-1
# Default output format: json
```

---

### Step 4: Create ECR Repository

```bash
# Create Elastic Container Registry
aws ecr create-repository \
  --repository-name heart-disease-api \
  --region us-east-1

# Get login command
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Get your account ID
aws sts get-caller-identity --query Account --output text
```

---

### Step 5: Build and Push Docker Image

```bash
# Build image
docker build -t heart-disease-api .

# Tag image
docker tag heart-disease-api:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api:latest
```

---

### Step 6: Create ECS Cluster

```bash
# Create cluster
aws ecs create-cluster --cluster-name heart-disease-cluster
```

---

### Step 7: Create Task Definition

Create a file: `task-definition.json`

```json
{
  "family": "heart-disease-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "heart-disease-api",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/heart-disease-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/heart-disease-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

---

### Step 8: Create Service and Deploy

```bash
# Create service (this makes it accessible)
aws ecs create-service \
  --cluster heart-disease-cluster \
  --service-name heart-disease-service \
  --task-definition heart-disease-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"
```

**Note:** You'll need to create VPC, subnets, and security groups first. See AWS documentation.

---

## 🔴 Option C: Google Cloud Run (EASIEST!)

### Step 1: Create Google Cloud Account

1. Go to: [cloud.google.com/free](https://cloud.google.com/free)
2. Click "Get started for free"
3. Sign in with Google account
4. Get $300 free credit (credit card required but won't be charged)

---

### Step 2: Install Google Cloud CLI

#### macOS:
```bash
brew install google-cloud-sdk
```

#### Windows/Linux:
Download from: [cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

---

### Step 3: Initialize and Login

```bash
# Initialize gcloud
gcloud init

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

---

### Step 4: Enable APIs

```bash
# Enable required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  containerregistry.googleapis.com
```

---

### Step 5: Build and Deploy (ONE COMMAND!)

```bash
# Navigate to project
cd heart-disease-mlops

# Build and deploy in one command!
gcloud run deploy heart-disease-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000

# This will:
# 1. Build your Docker image
# 2. Push to Google Container Registry
# 3. Deploy to Cloud Run
# 4. Give you a public URL!
```

**Expected Output:**
```
Service [heart-disease-api] revision [heart-disease-api-00001] has been deployed.
Service URL: https://heart-disease-api-xxxxx-uc.a.run.app
```

✅ **That's it! Your API is live!**

---

### Step 6: Test Your Google Cloud API

```bash
# Get service URL
gcloud run services describe heart-disease-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'

# Test it
curl https://heart-disease-api-xxxxx-uc.a.run.app/health
```

---

## 🔄 Setup CI/CD Pipeline with GitHub Actions

### Step 1: Create GitHub Repository

```bash
# Initialize git (if not already done)
cd heart-disease-mlops
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR_USERNAME/heart-disease-mlops.git
git branch -M main
git push -u origin main
```

---

### Step 2: Setup GitHub Secrets

Go to: **GitHub Repository → Settings → Secrets and variables → Actions**

#### For Azure:
Add these secrets:
- `AZURE_CREDENTIALS` (Get from: `az ad sp create-for-rbac --name "github-actions" --role contributor --scopes /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/heart-disease-rg --sdk-auth`)
- `AZURE_REGISTRY_NAME`: `heartdiseaseacr`
- `AZURE_REGISTRY_USERNAME`: (From Azure portal)
- `AZURE_REGISTRY_PASSWORD`: (From Azure portal)

#### For AWS:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_ACCOUNT_ID`

#### For Google Cloud:
- `GCP_PROJECT_ID`
- `GCP_SA_KEY` (Service account key JSON)

---

### Step 3: Create GitHub Actions Workflow

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: CI/CD Pipeline - Azure Deployment

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint with flake8
      run: |
        flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Run tests
      run: |
        pytest tests/ -v --cov=src
    
  build-and-deploy:
    name: Build and Deploy to Azure
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Azure Login
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Build and push image to ACR
      run: |
        az acr build \
          --registry ${{ secrets.AZURE_REGISTRY_NAME }} \
          --image heart-disease-api:${{ github.sha }} \
          --image heart-disease-api:latest \
          --file Dockerfile \
          .
    
    - name: Deploy to Azure Container Apps
      run: |
        az containerapp update \
          --name heart-disease-api \
          --resource-group heart-disease-rg \
          --image ${{ secrets.AZURE_REGISTRY_NAME }}.azurecr.io/heart-disease-api:${{ github.sha }}
    
    - name: Verify Deployment
      run: |
        URL=$(az containerapp show \
          --name heart-disease-api \
          --resource-group heart-disease-rg \
          --query properties.configuration.ingress.fqdn \
          --output tsv)
        
        echo "Testing health endpoint..."
        curl -f https://$URL/health || exit 1
        
        echo "✅ Deployment successful!"
        echo "API URL: https://$URL"
```

---

### Step 4: Push and Watch CI/CD in Action

```bash
# Make a change
echo "# Test CI/CD" >> README.md

# Commit and push
git add .
git commit -m "Test CI/CD pipeline"
git push origin main

# Go to GitHub → Actions tab to watch the magic happen!
```

**What happens:**
1. ✅ Code is checked out
2. ✅ Tests run automatically
3. ✅ Docker image is built
4. ✅ Image is pushed to container registry
5. ✅ Application is deployed to cloud
6. ✅ Health check verifies deployment

---

## 🧪 Testing Your Cloud Deployment

### Test Health Endpoint
```bash
curl https://YOUR_CLOUD_URL/health
```

### Test Prediction Endpoint
```bash
curl -X POST "https://YOUR_CLOUD_URL/predict" \
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
    "slope": 0,
    "ca": 0,
    "thal": 1
  }'
```

### Test in Browser
Open: `https://YOUR_CLOUD_URL/docs`

### Test with Python
```python
import requests

API_URL = "https://YOUR_CLOUD_URL"

# Health check
response = requests.get(f"{API_URL}/health")
print("Health:", response.json())

# Prediction
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
    "slope": 0,
    "ca": 0,
    "thal": 1
}

response = requests.post(f"{API_URL}/predict", json=data)
print("Prediction:", response.json())
```

---

## 💰 Cost Management

### Azure
```bash
# Check costs
az consumption usage list --output table

# Set up budget alert
az consumption budget create \
  --budget-name monthly-budget \
  --amount 10 \
  --time-grain Monthly
```

### Stop Services When Not Needed
```bash
# Azure
az containerapp update --name heart-disease-api \
  --resource-group heart-disease-rg \
  --min-replicas 0

# AWS
aws ecs update-service --cluster heart-disease-cluster \
  --service heart-disease-service \
  --desired-count 0

# Google Cloud
gcloud run services update heart-disease-api \
  --region us-central1 \
  --min-instances 0
```

---

## 📸 Screenshots for Assignment Submission

Take screenshots of:

1. ✅ **Cloud Console** showing deployed resources
2. ✅ **Public URL** working in browser
3. ✅ **Swagger UI** accessible via cloud URL
4. ✅ **Successful prediction** response
5. ✅ **GitHub Actions** workflow running successfully
6. ✅ **Cloud monitoring/logs** showing API requests
7. ✅ **Resource group/project** overview
8. ✅ **Cost/billing** page (showing free tier usage)

---

## 🎓 Assignment Checklist

For your MLOps assignment, ensure you have:

- [ ] Application deployed to cloud with public URL
- [ ] CI/CD pipeline configured and working
- [ ] API documentation accessible online
- [ ] Health endpoint returning successful response
- [ ] Prediction endpoint working with sample data
- [ ] Screenshots of all components
- [ ] Public URL shared in documentation
- [ ] GitHub repository with CI/CD workflow
- [ ] Monitoring/logging configured
- [ ] Cost optimization implemented

---

## 🆘 Troubleshooting

### Deployment Failed
```bash
# Check logs (Azure)
az containerapp logs show --name heart-disease-api \
  --resource-group heart-disease-rg --follow

# Check logs (Google Cloud)
gcloud run logs read --service heart-disease-api

# Check logs (AWS)
aws logs tail /ecs/heart-disease-api --follow
```

### Image Build Failed
- Check Dockerfile syntax
- Ensure all files are included
- Check Docker build logs

### Can't Access API
- Check if ingress is enabled
- Verify firewall/security group rules
- Check if service is running

### CI/CD Not Triggering
- Check GitHub secrets are set correctly
- Verify workflow file syntax
- Check branch name in workflow

---

## 📚 Additional Resources

- [Azure Container Apps Docs](https://learn.microsoft.com/en-us/azure/container-apps/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Google Cloud Run Docs](https://cloud.google.com/run/docs)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 🎉 Success!

If you've followed this guide, you now have:
- ✅ Your ML model deployed to the cloud
- ✅ A public URL anyone can access
- ✅ Automatic CI/CD pipeline
- ✅ Professional MLOps setup

**Share your public API URL in your assignment submission!**

---

**Last Updated:** December 30, 2025  
**Need help with local deployment?** See `LOCAL_DEPLOYMENT_GUIDE.md`
