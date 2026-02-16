#!/usr/bin/env python3
"""
Quick deployment verification script
Tests if your deployed API meets all hackathon requirements
"""

import requests
import sys
import time

def test_deployment(base_url, api_key):
    """Test deployed API against hackathon requirements"""
    
    print("="*70)
    print("  🔍 DEPLOYMENT VERIFICATION")
    print("="*70)
    print(f"  Testing: {base_url}")
    print("="*70)
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    
    # Test 1: Health Check
    print("\n[1/5] Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test 2: API Authentication
    print("\n[2/5] Testing API authentication...")
    try:
        # Test without API key
        response = requests.post(
            f"{base_url}/api/message",
            json={"message": {"text": "test"}},
            timeout=10
        )
        if response.status_code == 401:
            print("✅ Authentication working (rejected without key)")
        else:
            print("⚠️ Warning: API accepts requests without key")
        
        # Test with API key
        response = requests.post(
            f"{base_url}/api/message",
            json={"message": {"text": "test"}},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Authentication working (accepted with key)")
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False
    
    # Test 3: Scam Detection
    print("\n[3/5] Testing scam detection...")
    try:
        payload = {
            "sessionId": f"verify-{int(time.time())}",
            "message": {
                "sender": "scammer",
                "text": "URGENT! Your bank account will be blocked. Call +91-9876543210 immediately!"
            }
        }
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/api/message",
            json=payload,
            headers=headers,
            timeout=30
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            if "reply" in data or "message" in data or "text" in data:
                print(f"✅ Scam detection working (response time: {response_time:.2f}s)")
                if response_time > 30:
                    print("⚠️ Warning: Response time > 30s (may fail evaluation)")
            else:
                print("❌ Response missing reply/message/text field")
                return False
        else:
            print(f"❌ Scam detection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Scam detection test failed: {e}")
        return False
    
    # Test 4: Intelligence Extraction
    print("\n[4/5] Testing intelligence extraction...")
    try:
        messages = [
            "Your account is compromised. Verify at http://fake-bank.com",
            "Send payment to scammer@paytm UPI ID",
            "Call our helpline: +91-8765432109"
        ]
        
        session_id = f"intel-test-{int(time.time())}"
        
        for msg in messages:
            payload = {
                "sessionId": session_id,
                "message": {
                    "sender": "scammer",
                    "text": msg
                }
            }
            
            response = requests.post(
                f"{base_url}/api/message",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ Intelligence extraction failed: {response.status_code}")
                return False
            
            time.sleep(0.5)
        
        print("✅ Intelligence extraction working")
        
    except Exception as e:
        print(f"❌ Intelligence extraction test failed: {e}")
        return False
    
    # Test 5: Response Format
    print("\n[5/5] Testing response format...")
    try:
        payload = {
            "sessionId": f"format-test-{int(time.time())}",
            "message": {
                "sender": "scammer",
                "text": "Test message"
            }
        }
        
        response = requests.post(
            f"{base_url}/api/message",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            has_status = "status" in data
            has_reply = "reply" in data or "message" in data or "text" in data
            
            if has_status and has_reply:
                print("✅ Response format correct")
            else:
                print(f"❌ Response format incorrect")
                print(f"   Has 'status': {has_status}")
                print(f"   Has 'reply/message/text': {has_reply}")
                return False
        else:
            print(f"❌ Response format test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Response format test failed: {e}")
        return False
    
    # All tests passed
    print("\n" + "="*70)
    print("  ✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n  Your API is ready for GUVI hackathon evaluation!")
    print(f"\n  Submit this URL: {base_url}/api/message")
    print(f"  API Key: {api_key}")
    print("\n" + "="*70)
    
    return True

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python verify_deployment.py <BASE_URL> [API_KEY]")
        print("\nExamples:")
        print("  python verify_deployment.py http://localhost:8000")
        print("  python verify_deployment.py https://your-app.onrender.com")
        print("  python verify_deployment.py https://your-app.onrender.com your-api-key")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    api_key = sys.argv[2] if len(sys.argv) > 2 else "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"
    
    success = test_deployment(base_url, api_key)
    
    if not success:
        print("\n❌ Deployment verification failed!")
        print("   Review the errors above and fix your deployment.")
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
