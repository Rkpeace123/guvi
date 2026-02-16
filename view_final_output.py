#!/usr/bin/env python3
"""View the final output for a session"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"
API_KEY = "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

def view_sessions():
    """View all sessions"""
    headers = {"x-api-key": API_KEY}
    
    response = requests.get(f"{BASE_URL}/api/sessions", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("="*60)
        print("📊 All Sessions")
        print("="*60)
        print(json.dumps(data, indent=2))
        print()
        
        # Show session IDs
        if data.get("sessions"):
            print("Session IDs:")
            for sid in data["sessions"].keys():
                print(f"  - {sid}")
        
        return list(data["sessions"].keys())
    else:
        print(f"Error: {response.status_code}")
        return []

def view_session_details(session_id):
    """View detailed session info including final output"""
    headers = {"x-api-key": API_KEY}
    
    # First, try to get session details
    response = requests.get(f"{BASE_URL}/api/session/{session_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        print("\n" + "="*60)
        print(f"📋 Session Details: {session_id}")
        print("="*60)
        
        # Show session info
        session = data.get("session", {})
        print(f"\n🔍 Session Info:")
        print(f"  Scam Detected: {session.get('scam_detected')}")
        print(f"  Messages: {len(session.get('messages', []))}")
        print(f"  Finalized: {session.get('finalized')}")
        
        # Show intelligence
        intel = session.get("intelligence", {})
        print(f"\n📱 Extracted Intelligence:")
        if intel.get("phoneNumbers"):
            print(f"  Phone Numbers: {intel['phoneNumbers']}")
        if intel.get("upiIds"):
            print(f"  UPI IDs: {intel['upiIds']}")
        if intel.get("bankAccounts"):
            print(f"  Bank Accounts: {intel['bankAccounts']}")
        if intel.get("phishingLinks"):
            print(f"  Phishing Links: {intel['phishingLinks']}")
        if intel.get("emailAddresses"):
            print(f"  Email Addresses: {intel['emailAddresses']}")
        
        # Show final output
        final_output = data.get("finalOutput", {})
        if final_output:
            print("\n" + "="*60)
            print("📤 FINAL OUTPUT (Sent to GUVI)")
            print("="*60)
            print(json.dumps(final_output, indent=2))
        
        return final_output
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    # List all sessions
    session_ids = view_sessions()
    
    # If session ID provided, show details
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
        view_session_details(session_id)
    elif session_ids:
        # Show details of first session
        print(f"\n💡 To view details, run: python view_final_output.py {session_ids[0]}")
        print("\nShowing details of first session...\n")
        view_session_details(session_ids[0])
