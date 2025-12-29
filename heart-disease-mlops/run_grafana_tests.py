#!/usr/bin/env python3
"""
Auto-run script for populating Grafana dashboard with comprehensive metrics
Runs unattended for optimal dashboard visualization
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from comprehensive_api_tester import (
    check_health, burst_test, steady_load, concurrent_load,
    simulate_realistic_traffic, print_stats, collector
)
import time

def main():
    print("\n" + "="*80)
    print("🎯 AUTOMATED GRAFANA DASHBOARD DATA GENERATOR")
    print("="*80)
    print("\nThis script will generate comprehensive metrics for your Grafana dashboard.")
    print("It will run multiple test scenarios to populate all dashboard panels.\n")
    
    # Check API health
    print("🔍 Step 1: Checking API health...")
    if not check_health():
        print("\n❌ ERROR: API is not responding!")
        print("\nPlease start the API first:")
        print("  cd /Users/v0s01jh/Documents/BITS/MLOpsExperimentalLearning_Assignment_1_Group_81/heart-disease-mlops")
        print("  source venv/bin/activate")
        print("  PYTHONPATH=. python src/app.py &")
        return 1
    
    print("✅ API is healthy!\n")
    
    print("="*80)
    print("📊 TEST PLAN")
    print("="*80)
    print("Phase 1: Quick Burst (50 requests)               [Est. 15 seconds]")
    print("Phase 2: Concurrent Load (5 threads × 20 req)    [Est. 30 seconds]")
    print("Phase 3: Steady Load (60s @ 30 req/min)          [Est. 60 seconds]")
    print("Phase 4: Realistic Traffic Simulation            [Est. 5 minutes]")
    print("\nTotal estimated time: ~7 minutes")
    print("="*80)
    
    input("\n Press ENTER to start, or Ctrl+C to cancel... ")
    
    try:
        # Phase 1: Burst Test
        print("\n" + "="*80)
        print("🚀 PHASE 1: BURST TEST")
        print("="*80)
        print("Sending 50 rapid requests to test peak load handling...")
        burst_test(num_requests=50, delay=0.15)
        print("✅ Phase 1 complete!")
        print_stats()
        time.sleep(3)
        
        # Phase 2: Concurrent Load
        print("\n" + "="*80)
        print("🔀 PHASE 2: CONCURRENT LOAD TEST")
        print("="*80)
        print("Testing thread safety with concurrent requests...")
        concurrent_load(num_concurrent=5, requests_per_thread=20)
        print("✅ Phase 2 complete!")
        print_stats()
        time.sleep(3)
        
        # Phase 3: Steady Load
        print("\n" + "="*80)
        print("⚡ PHASE 3: STEADY LOAD TEST")
        print("="*80)
        print("Generating steady traffic at 30 requests per minute...")
        steady_load(duration_seconds=60, rate_per_minute=30)
        print("✅ Phase 3 complete!")
        print_stats()
        time.sleep(3)
        
        # Phase 4: Realistic Traffic
        print("\n" + "="*80)
        print("🌐 PHASE 4: REALISTIC TRAFFIC SIMULATION")
        print("="*80)
        print("Simulating real-world usage patterns with varying load...")
        simulate_realistic_traffic(duration_minutes=5)
        print("✅ Phase 4 complete!")
        
        # Final Statistics
        print("\n" + "="*80)
        print("🎉 ALL TESTS COMPLETE!")
        print("="*80)
        print_stats()
        
        print("\n" + "="*80)
        print("📊 NEXT STEPS - View Your Grafana Dashboard")
        print("="*80)
        print("\n1. Open Grafana in your browser:")
        print("   → http://localhost:3000")
        print("\n2. Login with:")
        print("   → Username: admin")
        print("   → Password: admin")
        print("\n3. Navigate to dashboard:")
        print("   → Click ☰ menu (top left)")
        print("   → Click 'Dashboards'")
        print("   → Select 'Heart Disease ML API Monitoring'")
        print("\n4. Adjust time range:")
        print("   → Click time picker (top right)")
        print("   → Select 'Last 15 minutes' or 'Last 30 minutes'")
        print("\n5. Enable auto-refresh:")
        print("   → Click refresh dropdown (top right)")
        print("   → Select '10s' or '30s'")
        print("\n6. All panels should now display data:")
        print("   ✅ Total Predictions")
        print("   ✅ Prediction Rate")
        print("   ✅ Average Prediction Time")
        print("   ✅ Predictions Over Time (graph)")
        print("   ✅ Latency Distribution")
        print("   ✅ Results Distribution (pie chart)")
        print("   ✅ Risk Level Distribution")
        print("   ✅ API Health Status")
        print("   ✅ System Metrics (CPU, Memory)")
        print("\n" + "="*80)
        print("📸 Perfect time to take screenshots for your assignment!")
        print("="*80 + "\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Test interrupted by user")
        print_stats()
        return 1
    except Exception as e:
        print(f"\n\n❌ Error occurred: {e}")
        print_stats()
        return 1

if __name__ == "__main__":
    sys.exit(main())
