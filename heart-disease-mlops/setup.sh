#!/bin/bash

# Heart Disease MLOps Project - Setup Script

echo "========================================"
echo "Heart Disease MLOps - Setup Script"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "\n${YELLOW}Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create necessary directories
echo -e "\n${YELLOW}Creating project directories...${NC}"
mkdir -p data/raw data/processed models logs mlruns screenshots

# Download and prepare data
echo -e "\n${YELLOW}Downloading and preparing dataset...${NC}"
python src/download_data.py

# Run tests
echo -e "\n${YELLOW}Running tests...${NC}"
pytest tests/ -v

# Setup complete
echo -e "\n${GREEN}========================================"
echo "Setup Complete!"
echo "========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Explore data: jupyter notebook notebooks/01_EDA.ipynb"
echo "3. Train models: python src/train.py"
echo "4. Start API: uvicorn src.app:app --reload"
echo "5. View API docs: http://localhost:8000/docs"
echo ""
echo "For Docker deployment:"
echo "  docker build -t heart-disease-api ."
echo "  docker run -p 8000:8000 heart-disease-api"
echo ""
echo "For full stack with monitoring:"
echo "  docker-compose up -d"
echo ""
