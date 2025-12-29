#!/bin/bash

echo "🔄 Restarting API with enhanced metrics..."

# Stop existing processes
echo "Stopping existing API and tester..."
pkill -f "python src/app.py"
pkill -f "comprehensive_api_tester"
sleep 2

# Navigate to project directory
cd /Users/v0s01jh/Documents/BITS/MLOpsExperimentalLearning_Assignment_1_Group_81/heart-disease-mlops

# Activate virtual environment
source venv/bin/activate

# Install psutil
echo "Installing psutil..."
pip install -q psutil==5.9.5

# Start API
echo "Starting enhanced API..."
PYTHONPATH=. python src/app.py > api_restart.log 2>&1 &
API_PID=$!

# Wait for API to start
echo "Waiting for API to be ready..."
sleep 5

# Check if API is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API is running (PID: $API_PID)"
    echo ""
    echo "📊 Enhanced metrics now available:"
    echo "   - Average Prediction Time"
    echo "   - Predictions by Class"
    echo "   - API Health Status"
    echo "   - CPU Usage"
    echo "   - Memory Usage"
    echo "   - HTTP Requests by Method"
    echo "   - /predict endpoint metrics"
    echo "   - /predict/batch endpoint metrics"
    echo ""
    echo "🧪 Test the batch endpoint:"
    echo '   curl -X POST http://localhost:8000/predict/batch \'
    echo '     -H "Content-Type: application/json" \'
    echo '     -d'"'"'[
        {"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 3, "ca": 0, "thal": 6},
        {"age": 37, "sex": 1, "cp": 2, "trestbps": 130, "chol": 250, "fbs": 0, "restecg": 1, "thalach": 187, "exang": 0, "oldpeak": 3.5, "slope": 1, "ca": 0, "thal": 2}
      ]'"'"
    echo ""
    echo "🚀 Run comprehensive tests:"
    echo "   python comprehensive_api_tester.py"
    echo "   Then select option 6 for Extended Test"
    echo ""
else
    echo "❌ API failed to start. Check api_restart.log for errors"
    tail -20 api_restart.log
fi
