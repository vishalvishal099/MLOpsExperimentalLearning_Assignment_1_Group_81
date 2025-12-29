#!/bin/bash

# Script to import the enhanced dashboard into Grafana

GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASS="admin"
DASHBOARD_FILE="deployment/grafana/dashboards/enhanced_dashboard.json"

echo "======================================================================"
echo "📊 IMPORTING ENHANCED DASHBOARD TO GRAFANA"
echo "======================================================================"

# Check if Grafana is running
if ! curl -s "$GRAFANA_URL/api/health" > /dev/null 2>&1; then
    echo "❌ Grafana is not running at $GRAFANA_URL"
    echo "Please start Grafana first: brew services start grafana"
    exit 1
fi

echo "✅ Grafana is running"

# Import the dashboard
echo "📥 Importing dashboard..."

RESPONSE=$(curl -s -X POST "$GRAFANA_URL/api/dashboards/db" \
  -u "$GRAFANA_USER:$GRAFANA_PASS" \
  -H "Content-Type: application/json" \
  -d @"$DASHBOARD_FILE")

if echo "$RESPONSE" | grep -q '"status":"success"'; then
    DASHBOARD_URL=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['url'])" 2>/dev/null || echo "/d/heart-disease-ml")
    echo "✅ Dashboard imported successfully!"
    echo ""
    echo "🔗 Access your dashboard at:"
    echo "   $GRAFANA_URL$DASHBOARD_URL"
    echo ""
    echo "📊 The dashboard includes:"
    echo "   ✓ API Health Status"
    echo "   ✓ CPU Usage (gauge)"
    echo "   ✓ Memory Usage (gauge)"
    echo "   ✓ HTTP Requests by Method"
    echo "   ✓ Average Prediction Time"
    echo "   ✓ Predictions by Class (pie chart)"
    echo "   ✓ Predictions by Risk Level (donut chart)"
    echo "   ✓ Batch Prediction Metrics"
    echo "   ✓ Endpoint Latency Distribution"
    echo "   ✓ HTTP Status Codes"
    echo ""
else
    echo "❌ Failed to import dashboard"
    echo "Response: $RESPONSE"
    exit 1
fi
