#!/usr/bin/env python3
"""
Comprehensive test script for the evidence system.
Tests CSV export, API endpoints, and dashboard functionality.
"""

import requests
import json
import subprocess
import sys
from pathlib import Path

def test_csv_exporter():
    """Test the CSV exporter functionality."""
    print("🧪 Testing CSV Exporter...")
    
    # Test test dataset export
    result = subprocess.run([
        "python", "src/evidence_exporter.py", 
        "--test-dataset", 
        "--dataset-tag", "test_dataset",
        "--output", "test_output.csv"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Test dataset CSV export successful")
        
        # Check if file exists and has content
        if Path("test_output.csv").exists():
            with open("test_output.csv", 'r') as f:
                lines = f.readlines()
                if len(lines) > 1:  # Header + at least one data row
                    print(f"✅ CSV file created with {len(lines)-1} data rows")
                else:
                    print("❌ CSV file is empty")
        else:
            print("❌ CSV file not created")
    else:
        print(f"❌ CSV export failed: {result.stderr}")
    
    # Clean up
    if Path("test_output.csv").exists():
        Path("test_output.csv").unlink()

def test_api_endpoints():
    """Test the API endpoints."""
    print("\n🧪 Testing API Endpoints...")
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test evidence endpoint
    try:
        response = requests.get(f"{base_url}/evidence?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Evidence endpoint working - {data['total']} total records")
            
            # Test filtering
            response = requests.get(f"{base_url}/evidence?agent=test_agent_0")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent filtering working - {data['total']} filtered records")
            else:
                print("❌ Agent filtering failed")
                
        else:
            print(f"❌ Evidence endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Evidence endpoint error: {e}")
        return False
    
    # Test evidence summary endpoint
    try:
        response = requests.get(f"{base_url}/evidence/summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Evidence summary endpoint working - {data['total_records']} total records")
        else:
            print(f"❌ Evidence summary endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Evidence summary endpoint error: {e}")
    
    # Test CSV export endpoint
    try:
        response = requests.get(f"{base_url}/evidence/export?format=csv")
        if response.status_code == 200:
            content = response.text
            if "feature_id,decision_flag" in content:
                print("✅ CSV export endpoint working")
            else:
                print("❌ CSV export endpoint returned invalid content")
        else:
            print(f"❌ CSV export endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ CSV export endpoint error: {e}")
    
    return True

def test_dashboard():
    """Test the dashboard functionality."""
    print("\n🧪 Testing Dashboard...")
    
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/dashboard")
        if response.status_code == 200:
            content = response.text
            if "<title>Evidence Dashboard</title>" in content:
                print("✅ Dashboard HTML loaded successfully")
                
                # Check for key dashboard elements
                if "Evidence Dashboard" in content:
                    print("✅ Dashboard title present")
                if "loadEvidence()" in content:
                    print("✅ Dashboard JavaScript functions present")
                if "filters" in content:
                    print("✅ Dashboard filters present")
                if "summary" in content:
                    print("✅ Dashboard summary cards present")
                if "evidenceTable" in content:
                    print("✅ Dashboard table present")
                    
            else:
                print("❌ Dashboard content invalid")
        else:
            print(f"❌ Dashboard failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")

def test_filtering_and_pagination():
    """Test advanced filtering and pagination."""
    print("\n🧪 Testing Filtering and Pagination...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Test pagination
        response = requests.get(f"{base_url}/evidence?limit=2&offset=0")
        if response.status_code == 200:
            data = response.json()
            if data['limit'] == 2 and data['offset'] == 0 and len(data['items']) == 2:
                print("✅ Pagination working correctly")
            else:
                print("❌ Pagination not working correctly")
        
        # Test decision flag filtering
        response = requests.get(f"{base_url}/evidence?decision_flag=false")
        if response.status_code == 200:
            data = response.json()
            all_false = all(item['decision_flag'] == False for item in data['items'])
            if all_false:
                print("✅ Decision flag filtering working")
            else:
                print("❌ Decision flag filtering not working")
        
        # Test text search
        response = requests.get(f"{base_url}/evidence?q=Feature%201")
        if response.status_code == 200:
            data = response.json()
            if data['total'] > 0:
                print("✅ Text search working")
            else:
                print("❌ Text search not working")
                
    except Exception as e:
        print(f"❌ Filtering/pagination test error: {e}")

def main():
    """Run all tests."""
    print("🚀 Starting Evidence System Tests...\n")
    
    # Test CSV exporter
    test_csv_exporter()
    
    # Test API endpoints
    if test_api_endpoints():
        # Test dashboard
        test_dashboard()
        
        # Test advanced functionality
        test_filtering_and_pagination()
    
    print("\n✨ Test Summary Complete!")
    print("\n📋 Available Commands:")
    print("  • Generate test dataset CSV: python src/evidence_exporter.py --test-dataset --dataset-tag test_dataset --output evidence_TESTSET.csv")
    print("  • Start dashboard: python -m uvicorn retriever.service:app --host 0.0.0.0 --port 8000 --reload")
    print("  • Access dashboard: http://localhost:8000/dashboard")
    print("  • API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
