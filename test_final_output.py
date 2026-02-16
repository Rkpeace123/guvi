#!/usr/bin/env python3
"""
Test script to demonstrate final output display in UI
Sends 10 messages to trigger auto-finalization
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"
API_KEY = "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

# Test messages simulating a scam conversation
test_messages = [
    "URGENT! Your bank account has been compromised. Call us immediately at 9876543210",
    "Yes, I'm calling from SBI fraud department. My employee ID is SBI-12345",
    "We need to verify your account. What's your account number?",
    "You can reach me at +91-9876543210 for verification",
    "Please transfer Rs 500 to verify your account to scammer@paytm",
    "Our office is located at Connaught Place, New Delhi",
    "You can also email us at fraud.dept@sbi-fake.com",
    "Click this link to verify: http://fake-sbi-verify.com/urgent",
    "Your account number ending in 1234567890 needs immediate action",
    "Final warning: Transfer to UPI ID scammer.fraud@okaxis now!"
]

def send_message(session_id, message_text, message_num):
    """Send a message to the API"""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": "scammer",
            "text": message_text,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "Web",
            "language": "English",
            "locale": "IN"
        }
    }
    
    print(f"\n{'='*60}")
    print(f"Message {message_num}/10")
    print(f"{'='*60}")
    print(f"Scammer: {message_text}")
    
    response = requests.post(f"{BASE_URL}/api/message", json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Agent: {data.get('reply', 'No reply')}")
        return True
    else:
        print(f"Error: {response.status_code}")
        return False

def view_final_output(session_id):
    """View the final output"""
    headers = {"X-API-Key": API_KEY}
    
    response = requests.get(f"{BASE_URL}/api/session/{session_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        final_output = data.get("finalOutput", {})
        
        print("\n" + "="*60)
        print("🏁 FINAL OUTPUT (Sent to GUVI)")
        print("="*60)
        print(json.dumps(final_output, indent=2))
        
        print("\n" + "="*60)
        print("📊 Summary")
        print("="*60)
        print(f"Scam Detected: {final_output.get('scamDetected')}")
        print(f"Total Messages: {final_output.get('totalMessagesExchanged')}")
        
        intel = final_output.get('extractedIntelligence', {})
        print(f"\nExtracted Intelligence:")
        print(f"  📞 Phone Numbers: {len(intel.get('phoneNumbers', []))}")
        print(f"  💳 UPI IDs: {len(intel.get('upiIds', []))}")
        print(f"  🏦 Bank Accounts: {len(intel.get('bankAccounts', []))}")
        print(f"  🔗 Phishing Links: {len(intel.get('phishingLinks', []))}")
        print(f"  📧 Email Addresses: {len(intel.get('emailAddresses', []))}")
        
        print(f"\n📝 Agent Notes:")
        print(f"  {final_output.get('agentNotes')}")
        
        return final_output
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    session_id = f"test-final-output-{int(time.time())}"
    
    print("="*60)
    print("🧪 Testing Final Output Display")
    print("="*60)
    print(f"Session ID: {session_id}")
    print(f"UI URL: {BASE_URL}/ui")
    print("\nSending 10 messages to trigger auto-finalization...")
    
    # Send all messages
    for i, message in enumerate(test_messages, 1):
        if not send_message(session_id, message, i):
            print("Failed to send message, stopping...")
            break
        time.sleep(1)  # Small delay between messages
    
    # Wait a moment for finalization
    print("\n⏳ Waiting for finalization...")
    time.sleep(2)
    
    # View final output
    final_output = view_final_output(session_id)
    
    if final_output:
        print("\n" + "="*60)
        print("✅ SUCCESS!")
        print("="*60)
        print(f"1. Open the UI: {BASE_URL}/ui")
        print(f"2. The final output is displayed in the chat")
        print(f"3. You can also view it at: {BASE_URL}/api/session/{session_id}")
        print("\nThe final output has been automatically sent to GUVI!")
