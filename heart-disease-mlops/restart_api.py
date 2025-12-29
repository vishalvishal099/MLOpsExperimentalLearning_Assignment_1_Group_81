#!/usr/bin/env python3
"""
Restart API with enhanced metrics and update comprehensive tester
"""
import subprocess
import sys
import time
import requests
import os
import signal

def kill_processes():
    """Kill existing API and tester processes"""
    print("🛑 Stopping existing processes...")
    try:
        # Kill Python processes running the API
        subprocess.run(["pkill", "-f", "python src/app.py"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "comprehensive_api_tester"], stderr=subprocess.DEVNULL)
        time.sleep(2)
        print("✅ Processes stopped")
    except Exception as e:
        print(f"Note: {e}")

def install_psutil():
    """Install psutil"""
    print("\n📦 Installing psutil...")
    try:
        subprocess.run(
            ["pip", "install", "-q", "psutil==5.9.5"],
            check=True,
            capture_output=True
        )
        print("✅ psutil installed")
    except Exception as e:
        print(f"❌ Failed to install psutil: {e}")
        return False
    return True

def start_api():
    """Start the API in background"""
    print("\n🚀 Starting enhanced API...")
    try:
        # Change to project directory
        os.chdir("/Users/v0s01jh/Documents/BITS/MLOpsExperimentalLearning_Assignment_1_Group_81/heart-disease-mlops")
        
        # Start API in background
        with open("api_enhanced.log", "w") as log_file:
            process = subprocess.Popen(
                ["python", "src/app.py"],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONPATH": "."}
            )
        
        print(f"✅ API started (PID: {process.pid})")
        
        # Wait for API to be ready
        print("⏳ Waiting for API to be ready...")
        for i in range(10):
            time.sleep(1)
            try:
                response = requests.get("http://localhost:8000/health", timeout=2)
                if response.status_code == 200:
                    print("✅ API is ready!")
                    return True
            except:
                if i < 9:
                    print(f"   Waiting... ({i+1}/10)")
                continue
        
        print("❌ API did not start in time")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start API: {e}")
        return False

def test_new_features():
    """Test the new batch endpoint"""
    print("\n🧪 Testing new features...")
    
    # Test health with new metric
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health check: {response.json()['status']}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test batch endpoint
    try:
        batch_data = [
            {
                "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233,
                "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
                "oldpeak": 2.3, "slope": 3, "ca": 0, "thal": 6
            },
            {
                "age": 37, "sex": 1, "cp": 2, "trestbps": 130, "chol": 250,
                "fbs": 0, "restecg": 1, "thalach": 187, "exang": 0,
                "oldpeak": 3.5, "slope": 1, "ca": 0, "thal": 2
            }
        ]
        
        response = requests.post(
            "http://localhost:8000/predict/batch",
            json=batch_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Batch prediction: {result['count']} predictions in {result['batch_latency']:.3f}s")
        else:
            print(f"❌ Batch prediction failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Batch prediction test failed: {e}")
    
    # Check metrics
    try:
        response = requests.get("http://localhost:8000/metrics")
        metrics = response.text
        
        print("\n📊 New metrics available:")
        new_metrics = [
            "api_cpu_usage_percent",
            "api_memory_usage_bytes",
            "api_health_status",
            "http_requests_total",
            "batch_prediction_requests_total",
            "prediction_results_total",
            "prediction_risk_level_total"
        ]
        
        for metric in new_metrics:
            if metric in metrics:
                print(f"   ✅ {metric}")
            else:
                print(f"   ❌ {metric} - not found")
                
    except Exception as e:
        print(f"❌ Metrics check failed: {e}")

def main():
    print("="*70)
    print("🔄 API RESTART WITH ENHANCED METRICS")
    print("="*70)
    
    # Step 1: Kill existing processes
    kill_processes()
    
    # Step 2: Install psutil
    if not install_psutil():
        return 1
    
    # Step 3: Start API
    if not start_api():
        return 1
    
    # Step 4: Test new features
    test_new_features()
    
    # Summary
    print("\n" + "="*70)
    print("✅ API RESTART COMPLETE!")
    print("="*70)
    print("\n📊 Enhanced Metrics Now Available:")
    print("   • Average Prediction Time")
    print("   • Predictions by Class (0/1)")
    print("   • API Health Status (1=UP, 0=DOWN)")
    print("   • CPU Usage (%)")
    print("   • Memory Usage (bytes)")
    print("   • HTTP Requests by Method (GET/POST)")
    print("   • Endpoint-specific metrics (/predict, /predict/batch)")
    print("\n🚀 Next Steps:")
    print("   1. Run comprehensive tests:")
    print("      python comprehensive_api_tester.py")
    print("      Select option 6 (Extended Test)")
    print("\n   2. View Grafana dashboard:")
    print("      http://localhost:3000")
    print("      Dashboard: Heart Disease ML API Monitoring")
    print("\n   3. Check Prometheus metrics:")
    print("      http://localhost:9090")
    print("="*70 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
