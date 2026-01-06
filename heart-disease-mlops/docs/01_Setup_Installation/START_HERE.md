# 🚀 START HERE - Complete Deployment Guide


This is your **complete roadmap** for deploying the Heart Disease Prediction MLOps project. Follow the steps below : 

---

## 🎯 What Do You Want To Do?

### Option 1: 🏠 Run Locally 
**Perfect for:** Testing, development, understanding the project

👉 **Follow:** [`LOCAL_DEPLOYMENT_GUIDE.md`](./LOCAL_DEPLOYMENT_GUIDE.md)
    *API will be running on http://localhost:8000* 

---

### Option 2: ☁️ Deploy to Cloud 

👉 **Follow:** [`CLOUD_DEPLOYMENT_GUIDE.md`](./CLOUD_DEPLOYMENT_GUIDE.md)

---

### Option 3: 🔗  Test the API?

👉 **Follow:** [`ACCESS_INSTRUCTIONS.md`](./ACCESS_INSTRUCTIONS.md)

---

## 📚 Complete Step-by-Step Path

Follow these guides **in order** for the complete MLOps workflow:

```
1. LOCAL_DEPLOYMENT_GUIDE.md    ← Start here (Run locally first)
   ↓
2. CLOUD_DEPLOYMENT_GUIDE.md    ← Deploy to cloud (Get public URL)
   ↓
3. ACCESS_INSTRUCTIONS.md       ← Test everything (Verify it works)
   ↓
4. EXECUTION_GUIDE.md           ← Reference guide (Additional details)
```

---

## 📋 Summary of Available Guides

| Guide | Purpose |  
|-------|---------|
| **LOCAL_DEPLOYMENT_GUIDE.md** | Run on your computer |
| **CLOUD_DEPLOYMENT_GUIDE.md** | Deploy to internet | 
| **ACCESS_INSTRUCTIONS.md** | Test the API | 
| **EXECUTION_GUIDE.md** | Additional reference |


---

## 🚀 Quick Start Commands

### For Local Deployment:
```bash
cd heart-disease-mlops
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/download_data.py
python src/train.py
uvicorn src.app:app --reload
```

### For Cloud Deployment (Azure):
```bash
az login
az group create --name heart-disease-rg --location eastus
az acr create --name heartdiseaseacr --resource-group heart-disease-rg --sku Basic
az acr build --registry heartdiseaseacr --image heart-disease-api:v1 .
# ... (see CLOUD_DEPLOYMENT_GUIDE.md for complete steps)
```
---
