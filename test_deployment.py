#!/usr/bin/env python3
"""
Test script to verify deployment connectivity
"""

import requests
import json

def test_deployment():
    """Test the deployed frontend and backend connectivity"""
    
    print("🚀 Testing WiFi Portal Deployment")
    print("=" * 50)
    
    # URLs
    frontend_url = "https://project-p4-lovat.vercel.app"
    backend_url = "https://project-p4-yc0o.onrender.com"
    
    print(f"Frontend: {frontend_url}")
    print(f"Backend:  {backend_url}")
    print()
    
    # Test 1: Backend Health Check
    print("1. Testing Backend API...")
    try:
        response = requests.get(f"{backend_url}/plans", timeout=30)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Backend API working - Found {len(plans)} plans")
        else:
            print(f"❌ Backend API error: {response.status_code}")
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
    
    # Test 2: CORS Check
    print("\n2. Testing CORS Configuration...")
    try:
        headers = {
            'Origin': frontend_url,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{backend_url}/login", headers=headers, timeout=10)
        if response.status_code in [200, 204]:
            print("✅ CORS configured correctly")
        else:
            print(f"❌ CORS issue: {response.status_code}")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")
    
    # Test 3: Login Endpoint
    print("\n3. Testing Login Endpoint...")
    try:
        login_data = {
            "email": "user1@gmail.com",
            "password": "User1!"
        }
        response = requests.post(
            f"{backend_url}/login", 
            json=login_data,
            headers={'Origin': frontend_url},
            timeout=10
        )
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Login working - User: {user_data.get('name', 'Unknown')}")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Login test failed: {e}")
    
    # Test 4: Frontend Accessibility
    print("\n4. Testing Frontend Accessibility...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend accessible")
        else:
            print(f"❌ Frontend error: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Deployment Test Complete!")
    print(f"🌐 Visit: {frontend_url}/login")
    print("📧 Test Login: user1@gmail.com / User1!")

if __name__ == "__main__":
    test_deployment()
