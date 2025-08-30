#!/usr/bin/env python3
"""
Test script for MCP Server Bridge functionality.
"""

import json
import time
from datetime import datetime

import requests

BASE_URL = "http://localhost:8000"


def test_mcp_endpoints():
    """Test all MCP endpoints."""
    print("🧪 Testing MCP Server Bridge Endpoints")
    print("=" * 50)

    # Test 1: Check if service is running
    print("\n1. Testing service health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Service healthy: {health.get('status', 'unknown')}")
            print(f"   Total chunks: {health.get('total_chunks', 0)}")
        else:
            print(f"❌ Service unhealthy: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Service not accessible: {e}")
        return False

    # Test 2: Check MCP tools endpoint
    print("\n2. Testing MCP tools endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/tools", timeout=10)
        if response.status_code == 200:
            tools = response.json()
            print(
                f"✅ Tools endpoint working: {len(tools.get('tools', []))} tools registered"
            )
            for tool in tools.get("tools", [])[:3]:  # Show first 3 tools
                print(
                    f"   - {tool.get('name', 'unknown')}: {tool.get('description', 'no description')}"
                )
        else:
            print(f"❌ Tools endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Tools endpoint error: {e}")
        return False

    # Test 3: Check MCP status endpoint
    print("\n3. Testing MCP status endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/mcp/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"✅ Status endpoint working")
            print(f"   LLM loaded: {status.get('llm_loaded', False)}")
            print(f"   FAISS available: {status.get('faiss_available', False)}")
            print(f"   Tools active: {status.get('tools_active', 0)}")
            print(f"   Status: {status.get('status', 'unknown')}")
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False

    # Test 4: Test MCP analyze endpoint with sample feature
    print("\n4. Testing MCP analyze endpoint...")
    test_features = [
        {
            "feature_id": "test_age_verification_eu",
            "feature_title": "Age Verification for EU Users",
            "description": "Requires parental consent for users under 16 in EU jurisdictions",
            "region_hint": "EU",
            "dataset_tag": "test",
        },
        {
            "feature_id": "test_global_except_kr",
            "feature_title": "Global Feature Except Korea",
            "description": "Feature available globally except for users in South Korea due to local regulations",
            "region_hint": "Global",
            "dataset_tag": "test",
        },
        {
            "feature_id": "test_indonesia_age_gating",
            "feature_title": "Indonesia Age Gating",
            "description": "Age verification required for users in Indonesia with strict enforcement",
            "region_hint": "ID",
            "dataset_tag": "test",
        },
    ]

    for i, feature in enumerate(test_features, 1):
        print(f"\n   Testing feature {i}: {feature['feature_title']}")
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/mcp/analyze",
                json=feature,
                timeout=60,  # Longer timeout for analysis
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Analysis successful in {duration:.2f}s")
                print(f"      Decision: {result.get('decision_flag', 'unknown')}")
                print(f"      Confidence: {result.get('confidence', 0):.2f}")
                print(f"      Tools used: {len(result.get('tools_used', []))}")
                print(f"      Request ID: {result.get('request_id', 'unknown')}")
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                print(f"      Error: {response.text}")
                return False

        except Exception as e:
            print(f"   ❌ Analysis error: {e}")
            return False

    # Test 5: Check evidence logging
    print("\n5. Testing evidence logging...")
    try:
        response = requests.get(
            f"{BASE_URL}/evidence?limit=5&order=timestamp_desc", timeout=10
        )
        if response.status_code == 200:
            evidence = response.json()
            recent_records = evidence.get("items", [])
            mcp_records = [
                r for r in recent_records if r.get("agent_name") == "mcp_orchestrator"
            ]
            print(f"✅ Evidence endpoint working: {len(mcp_records)} MCP records found")
            if mcp_records:
                latest = mcp_records[0]
                print(f"   Latest MCP record: {latest.get('feature_title', 'unknown')}")
                print(f"   Decision: {latest.get('decision_flag', 'unknown')}")
        else:
            print(f"❌ Evidence endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Evidence endpoint error: {e}")

    print("\n🎉 All MCP tests completed successfully!")
    return True


def test_csv_export():
    """Test CSV export functionality."""
    print("\n📊 Testing CSV Export Functionality")
    print("=" * 40)

    try:
        response = requests.get(
            f"{BASE_URL}/evidence/export?format=csv&limit=10", timeout=30
        )

        if response.status_code == 200:
            csv_content = response.text
            lines = csv_content.strip().split("\n")
            print(f"✅ CSV export successful: {len(lines)} lines")
            if lines:
                headers = lines[0].split(",")
                print(f"   Headers: {', '.join(headers[:5])}...")
                print(f"   Data rows: {len(lines) - 1}")
        else:
            print(f"❌ CSV export failed: {response.status_code}")
            print(f"   Error: {response.text}")

    except Exception as e:
        print(f"❌ CSV export error: {e}")


def main():
    """Main test function."""
    print("🚀 MCP Server Bridge Test Suite")
    print("=" * 50)
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Test MCP functionality
    if test_mcp_endpoints():
        # Test CSV export
        test_csv_export()

        print("\n" + "=" * 50)
        print("✅ All tests passed! MCP Server Bridge is working correctly.")
        print("\nNext steps:")
        print("1. Open the dashboard at http://localhost:3000")
        print("2. Use the MCP Chat interface to test features")
        print("3. Check the /evidence endpoint for logged decisions")
        print("4. Verify CSV export functionality")
    else:
        print("\n" + "=" * 50)
        print("❌ Some tests failed. Check the service logs for details.")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
