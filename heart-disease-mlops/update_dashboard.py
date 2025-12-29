#!/usr/bin/env python3
"""
Update Grafana dashboard with fixed configuration
"""
import requests
import json
import time

GRAFANA_URL = "http://localhost:3000"
GRAFANA_USER = "admin"
GRAFANA_PASSWORD = "admin"
DASHBOARD_FILE = "deployment/grafana/dashboards/enhanced_dashboard.json"

def update_dashboard():
    """Update the dashboard in Grafana"""
    print("="*70)
    print("📊 UPDATING GRAFANA DASHBOARD")
    print("="*70)
    
    # Read dashboard JSON
    print("\n📖 Reading dashboard file...")
    with open(DASHBOARD_FILE, 'r') as f:
        dashboard_json = json.load(f)
    
    # Prepare the payload
    payload = {
        "dashboard": dashboard_json["dashboard"],
        "overwrite": True,
        "message": "Fixed API Health Status panel"
    }
    
    # Import to Grafana
    print("📤 Uploading to Grafana...")
    response = requests.post(
        f"{GRAFANA_URL}/api/dashboards/db",
        auth=(GRAFANA_USER, GRAFANA_PASSWORD),
        headers={"Content-Type": "application/json"},
        json=payload
    )
    
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"✅ Dashboard updated successfully!")
        print(f"   Dashboard ID: {result.get('id')}")
        print(f"   Dashboard URL: {result.get('url')}")
        print(f"\n🌐 Open Grafana: {GRAFANA_URL}{result.get('url')}")
    else:
        print(f"❌ Failed to update dashboard")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        if update_dashboard():
            print("\n" + "="*70)
            print("✅ DASHBOARD UPDATE COMPLETE")
            print("="*70)
            print("\nNext steps:")
            print("1. Open Grafana: http://localhost:3000")
            print("2. Go to the dashboard")
            print("3. The API Health Status panel should now work correctly")
            print("4. Refresh the dashboard to see the changes")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
