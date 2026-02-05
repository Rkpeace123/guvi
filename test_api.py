#!/usr/bin/env python3
"""
Test script for the Agentic Honeypot API
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = os.getenv('API_SECRET_KEY', 'test-key')

def test_health():
    """Test health endpoint"""
    print("🧪 Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}\n")
    return response.status_code == 200

def test_scam_message():
    """Test with a scam message"""
    print("🧪 Testing scam detection...")
    
    payload = {
        "sessionId": "test-session-1",
        "message": {
            "sender": "scammer",
            "text": "URGENT! Your bank account will be blocked today. Call +91-9876543210 immediately or verify at http://fake-bank.com"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    response = requests.post(
        f"{BASE_URL}/api/message",
        json=payload,
        headers=headers
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_normal_message():
    """Test with a normal message"""
    print("🧪 Testing normal message...")
    
    payload = {
        "sessionId": "test-session-2",
        "message": {
            "sender": "user",
            "text": "Hello, how are you today?"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    response = requests.post(
        f"{BASE_URL}/api/message",
        json=payload,
        headers=headers
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_conversation():
    """Test a full conversation"""
    print("🧪 Testing full conversation...")
    
    session_id = "test-conversation-1"
    messages = [
        "Your account has been suspended. Verify immediately.",
        "Click this link to verify: http://fake-bank.com",
        "Send Rs 100 to UPI: scammer@paytm to unlock your account",
        "Call our support at 9876543210 now!"
    ]
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    for i, msg in enumerate(messages, 1):
        print(f"   Message {i}: {msg[:50]}...")
        
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": msg
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/message",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            reply = response.json().get('reply', '')
            print(f"   Reply: {reply}\n")
        else:
            print(f"   Error: {response.status_code}\n")
            return False
    
    return True

def test_sessions():
    """Test sessions endpoint"""
    print("🧪 Testing sessions endpoint...")
    
    headers = {
        "x-api-key": API_KEY
    }
    
    response = requests.get(
        f"{BASE_URL}/api/sessions",
        headers=headers
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("="*60)
    print("🍯 Testing Ultimate Agentic Honeypot API")
    print("="*60)
    print()
    
    # Check if server is running
    try:
        requests.get(BASE_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running!")
        print("   Start the server with: python honeypot.py")
        return
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Scam Detection", test_scam_message()))
    results.append(("Normal Message", test_normal_message()))
    results.append(("Full Conversation", test_conversation()))
    results.append(("Sessions List", test_sessions()))
    
    # Summary
    print("="*60)
    print("📊 Test Results")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print()
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()
