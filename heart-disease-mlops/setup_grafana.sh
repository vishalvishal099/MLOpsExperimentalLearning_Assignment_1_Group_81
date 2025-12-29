#!/bin/bash

echo "=========================================="
echo "Grafana Dashboard Setup Script"
echo "=========================================="
echo ""

# Check if Grafana is running
if ! curl -s http://localhost:3000/api/health > /dev/null; then
    echo "❌ Grafana is not running!"
    echo "Please start it with: brew services start grafana"
    exit 1
fi

echo "✅ Grafana is running at http://localhost:3000"
echo ""

# Wait for Grafana to be fully ready
sleep 2

# Add Prometheus data source
echo "📊 Adding Prometheus data source..."
curl -X POST http://admin:admin@localhost:3000/api/datasources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Prometheus",
    "type": "prometheus",
    "url": "http://localhost:9090",
    "access": "proxy",
    "isDefault": true
  }' 2>/dev/null

echo ""
echo ""

# Import dashboard
echo "📈 Importing Heart Disease API Dashboard..."
DASHBOARD_JSON=$(cat deployment/grafana/dashboard.json)
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d "{
    \"dashboard\": $DASHBOARD_JSON,
    \"overwrite\": true
  }" 2>/dev/null

echo ""
echo ""
echo "=========================================="
echo "✨ Setup Complete!"
echo "=========================================="
echo ""
echo "🌐 Access URLs:"
echo "  • Grafana:    http://localhost:3000"
echo "  • Prometheus: http://localhost:9090"
echo "  • API:        http://localhost:8000"
echo ""
echo "🔐 Grafana Login:"
echo "  • Username: admin"
echo "  • Password: admin"
echo ""
echo "📊 Dashboard:"
echo "  • Go to: Dashboards → Browse"
echo "  • Select: Heart Disease Prediction API Dashboard"
echo ""
echo "🧪 Generate Traffic:"
echo "  Run: ./generate_traffic.sh"
echo ""
