#!/usr/bin/env python3
"""
Test script to verify subscription overlap prevention
"""

import requests
import time

def test_subscription_overlap():
    """Test that users cannot have overlapping subscriptions"""
    
    print("🔒 Testing Subscription Overlap Prevention")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test user credentials
    user_id = 1
    
    print("1. Testing first subscription creation...")
    try:
        response = requests.post(f"{base_url}/subscriptions", json={
            'user_id': user_id,
            'plan_id': 1  # 1 Hour plan
        })
        
        if response.status_code == 201:
            print("✅ First subscription created successfully")
        elif response.status_code == 409:
            print("ℹ️  User already has an active subscription")
        else:
            print(f"❌ Unexpected response: {response.status_code} - {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error creating first subscription: {e}")
        return
    
    print("\n2. Testing overlap prevention...")
    try:
        response = requests.post(f"{base_url}/subscriptions", json={
            'user_id': user_id,
            'plan_id': 2  # 3 Hours plan
        })
        
        if response.status_code == 409:
            data = response.json()
            print("✅ Overlap prevention working correctly!")
            print(f"   Error: {data.get('error', 'N/A')}")
            print(f"   Message: {data.get('message', 'N/A')}")
            
            if 'current_subscription' in data:
                remaining = data['current_subscription']['remaining_time']
                print(f"   Remaining time: {remaining}")
        else:
            print(f"❌ Expected 409 Conflict, got {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing overlap: {e}")
    
    print("\n3. Checking user's current subscriptions...")
    try:
        response = requests.get(f"{base_url}/subscriptions/{user_id}")
        
        if response.status_code == 200:
            subscriptions = response.json()
            print(f"✅ User has {len(subscriptions)} subscription(s)")
            
            for i, sub in enumerate(subscriptions, 1):
                plan_name = sub['plan']['name']
                status = sub['status']
                expires = sub['ends_at']
                print(f"   {i}. {plan_name} - {status} (expires: {expires})")
        else:
            print(f"❌ Error fetching subscriptions: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking subscriptions: {e}")
    
    print("\n🎉 Subscription overlap prevention test completed!")

if __name__ == "__main__":
    test_subscription_overlap()
