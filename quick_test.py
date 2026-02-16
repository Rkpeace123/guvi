#!/usr/bin/env python3
"""Quick test of the honeypot API"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
API_KEY = "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

def test_scam_scenario():
    """Test a complete scam scenario"""
    
    session_id = f"test-{int(time.time())}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    messages = [
        "URGENT! Your bank account has been compromised. Call 9876543210 immediately!",
        "You need to verify your account by sending Rs 100 to verify@upi",
        "Click this link to verify: http://fake-bank.com/verify",
        "Send your account number and OTP to secure your account",
        "This is your last chance before we block your account permanently"
    ]
    
    print("="*60)
    print("🧪 Testing Honeypot API")
    print("="*60)
    print(f"Session ID: {session_id}\n")
    
    for i, msg in enumerate(messages, 1):
        print(f"[Turn {i}] Scammer: {msg[:60]}...")
        
        payload = {
            "sessionId": session_id,
            "message": {
                "sender": "scammer",
                "text": msg
            }
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/message",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                reply = data.get('reply', '')
                print(f"[Turn {i}] Honeypot: {reply}\n")
            else:
                print(f"❌ Error: {response.status_code}\n")
                return False
                
        except Exception as e:
            print(f"❌ Exception: {e}\n")
            return False
        
        time.sleep(1)
    
    # Get session details
    print("="*60)
    print("📊 Session Results")
    print("="*60)
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/sessions",
            headers={"x-api-key": API_KEY}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"Error getting session: {e}")
    
    return True

if __name__ == "__main__":
    test_scam_scenario()
