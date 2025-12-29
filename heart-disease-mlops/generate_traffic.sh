#!/bin/bash

echo "=========================================="
echo "Generating Traffic for Dashboard Testing"
echo "=========================================="
echo ""

API_URL="http://localhost:8000"

# Check if API is running
if ! curl -s $API_URL/health > /dev/null; then
    echo "❌ API is not running!"
    echo "Please start it first."
    exit 1
fi

echo "✅ API is running"
echo ""

# Function to make a prediction with random data
make_prediction() {
    AGE=$((40 + RANDOM % 40))
    SEX=$((RANDOM % 2))
    CP=$((1 + RANDOM % 4))
    TRESTBPS=$((120 + RANDOM % 60))
    CHOL=$((150 + RANDOM % 200))
    FBS=$((RANDOM % 2))
    RESTECG=$((RANDOM % 3))
    THALACH=$((100 + RANDOM % 100))
    EXANG=$((RANDOM % 2))
    OLDPEAK=$(echo "scale=1; $((RANDOM % 60)) / 10" | bc)
    SLOPE=$((1 + RANDOM % 3))
    CA=$((RANDOM % 4))
    THAL=$((1 + RANDOM % 3 + 5))  # 6, 7, or 3

    curl -s -X POST $API_URL/predict \
      -H "Content-Type: application/json" \
      -d "{
        \"age\": $AGE,
        \"sex\": $SEX,
        \"cp\": $CP,
        \"trestbps\": $TRESTBPS,
        \"chol\": $CHOL,
        \"fbs\": $FBS,
        \"restecg\": $RESTECG,
        \"thalach\": $THALACH,
        \"exang\": $EXANG,
        \"oldpeak\": $OLDPEAK,
        \"slope\": $SLOPE,
        \"ca\": $CA,
        \"thal\": $THAL
      }" | jq -r '.prediction, .risk_level' | xargs echo "Prediction:"
}

# Generate traffic
echo "📊 Generating 50 predictions..."
echo ""

for i in {1..50}; do
    echo -n "[$i/50] "
    make_prediction
    sleep 2
done

echo ""
echo "✅ Traffic generation complete!"
echo ""
echo "📈 View metrics at:"
echo "  • Grafana Dashboard: http://localhost:3000"
echo "  • Prometheus: http://localhost:9090"
echo "  • Raw Metrics: http://localhost:8000/metrics"
echo ""
