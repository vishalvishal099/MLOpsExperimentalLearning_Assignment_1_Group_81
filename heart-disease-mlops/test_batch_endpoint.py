#!/usr/bin/env python3
"""
Update comprehensive tester to include batch endpoint testing
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comprehensive_api_tester import (
    check_health, PATIENT_PROFILES, collector, make_prediction,
    PREDICT_ENDPOINT, API_BASE_URL
)
import requests
import time
import random

# Batch endpoint
BATCH_ENDPOINT = f"{API_BASE_URL}/predict/batch"

def make_batch_prediction(batch_size=5):
    """Make a batch prediction request"""
    try:
        # Select random patients for batch
        patients = random.sample(PATIENT_PROFILES, min(batch_size, len(PATIENT_PROFILES)))
        batch_data = [p["data"] for p in patients]
        
        start_time = time.time()
        response = requests.post(
            BATCH_ENDPOINT,
            json=batch_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            predictions = result["predictions"]
            
            # Update collector for each prediction in batch
            for pred in predictions:
                collector.record_prediction(
                    pred["prediction"],
                    pred["risk_level"],
                    response_time / len(predictions)
                )
            
            return {
                "success": True,
                "count": len(predictions),
                "batch_latency": result.get("batch_latency", response_time),
                "response_time": response_time,
                "predictions": predictions
            }
        else:
            error_msg = f"Status {response.status_code}: {response.text}"
            collector.record_error(error_msg)
            return {"success": False, "error": error_msg}
            
    except Exception as e:
        error_msg = str(e)
        collector.record_error(error_msg)
        return {"success": False, "error": error_msg}

def test_batch_endpoint():
    """Test the batch prediction endpoint"""
    print("\n" + "="*70)
    print("🔀 BATCH PREDICTION TEST")
    print("="*70)
    
    # Test different batch sizes
    batch_sizes = [2, 5, 10]
    
    for size in batch_sizes:
        print(f"\nTesting batch size: {size}")
        result = make_batch_prediction(batch_size=size)
        
        if result["success"]:
            print(f"  ✅ Batch of {result['count']} predictions")
            print(f"     Total time: {result['response_time']:.3f}s")
            print(f"     Avg per prediction: {result['response_time']/result['count']:.3f}s")
            print(f"     Results: ", end="")
            for i, pred in enumerate(result["predictions"][:3]):  # Show first 3
                print(f"{pred['prediction']}({pred['risk_level']})", end=" ")
            if len(result["predictions"]) > 3:
                print(f"... +{len(result['predictions'])-3} more")
            else:
                print()
        else:
            print(f"  ❌ Failed: {result['error']}")
        
        time.sleep(1)

def mixed_endpoint_test(duration_seconds=60):
    """Test both single and batch endpoints together"""
    print("\n" + "="*70)
    print(f"🎭 MIXED ENDPOINT TEST ({duration_seconds}s)")
    print("="*70)
    print("Testing both /predict and /predict/batch endpoints\n")
    
    end_time = time.time() + duration_seconds
    single_count = 0
    batch_count = 0
    
    while time.time() < end_time:
        # Randomly choose between single and batch
        if random.random() < 0.7:  # 70% single predictions
            patient = random.choice(PATIENT_PROFILES)
            result = make_prediction(patient)
            if result["success"]:
                single_count += 1
                print(f"  Single: {patient['name']:30s} → {result['risk']:6s}", end="\r")
        else:  # 30% batch predictions
            batch_size = random.randint(2, 5)
            result = make_batch_prediction(batch_size)
            if result["success"]:
                batch_count += 1
                print(f"  Batch: {result['count']} predictions in {result['response_time']:.2f}s    ", end="\r")
        
        time.sleep(random.uniform(0.5, 2))
    
    print(f"\n\n✅ Mixed test complete:")
    print(f"   Single predictions: {single_count}")
    print(f"   Batch predictions:  {batch_count}")

def main():
    print("\n" + "="*80)
    print("🧪 BATCH ENDPOINT TESTER")
    print("="*80)
    
    # Check API
    if not check_health():
        print("\n❌ API is not responding. Please ensure:")
        print("   1. API is running: python restart_api.py")
        print("   2. Or manually: PYTHONPATH=. python src/app.py")
        return 1
    
    print("✅ API is healthy!\n")
    
    while True:
        print("\n" + "="*70)
        print("TEST OPTIONS")
        print("="*70)
        print("1. Test Batch Endpoint (different sizes)")
        print("2. Mixed Endpoint Test (60s, single + batch)")
        print("3. Run Full Comprehensive Tests")
        print("4. Return to Main Menu")
        print("="*70)
        
        choice = input("\nSelect (1-4): ").strip()
        
        if choice == "1":
            test_batch_endpoint()
        elif choice == "2":
            mixed_endpoint_test(60)
        elif choice == "3":
            print("\n🚀 Launching main comprehensive tester...")
            print("Please run: python comprehensive_api_tester.py")
            break
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
