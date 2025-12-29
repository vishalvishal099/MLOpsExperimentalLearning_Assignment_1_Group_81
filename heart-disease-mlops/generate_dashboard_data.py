#!/usr/bin/env python3
"""
Generate comprehensive traffic to populate Grafana dashboard
"""
import requests
import time
import random
import json
from concurrent.futures import ThreadPoolExecutor

API_BASE = "http://localhost:8000"

# Sample patient profiles with varied risk
PATIENTS = [
    # High risk
    {"age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233, "fbs": 1, "restecg": 1, "thalach": 150, "exang": 1, "oldpeak": 2.3, "slope": 1, "ca": 1, "thal": 1},
    {"age": 67, "sex": 1, "cp": 4, "trestbps": 160, "chol": 286, "fbs": 1, "restecg": 1, "thalach": 108, "exang": 1, "oldpeak": 1.5, "slope": 2, "ca": 3, "thal": 2},
    # Medium risk
    {"age": 54, "sex": 1, "cp": 2, "trestbps": 125, "chol": 273, "fbs": 1, "restecg": 1, "thalach": 152, "exang": 1, "oldpeak": 0.5, "slope": 1, "ca": 1, "thal": 2},
    {"age": 48, "sex": 0, "cp": 3, "trestbps": 130, "chol": 275, "fbs": 1, "restecg": 1, "thalach": 139, "exang": 1, "oldpeak": 0.2, "slope": 2, "ca": 1, "thal": 2},
    # Low risk
    {"age": 37, "sex": 1, "cp": 2, "trestbps": 130, "chol": 250, "fbs": 1, "restecg": 1, "thalach": 187, "exang": 1, "oldpeak": 3.5, "slope": 1, "ca": 1, "thal": 2},
    {"age": 41, "sex": 0, "cp": 1, "trestbps": 130, "chol": 204, "fbs": 1, "restecg": 1, "thalach": 172, "exang": 1, "oldpeak": 1.4, "slope": 2, "ca": 1, "thal": 2},
    {"age": 29, "sex": 1, "cp": 1, "trestbps": 130, "chol": 204, "fbs": 1, "restecg": 1, "thalach": 202, "exang": 1, "oldpeak": 0.0, "slope": 2, "ca": 1, "thal": 2},
    {"age": 35, "sex": 0, "cp": 1, "trestbps": 138, "chol": 183, "fbs": 1, "restecg": 1, "thalach": 182, "exang": 1, "oldpeak": 1.4, "slope": 2, "ca": 1, "thal": 2},
]

def single_prediction(patient):
    """Send a single prediction request"""
    try:
        response = requests.post(f"{API_BASE}/predict", json=patient, timeout=5)
        return response.status_code == 200
    except:
        return False

def batch_prediction(batch_size=3):
    """Send a batch prediction request"""
    try:
        batch = random.sample(PATIENTS, min(batch_size, len(PATIENTS)))
        response = requests.post(f"{API_BASE}/predict/batch", json=batch, timeout=10)
        return response.status_code == 200
    except:
        return False

def health_check():
    """Send a health check request"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def generate_traffic(duration_seconds=120):
    """Generate mixed traffic for the specified duration"""
    print(f"\n🚀 Generating traffic for {duration_seconds} seconds...")
    print("=" * 70)
    
    end_time = time.time() + duration_seconds
    single_count = 0
    batch_count = 0
    health_count = 0
    
    while time.time() < end_time:
        remaining = int(end_time - time.time())
        
        # Random mix of operations
        rand = random.random()
        
        if rand < 0.6:  # 60% single predictions
            patient = random.choice(PATIENTS)
            if single_prediction(patient):
                single_count += 1
                print(f"✓ Single: {single_count:3d} | Batch: {batch_count:3d} | Health: {health_count:3d} | Time left: {remaining:3d}s", end="\r")
        
        elif rand < 0.9:  # 30% batch predictions
            batch_size = random.randint(2, 5)
            if batch_prediction(batch_size):
                batch_count += 1
                print(f"✓ Single: {single_count:3d} | Batch: {batch_count:3d} | Health: {health_count:3d} | Time left: {remaining:3d}s", end="\r")
        
        else:  # 10% health checks
            if health_check():
                health_count += 1
                print(f"✓ Single: {single_count:3d} | Batch: {batch_count:3d} | Health: {health_count:3d} | Time left: {remaining:3d}s", end="\r")
        
        # Random delay between requests
        time.sleep(random.uniform(0.1, 1.0))
    
    print("\n" + "=" * 70)
    print(f"✅ Traffic generation complete!")
    print(f"   Single predictions: {single_count}")
    print(f"   Batch predictions:  {batch_count}")
    print(f"   Health checks:      {health_count}")
    print(f"   Total requests:     {single_count + batch_count + health_count}")

def concurrent_load(num_threads=5, requests_per_thread=20):
    """Generate concurrent load"""
    print(f"\n⚡ Generating concurrent load: {num_threads} threads × {requests_per_thread} requests")
    print("=" * 70)
    
    def worker():
        for _ in range(requests_per_thread):
            patient = random.choice(PATIENTS)
            single_prediction(patient)
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(executor.map(lambda _: worker(), range(num_threads)))
    
    duration = time.time() - start
    total_requests = num_threads * requests_per_thread
    
    print(f"✅ Concurrent load complete!")
    print(f"   Total requests: {total_requests}")
    print(f"   Duration:       {duration:.2f}s")
    print(f"   Rate:           {total_requests/duration:.1f} req/s")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("📊 DASHBOARD TRAFFIC GENERATOR")
    print("=" * 70)
    
    # Check API health
    if not health_check():
        print("\n❌ API is not responding!")
        print("Please ensure the API is running on http://localhost:8000")
        exit(1)
    
    print("✅ API is healthy!\n")
    
    print("This will generate comprehensive traffic to populate all dashboard metrics:")
    print("  • Phase 1: Concurrent Load Test (5 threads × 20 requests)")
    print("  • Phase 2: Sustained Traffic (2 minutes)")
    print("  • Phase 3: Final Burst (5 threads × 10 requests)")
    print()
    
    input("Press ENTER to start... ")
    
    # Phase 1: Concurrent load
    print("\n" + "=" * 70)
    print("PHASE 1: CONCURRENT LOAD TEST")
    print("=" * 70)
    concurrent_load(5, 20)
    time.sleep(2)
    
    # Phase 2: Sustained traffic
    print("\n" + "=" * 70)
    print("PHASE 2: SUSTAINED TRAFFIC (2 minutes)")
    print("=" * 70)
    generate_traffic(120)
    time.sleep(2)
    
    # Phase 3: Final burst
    print("\n" + "=" * 70)
    print("PHASE 3: FINAL BURST")
    print("=" * 70)
    concurrent_load(5, 10)
    
    print("\n" + "=" * 70)
    print("🎉 ALL PHASES COMPLETE!")
    print("=" * 70)
    print("\n✅ Your Grafana dashboard should now be fully populated!")
    print(f"🔗 View dashboard: http://localhost:3000/d/heart-disease-ml-api-enhanced-monitoring")
    print()
