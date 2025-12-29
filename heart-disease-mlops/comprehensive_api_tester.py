#!/usr/bin/env python3
"""
Comprehensive API Tester for Heart Disease ML API
Generates realistic traffic to populate Prometheus metrics and Grafana dashboard
"""

import requests
import time
import random
import json
from datetime import datetime
from typing import Dict, List
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# API Configuration
API_BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict"
METRICS_ENDPOINT = f"{API_BASE_URL}/metrics"

# Test Data - Diverse patient profiles
PATIENT_PROFILES = [
    {
        "name": "High Risk Patient 1",
        "data": {"age": 67, "sex": 1, "cp": 4, "trestbps": 160, "chol": 286, "fbs": 0, "restecg": 2, "thalach": 108, "exang": 1, "oldpeak": 1.5, "slope": 2, "ca": 3, "thal": 3},
        "expected_risk": "High"
    },
    {
        "name": "High Risk Patient 2",
        "data": {"age": 62, "sex": 1, "cp": 4, "trestbps": 150, "chol": 244, "fbs": 1, "restecg": 1, "thalach": 154, "exang": 1, "oldpeak": 1.4, "slope": 2, "ca": 2, "thal": 3},
        "expected_risk": "High"
    },
    {
        "name": "Medium Risk Patient 1",
        "data": {"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0, "oldpeak": 2.3, "slope": 3, "ca": 0, "thal": 6},
        "expected_risk": "Medium"
    },
    {
        "name": "Medium Risk Patient 2",
        "data": {"age": 56, "sex": 1, "cp": 2, "trestbps": 130, "chol": 256, "fbs": 1, "restecg": 2, "thalach": 142, "exang": 1, "oldpeak": 0.6, "slope": 2, "ca": 1, "thal": 6},
        "expected_risk": "Medium"
    },
    {
        "name": "Low Risk Patient 1",
        "data": {"age": 37, "sex": 1, "cp": 2, "trestbps": 130, "chol": 250, "fbs": 0, "restecg": 1, "thalach": 187, "exang": 0, "oldpeak": 3.5, "slope": 1, "ca": 0, "thal": 2},
        "expected_risk": "Low"
    },
    {
        "name": "Low Risk Patient 2",
        "data": {"age": 41, "sex": 0, "cp": 1, "trestbps": 130, "chol": 204, "fbs": 0, "restecg": 0, "thalach": 172, "exang": 0, "oldpeak": 1.4, "slope": 2, "ca": 0, "thal": 2},
        "expected_risk": "Low"
    },
    {
        "name": "Healthy Young Adult",
        "data": {"age": 29, "sex": 0, "cp": 1, "trestbps": 120, "chol": 180, "fbs": 0, "restecg": 0, "thalach": 180, "exang": 0, "oldpeak": 0.0, "slope": 1, "ca": 0, "thal": 2},
        "expected_risk": "Low"
    },
    {
        "name": "Senior with Symptoms",
        "data": {"age": 71, "sex": 1, "cp": 3, "trestbps": 160, "chol": 302, "fbs": 0, "restecg": 1, "thalach": 162, "exang": 0, "oldpeak": 0.4, "slope": 2, "ca": 2, "thal": 2},
        "expected_risk": "High"
    },
    {
        "name": "Middle-aged Female",
        "data": {"age": 54, "sex": 0, "cp": 2, "trestbps": 135, "chol": 304, "fbs": 1, "restecg": 1, "thalach": 170, "exang": 0, "oldpeak": 0.0, "slope": 2, "ca": 0, "thal": 2},
        "expected_risk": "Medium"
    },
    {
        "name": "Athletic Male",
        "data": {"age": 42, "sex": 1, "cp": 1, "trestbps": 120, "chol": 200, "fbs": 0, "restecg": 0, "thalach": 190, "exang": 0, "oldpeak": 0.2, "slope": 1, "ca": 0, "thal": 2},
        "expected_risk": "Low"
    }
]

# Statistics tracking
class MetricsCollector:
    def __init__(self):
        self.total_requests = 0
        self.successful_predictions = 0
        self.failed_requests = 0
        self.health_checks = 0
        self.predictions_by_result = {0: 0, 1: 0}
        self.predictions_by_risk = {"Low": 0, "Medium": 0, "High": 0}
        self.response_times = []
        self.errors = []
        self.lock = threading.Lock()
    
    def record_prediction(self, prediction: int, risk: str, response_time: float):
        with self.lock:
            self.total_requests += 1
            self.successful_predictions += 1
            self.predictions_by_result[prediction] += 1
            self.predictions_by_risk[risk] += 1
            self.response_times.append(response_time)
    
    def record_error(self, error: str):
        with self.lock:
            self.total_requests += 1
            self.failed_requests += 1
            self.errors.append(error)
    
    def record_health_check(self):
        with self.lock:
            self.health_checks += 1
    
    def get_stats(self) -> Dict:
        with self.lock:
            return {
                "total_requests": self.total_requests,
                "successful_predictions": self.successful_predictions,
                "failed_requests": self.failed_requests,
                "health_checks": self.health_checks,
                "predictions_by_result": self.predictions_by_result.copy(),
                "predictions_by_risk": self.predictions_by_risk.copy(),
                "avg_response_time": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
                "min_response_time": min(self.response_times) if self.response_times else 0,
                "max_response_time": max(self.response_times) if self.response_times else 0,
                "error_count": len(self.errors)
            }

collector = MetricsCollector()

def check_health() -> bool:
    """Check if API is healthy"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        collector.record_health_check()
        return response.status_code == 200 and response.json().get("status") == "healthy"
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def make_prediction(patient_profile: Dict) -> Dict:
    """Make a prediction request"""
    try:
        start_time = time.time()
        response = requests.post(
            PREDICT_ENDPOINT,
            json=patient_profile["data"],
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            prediction = result.get("prediction")
            risk = result.get("risk_level")
            probability = result.get("probability", 0)
            
            collector.record_prediction(prediction, risk, response_time)
            
            return {
                "success": True,
                "patient": patient_profile["name"],
                "prediction": prediction,
                "risk": risk,
                "probability": probability,
                "response_time": response_time
            }
        else:
            error_msg = f"Status {response.status_code}: {response.text}"
            collector.record_error(error_msg)
            return {"success": False, "error": error_msg}
            
    except Exception as e:
        error_msg = str(e)
        collector.record_error(error_msg)
        return {"success": False, "error": error_msg}

def get_metrics() -> str:
    """Fetch current Prometheus metrics"""
    try:
        response = requests.get(METRICS_ENDPOINT, timeout=5)
        if response.status_code == 200:
            return response.text
        return None
    except Exception as e:
        return None

def print_stats():
    """Print current statistics"""
    stats = collector.get_stats()
    print("\n" + "="*70)
    print("📊 CURRENT STATISTICS")
    print("="*70)
    print(f"Total Requests:          {stats['total_requests']}")
    print(f"Successful Predictions:  {stats['successful_predictions']}")
    print(f"Failed Requests:         {stats['failed_requests']}")
    print(f"Health Checks:           {stats['health_checks']}")
    print(f"\nPredictions by Result:")
    print(f"  No Disease (0):        {stats['predictions_by_result'][0]}")
    print(f"  Disease (1):           {stats['predictions_by_result'][1]}")
    print(f"\nPredictions by Risk Level:")
    print(f"  Low Risk:              {stats['predictions_by_risk']['Low']}")
    print(f"  Medium Risk:           {stats['predictions_by_risk']['Medium']}")
    print(f"  High Risk:             {stats['predictions_by_risk']['High']}")
    print(f"\nResponse Times:")
    print(f"  Average:               {stats['avg_response_time']:.3f}s")
    print(f"  Min:                   {stats['min_response_time']:.3f}s")
    print(f"  Max:                   {stats['max_response_time']:.3f}s")
    print("="*70 + "\n")

def burst_test(num_requests: int = 10, delay: float = 0.1):
    """Send burst of requests quickly"""
    print(f"\n🚀 BURST TEST: Sending {num_requests} rapid requests...")
    for i in range(num_requests):
        patient = random.choice(PATIENT_PROFILES)
        result = make_prediction(patient)
        if result["success"]:
            print(f"  [{i+1}/{num_requests}] {patient['name']}: {result['risk']} risk ({result['prediction']}) - {result['response_time']:.3f}s")
        else:
            print(f"  [{i+1}/{num_requests}] ❌ Failed: {result['error']}")
        time.sleep(delay)

def steady_load(duration_seconds: int = 60, rate_per_minute: int = 30):
    """Generate steady load for specified duration"""
    print(f"\n⚡ STEADY LOAD TEST: {rate_per_minute} requests/min for {duration_seconds}s...")
    delay = 60.0 / rate_per_minute
    end_time = time.time() + duration_seconds
    count = 0
    
    while time.time() < end_time:
        patient = random.choice(PATIENT_PROFILES)
        result = make_prediction(patient)
        count += 1
        
        if count % 10 == 0:
            print(f"  Progress: {count} requests sent...")
        
        time.sleep(delay)
    
    print(f"✅ Completed {count} requests")

def concurrent_load(num_concurrent: int = 5, requests_per_thread: int = 10):
    """Send concurrent requests to test thread safety"""
    print(f"\n🔀 CONCURRENT LOAD TEST: {num_concurrent} threads × {requests_per_thread} requests...")
    
    def worker(thread_id: int):
        results = []
        for i in range(requests_per_thread):
            patient = random.choice(PATIENT_PROFILES)
            result = make_prediction(patient)
            results.append(result)
            time.sleep(random.uniform(0.1, 0.5))
        return thread_id, results
    
    with ThreadPoolExecutor(max_workers=num_concurrent) as executor:
        futures = [executor.submit(worker, i) for i in range(num_concurrent)]
        
        for future in as_completed(futures):
            thread_id, results = future.result()
            successful = sum(1 for r in results if r["success"])
            print(f"  Thread {thread_id}: {successful}/{requests_per_thread} successful")

def simulate_realistic_traffic(duration_minutes: int = 5):
    """Simulate realistic user traffic patterns"""
    print(f"\n🌐 REALISTIC TRAFFIC SIMULATION: Running for {duration_minutes} minutes...")
    print("Simulating: peak hours, idle periods, and occasional bursts\n")
    
    end_time = time.time() + (duration_minutes * 60)
    cycle = 0
    
    while time.time() < end_time:
        cycle += 1
        cycle_type = random.choices(
            ["quiet", "normal", "busy", "burst"],
            weights=[0.2, 0.4, 0.3, 0.1]
        )[0]
        
        if cycle_type == "quiet":
            print(f"[Cycle {cycle}] 😴 Quiet period (1-2 requests)...")
            for _ in range(random.randint(1, 2)):
                patient = random.choice(PATIENT_PROFILES)
                make_prediction(patient)
                time.sleep(random.uniform(3, 6))
                
        elif cycle_type == "normal":
            print(f"[Cycle {cycle}] 👤 Normal traffic (3-5 requests)...")
            for _ in range(random.randint(3, 5)):
                patient = random.choice(PATIENT_PROFILES)
                make_prediction(patient)
                time.sleep(random.uniform(1, 3))
                
        elif cycle_type == "busy":
            print(f"[Cycle {cycle}] 👥 Busy period (8-12 requests)...")
            for _ in range(random.randint(8, 12)):
                patient = random.choice(PATIENT_PROFILES)
                make_prediction(patient)
                time.sleep(random.uniform(0.5, 1.5))
                
        else:  # burst
            print(f"[Cycle {cycle}] 💥 Traffic burst (15-20 rapid requests)...")
            for _ in range(random.randint(15, 20)):
                patient = random.choice(PATIENT_PROFILES)
                make_prediction(patient)
                time.sleep(random.uniform(0.1, 0.3))
        
        # Periodic health check
        if cycle % 5 == 0:
            check_health()
            print_stats()
        
        # Cool down between cycles
        time.sleep(random.uniform(2, 5))

def menu():
    """Interactive menu"""
    print("\n" + "="*70)
    print("🏥 HEART DISEASE ML API - COMPREHENSIVE TESTER")
    print("="*70)
    print("\nTest Modes:")
    print("  1. Quick Test (10 diverse predictions)")
    print("  2. Burst Test (50 rapid requests)")
    print("  3. Steady Load (1 min @ 30 req/min)")
    print("  4. Concurrent Load (5 threads × 20 requests)")
    print("  5. Realistic Traffic (5 minute simulation)")
    print("  6. Extended Test (10 minute comprehensive test)")
    print("  7. View Current Metrics")
    print("  8. Continuous Testing (until Ctrl+C)")
    print("  9. Exit")
    print("="*70)

def main():
    """Main execution"""
    print("\n🔍 Checking API health...")
    if not check_health():
        print("❌ API is not responding. Please start the API first.")
        print("\nTo start the API, run:")
        print("  cd /Users/v0s01jh/Documents/BITS/MLOpsExperimentalLearning_Assignment_1_Group_81/heart-disease-mlops")
        print("  source venv/bin/activate")
        print("  PYTHONPATH=. python src/app.py")
        return
    
    print("✅ API is healthy and ready!\n")
    
    while True:
        menu()
        choice = input("\nSelect an option (1-9): ").strip()
        
        try:
            if choice == "1":
                print("\n" + "="*70)
                print("🧪 QUICK TEST - Testing all patient profiles")
                print("="*70)
                for patient in PATIENT_PROFILES:
                    result = make_prediction(patient)
                    if result["success"]:
                        print(f"✅ {patient['name']:30s} → Prediction: {result['prediction']} | "
                              f"Risk: {result['risk']:6s} | "
                              f"Probability: {result['probability']:.3f} | "
                              f"Time: {result['response_time']:.3f}s")
                    else:
                        print(f"❌ {patient['name']:30s} → Error: {result['error']}")
                    time.sleep(0.5)
                print_stats()
                
            elif choice == "2":
                burst_test(50, 0.2)
                print_stats()
                
            elif choice == "3":
                steady_load(60, 30)
                print_stats()
                
            elif choice == "4":
                concurrent_load(5, 20)
                print_stats()
                
            elif choice == "5":
                simulate_realistic_traffic(5)
                print_stats()
                
            elif choice == "6":
                print("\n🔥 EXTENDED COMPREHENSIVE TEST")
                print("This will run multiple test scenarios over 10 minutes...\n")
                
                # Phase 1: Warm up
                print("Phase 1: Warm-up (burst test)")
                burst_test(20, 0.1)
                
                # Phase 2: Concurrent
                print("\nPhase 2: Concurrent load test")
                concurrent_load(3, 15)
                
                # Phase 3: Realistic traffic
                print("\nPhase 3: Realistic traffic simulation")
                simulate_realistic_traffic(8)
                
                print("\n✅ Extended test complete!")
                print_stats()
                
            elif choice == "7":
                print("\n📊 Fetching Prometheus metrics...")
                metrics = get_metrics()
                if metrics:
                    print("\n" + "="*70)
                    print("PROMETHEUS METRICS")
                    print("="*70)
                    # Show only prediction-related metrics
                    for line in metrics.split('\n'):
                        if 'prediction' in line.lower() or 'http_request' in line.lower():
                            print(line)
                    print("="*70)
                else:
                    print("❌ Could not fetch metrics")
                print_stats()
                
            elif choice == "8":
                print("\n♾️  CONTINUOUS TESTING MODE")
                print("Press Ctrl+C to stop\n")
                try:
                    while True:
                        patient = random.choice(PATIENT_PROFILES)
                        result = make_prediction(patient)
                        if result["success"]:
                            print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                                  f"{patient['name']:30s} → {result['risk']:6s} "
                                  f"({result['prediction']}) - {result['response_time']:.3f}s")
                        time.sleep(random.uniform(1, 3))
                        
                        # Periodic stats
                        if collector.total_requests % 50 == 0:
                            print_stats()
                            
                except KeyboardInterrupt:
                    print("\n\n⏸️  Stopped continuous testing")
                    print_stats()
                
            elif choice == "9":
                print("\n👋 Exiting... Final statistics:")
                print_stats()
                break
                
            else:
                print("❌ Invalid choice. Please select 1-9.")
                
        except KeyboardInterrupt:
            print("\n\n⏸️  Operation interrupted")
            print_stats()
            continue
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        print_stats()
