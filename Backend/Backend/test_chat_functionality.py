#!/usr/bin/env python3
"""
Test script to check chat history functionality thoroughly
"""

import requests
import json
import time

def test_chat_functionality():
    base_url = "http://localhost:5000"
    
    print("="*80)
    print("TESTING CHAT FUNCTIONALITY")
    print("="*80)
    
    # Test 1: Create new sessions
    print("\n1. Creating new chat sessions...")
    test_sessions = []
    
    for i in range(3):
        try:
            payload = {"user_id": 24}
            response = requests.post(f"{base_url}/api/chat/new", json=payload)
            if response.status_code == 200:
                session_data = response.json()
                session_id = session_data['session_id']
                test_sessions.append(session_id)
                print(f"  Created session {i+1}: {session_id}")
            else:
                print(f"  Error creating session {i+1}: {response.status_code}")
        except Exception as e:
            print(f"  Exception creating session {i+1}: {e}")
    
    # Test 2: Save messages to sessions
    print(f"\n2. Saving messages to {len(test_sessions)} sessions...")
    
    messages = [
        "What are the symptoms of flu?",
        "How does photosynthesis work?", 
        "What is the capital of France?"
    ]
    
    for i, session_id in enumerate(test_sessions):
        try:
            # Save user message
            payload = {
                "user_id": 24,
                "session_id": session_id,
                "role": "user",
                "message": messages[i]
            }
            response = requests.post(f"{base_url}/api/chat/save", json=payload)
            print(f"  Session {session_id} - User message: {response.status_code}")
            
            # Get AI response
            query_payload = {
                "query": messages[i],
                "user_id": 24,
                "session_id": session_id
            }
            response = requests.post(f"{base_url}/api/ask", json=query_payload)
            if response.status_code == 200:
                ai_response = response.json()
                ai_message = ai_response.get('answer', '')
                
                # Save AI message
                save_payload = {
                    "user_id": 24,
                    "session_id": session_id,
                    "role": "assistant",
                    "message": ai_message
                }
                save_response = requests.post(f"{base_url}/api/chat/save", json=save_payload)
                print(f"  Session {session_id} - AI message: {save_response.status_code}")
            
        except Exception as e:
            print(f"  Exception in session {session_id}: {e}")
    
    # Test 3: Check all sessions for user
    print(f"\n3. Checking all sessions for user 24...")
    try:
        response = requests.get(f"{base_url}/api/chat/sessions/24")
        if response.status_code == 200:
            sessions = response.json()
            print(f"  Total sessions found: {len(sessions)}")
            for session in sessions:
                print(f"    - {session['session_id']}: {session['title'][:50]}... ({session['message_count']} messages)")
        else:
            print(f"  Error: {response.status_code}")
    except Exception as e:
        print(f"  Exception: {e}")
    
    # Test 4: Retrieve messages from each session
    print(f"\n4. Retrieving messages from sessions...")
    for session_id in test_sessions:
        try:
            response = requests.get(f"{base_url}/api/chat/sessions/{session_id}/messages")
            if response.status_code == 200:
                messages = response.json()
                print(f"  Session {session_id}: {len(messages)} messages")
                for msg in messages:
                    print(f"    {msg['role']}: {msg['message'][:30]}...")
            else:
                print(f"  Error retrieving {session_id}: {response.status_code}")
        except Exception as e:
            print(f"  Exception retrieving {session_id}: {e}")
    
    # Test 5: Test persistence (simulate restart by checking data exists)
    print(f"\n5. Testing data persistence...")
    try:
        response = requests.get(f"{base_url}/api/chat/sessions/24")
        if response.status_code == 200:
            sessions = response.json()
            print(f"  Sessions persist: {len(sessions)} found")
            
            # Check total message count
            total_messages = sum(s['message_count'] for s in sessions)
            print(f"  Total messages persist: {total_messages}")
            
        else:
            print(f"  Error checking persistence: {response.status_code}")
    except Exception as e:
        print(f"  Exception checking persistence: {e}")

if __name__ == "__main__":
    test_chat_functionality()
