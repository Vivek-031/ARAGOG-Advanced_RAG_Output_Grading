#!/usr/bin/env python3
"""
Test script to check current behavior of the system
"""

import requests
import json
import time

def test_endpoints():
    base_url = "http://localhost:5000"
    
    print("="*80)
    print("TESTING CURRENT BEHAVIOR")
    print("="*80)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test 2: Get sessions for user 24
    try:
        response = requests.get(f"{base_url}/api/chat/sessions/24")
        print(f"\nSessions for user 24: {response.status_code}")
        if response.status_code == 200:
            sessions = response.json()
            print(f"Found {len(sessions)} sessions")
            for session in sessions:
                print(f"  - {session['session_id']}: {session['title']} ({session['message_count']} messages)")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Sessions test failed: {e}")
    
    # Test 3: Get messages for first session
    try:
        response = requests.get(f"{base_url}/api/chat/sessions/24")
        if response.status_code == 200:
            sessions = response.json()
            if sessions:
                first_session = sessions[0]['session_id']
                response = requests.get(f"{base_url}/api/chat/sessions/{first_session}/messages")
                print(f"\nMessages for session {first_session}: {response.status_code}")
                if response.status_code == 200:
                    messages = response.json()
                    print(f"Found {len(messages)} messages")
                    for msg in messages[:3]:  # Show first 3
                        print(f"  - {msg['role']}: {msg['message'][:50]}...")
                else:
                    print(f"Error: {response.text}")
    except Exception as e:
        print(f"Messages test failed: {e}")
    
    # Test 4: Test query types
    test_queries = [
        {"query": "What is diabetes?", "type": "medical"},
        {"query": "What is 2+2?", "type": "general"},
        {"query": "xyz", "type": "irrelevant"}
    ]
    
    print(f"\n{'='*80}")
    print("TESTING QUERY TYPES")
    print("="*80)
    
    for test in test_queries:
        try:
            payload = {
                "query": test["query"],
                "user_id": 24,
                "session_id": f"test_{int(time.time())}"
            }
            response = requests.post(f"{base_url}/api/ask", json=payload)
            print(f"\nQuery: '{test['query']}' (expected: {test['type']})")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Mode: {result.get('mode', 'unknown')}")
                print(f"Is Medical: {result.get('is_medical', 'unknown')}")
                print(f"Answer: {result.get('answer', '')[:100]}...")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Query test failed: {e}")

if __name__ == "__main__":
    test_endpoints()
