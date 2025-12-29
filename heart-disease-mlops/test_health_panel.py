#!/usr/bin/env python3
"""
Test Grafana API Health Status panel query
"""
import requests
import json
import time

PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3000"

def test_prometheus_query():
    """Test if Prometheus has the metric"""
    print("="*70)
    print("🔍 TESTING API HEALTH STATUS METRIC")
    print("="*70)
    
    # Query Prometheus
    print("\n📊 Querying Prometheus...")
    query = "api_health_status"
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            results = data["data"]["result"]
            if results:
                value = results[0]["value"][1]
                print(f"✅ Metric found in Prometheus")
                print(f"   Query: {query}")
                print(f"   Value: {value}")
                print(f"   Labels: {results[0]['metric']}")
                return True
            else:
                print(f"❌ No data for query: {query}")
                return False
    
    print(f"❌ Failed to query Prometheus: {response.status_code}")
    return False

def test_grafana_datasource():
    """Test Grafana datasource connection"""
    print("\n📡 Testing Grafana Datasource...")
    
    response = requests.get(
        f"{GRAFANA_URL}/api/datasources",
        auth=("admin", "admin")
    )
    
    if response.status_code == 200:
        datasources = response.json()
        for ds in datasources:
            if ds["type"] == "prometheus":
                print(f"✅ Prometheus datasource found")
                print(f"   Name: {ds['name']}")
                print(f"   UID: {ds['uid']}")
                print(f"   URL: {ds['url']}")
                print(f"   Default: {ds['isDefault']}")
                return ds["uid"]
    
    print("❌ No Prometheus datasource found")
    return None

def generate_test_data():
    """Generate test data by calling health endpoint"""
    print("\n🔄 Generating test data...")
    
    for i in range(10):
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print(f"   Health check {i+1}/10 ✓", end="\r")
        time.sleep(0.5)
    
    print("\n✅ Generated 10 health checks")
    
    # Wait for Prometheus to scrape
    print("   Waiting 5s for Prometheus to scrape...")
    time.sleep(5)

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 GRAFANA HEALTH STATUS PANEL TROUBLESHOOTING")
    print("="*70)
    
    # Test Prometheus query
    if test_prometheus_query():
        print("\n✅ Step 1 passed: Metric available in Prometheus")
    else:
        print("\n❌ Step 1 failed: Metric not in Prometheus")
        print("   Fix: Check if API is running and exposing metrics")
        exit(1)
    
    # Test Grafana datasource
    uid = test_grafana_datasource()
    if uid:
        print("\n✅ Step 2 passed: Grafana datasource configured")
    else:
        print("\n❌ Step 2 failed: No Prometheus datasource in Grafana")
        exit(1)
    
    # Generate test data
    generate_test_data()
    
    # Final verification
    if test_prometheus_query():
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED")
        print("="*70)
        print("\nThe API Health Status panel should now work in Grafana!")
        print("\n📋 Next steps:")
        print(f"1. Open Grafana: {GRAFANA_URL}")
        print("2. Go to the dashboard")
        print("3. If still showing 'No data', check:")
        print("   - Time range (try 'Last 15 minutes')")
        print("   - Click on the panel title → Edit")
        print("   - Check the Query tab to see if data is returned")
        print("   - Try changing the query to: api_health_status")
        print("4. Hard refresh the browser (Ctrl+Shift+R)")
    else:
        print("\n❌ Metric disappeared - there may be an issue with metric collection")
