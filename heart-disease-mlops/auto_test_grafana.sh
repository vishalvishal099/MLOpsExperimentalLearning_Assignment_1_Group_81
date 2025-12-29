#!/bin/bash

# Auto-run script for comprehensive API testing
# Generates rich metrics for Grafana dashboard

cd /Users/v0s01jh/Documents/BITS/MLOpsExperimentalLearning_Assignment_1_Group_81/heart-disease-mlops
source venv/bin/activate

echo "🚀 Starting automated API testing for Grafana dashboard..."
echo ""
echo "This will run realistic traffic simulation for 10 minutes"
echo "to populate all Prometheus metrics and Grafana panels."
echo ""

# Run the comprehensive tester with option 6 (Extended Test)
python3 - <<'EOF'
import subprocess
import time

# Simulate selecting option 6 (Extended Test)
proc = subprocess.Popen(
    ["python", "comprehensive_api_tester.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Send option 6 for extended test
proc.stdin.write("6\n")
proc.stdin.flush()

# Wait for completion
try:
    stdout, stderr = proc.communicate(timeout=660)  # 11 minutes timeout
    print(stdout)
    if stderr:
        print("Errors:", stderr)
except subprocess.TimeoutExpired:
    proc.kill()
    stdout, stderr = proc.communicate()
    print(stdout)
    print("\n✅ Test completed!")

EOF

echo ""
echo "✅ Automated testing complete!"
echo ""
echo "📊 Now open Grafana to see the populated dashboard:"
echo "   http://localhost:3000"
echo ""
echo "Login: admin / admin"
echo "Dashboard: Heart Disease ML API Monitoring"
