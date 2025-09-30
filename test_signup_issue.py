#!/usr/bin/env python3
"""
Test script to debug signup issues
"""

import requests
import json
import random
import string

def generate_test_user():
    """Generate a unique test user"""
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        'name': f'TestUser{random_id}',
        'email': f'test{random_id}@example.com',
        'password': 'Test123!'
    }

def test_signup_scenarios():
    """Test various signup scenarios"""
    
    print("🧪 Testing Signup Issues")
    print("=" * 50)
    
    backend_url = "https://project-p4-yc0o.onrender.com"
    frontend_url = "https://project-p4-lovat.vercel.app"
    
    # Test 1: Valid new user
    print("1. Testing valid new user registration...")
    test_user = generate_test_user()
    print(f"   User: {test_user['name']} ({test_user['email']})")
    
    try:
        response = requests.post(
            f"{backend_url}/register",
            json=test_user,
            headers={
                'Content-Type': 'application/json',
                'Origin': frontend_url
            },
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Success: User ID {data['user']['id']} created")
        else:
            print(f"   ❌ Failed: {response.text}")
            
    except Exception as e:
        print(f"   🚨 Error: {e}")
    
    # Test 2: Duplicate email
    print("\n2. Testing duplicate email...")
    try:
        response = requests.post(
            f"{backend_url}/register",
            json={
                'name': 'Duplicate User',
                'email': 'user1@gmail.com',  # Existing user
                'password': 'Test123!'
            },
            headers={
                'Content-Type': 'application/json',
                'Origin': frontend_url
            },
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Correctly rejected: {data.get('message', 'No message')}")
        else:
            print(f"   ❌ Unexpected response: {response.text}")
            
    except Exception as e:
        print(f"   🚨 Error: {e}")
    
    # Test 3: Invalid data
    print("\n3. Testing invalid data (missing fields)...")
    try:
        response = requests.post(
            f"{backend_url}/register",
            json={
                'name': '',  # Empty name
                'email': 'invalid-email',  # Invalid email
                'password': '123'  # Weak password
            },
            headers={
                'Content-Type': 'application/json',
                'Origin': frontend_url
            },
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   🚨 Error: {e}")
    
    # Test 4: Check current users
    print("\n4. Checking existing users...")
    try:
        response = requests.get(f"{backend_url}/users", timeout=30)
        if response.status_code == 200:
            users = response.json()
            print(f"   ✅ Found {len(users)} users in database")
            for user in users[-3:]:  # Show last 3 users
                print(f"      - {user.get('username', 'N/A')} ({user.get('email', 'N/A')})")
        else:
            print(f"   ❌ Failed to get users: {response.status_code}")
    except Exception as e:
        print(f"   🚨 Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Signup Test Complete!")
    print("\n💡 Common Issues:")
    print("   - Email domain validation too strict (.com, .me, .co.ke, etc.)")
    print("   - Password requirements: max 10 chars, A-z, 0-9/special")
    print("   - Username: 3-20 characters")
    print("   - Confirm password must match")

if __name__ == "__main__":
    test_signup_scenarios()
