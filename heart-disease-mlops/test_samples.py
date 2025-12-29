#!/usr/bin/env python3
"""
Test API with various sample requests
"""
import requests
import json
import time
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_single_request():
    """Test single prediction endpoint"""
    print("\n" + "="*70)
    print("🔹 TESTING SINGLE PREDICTION")
    print("="*70)
    
    with open("sample_single_request.json", "r") as f:
        data = json.load(f)
    
    print(f"\n📤 Sending request to {API_BASE_URL}/predict")
    print(f"   Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(
        f"{API_BASE_URL}/predict",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Response:")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Probability: {result['probability']:.3f}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Response Time: {response.elapsed.total_seconds():.3f}s")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"   {response.text}")

def test_batch_request():
    """Test batch prediction endpoint"""
    print("\n" + "="*70)
    print("🔹 TESTING BATCH PREDICTION")
    print("="*70)
    
    with open("sample_batch_request.json", "r") as f:
        data = json.load(f)
    
    print(f"\n📤 Sending batch request to {API_BASE_URL}/predict/batch")
    print(f"   Number of patients: {len(data)}")
    
    response = requests.post(
        f"{API_BASE_URL}/predict/batch",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Batch Response:")
        print(f"   Total predictions: {result['count']}")
        print(f"   Batch latency: {result['batch_latency']:.3f}s")
        print(f"   Avg per prediction: {result['batch_latency']/result['count']:.3f}s")
        print(f"\n   Results:")
        for i, pred in enumerate(result['predictions'], 1):
            print(f"   Patient {i}: Prediction={pred['prediction']}, "
                  f"Probability={pred['probability']:.3f}, "
                  f"Risk={pred['risk_level']}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"   {response.text}")

def test_all_patients():
    """Test all sample patients"""
    print("\n" + "="*70)
    print("🔹 TESTING ALL SAMPLE PATIENTS")
    print("="*70)
    
    with open("sample_patients.json", "r") as f:
        patients = json.load(f)
    
    print(f"\n📊 Testing {len(patients)} patients...")
    
    results = {
        "no_disease": 0,
        "disease": 0,
        "low_risk": 0,
        "medium_risk": 0,
        "high_risk": 0
    }
    
    for patient in patients:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=patient["data"],
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            prediction = result['prediction']
            risk_level = result['risk_level']
            
            if prediction == 0:
                results["no_disease"] += 1
            else:
                results["disease"] += 1
            
            if risk_level == "Low":
                results["low_risk"] += 1
            elif risk_level == "Medium":
                results["medium_risk"] += 1
            else:
                results["high_risk"] += 1
            
            print(f"   ✓ {patient['name']:45s} → {prediction} ({risk_level})")
        else:
            print(f"   ✗ {patient['name']:45s} → Error")
        
        time.sleep(0.1)
    
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70)
    print(f"Total patients tested: {len(patients)}")
    print(f"\nPredictions:")
    print(f"   No Disease (0): {results['no_disease']}")
    print(f"   Disease (1):    {results['disease']}")
    print(f"\nRisk Levels:")
    print(f"   Low Risk:       {results['low_risk']}")
    print(f"   Medium Risk:    {results['medium_risk']}")
    print(f"   High Risk:      {results['high_risk']}")

def test_health():
    """Test health endpoint"""
    print("\n" + "="*70)
    print("🔹 TESTING HEALTH ENDPOINT")
    print("="*70)
    
    response = requests.get(f"{API_BASE_URL}/health")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ Health Status:")
        print(f"   Status: {result['status']}")
        print(f"   Model Loaded: {result['model_loaded']}")
        print(f"   Preprocessor Loaded: {result['preprocessor_loaded']}")
    else:
        print(f"\n❌ Error: {response.status_code}")

def main():
    print("\n" + "="*70)
    print("🧪 API SAMPLE DATA TESTER")
    print("="*70)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ API is not healthy!")
            return
    except:
        print("\n❌ Cannot connect to API. Please ensure it's running:")
        print("   cd /path/to/heart-disease-mlops")
        print("   source venv/bin/activate")
        print("   PYTHONPATH=. python src/app.py")
        return
    
    while True:
        print("\n" + "="*70)
        print("SELECT TEST")
        print("="*70)
        print("1. Test Single Prediction (sample_single_request.json)")
        print("2. Test Batch Prediction (sample_batch_request.json)")
        print("3. Test All Sample Patients (sample_patients.json)")
        print("4. Test Health Endpoint")
        print("5. Run All Tests")
        print("6. Exit")
        print("="*70)
        
        choice = input("\nSelect (1-6): ").strip()
        
        if choice == "1":
            test_single_request()
        elif choice == "2":
            test_batch_request()
        elif choice == "3":
            test_all_patients()
        elif choice == "4":
            test_health()
        elif choice == "5":
            test_health()
            test_single_request()
            test_batch_request()
            test_all_patients()
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
        
        input("\n[Press Enter to continue]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
