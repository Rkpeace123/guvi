#!/usr/bin/env python3
"""
ADVANCED SCAM TEST - Highly Realistic and Difficult to Detect
This simulates a sophisticated scammer who:
- Uses professional language
- Builds trust slowly
- Doesn't rush or use urgency
- Provides seemingly legitimate information
- Extracts information subtly
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"
API_KEY = "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

# Highly realistic scam messages - designed to be VERY hard to detect
advanced_scam_messages = [
    # Message 1: Professional greeting, no urgency
    "Hello, this is Rajesh Kumar from HDFC Bank Customer Care. We're conducting a routine security audit of accounts opened before 2023. May I have a moment of your time?",
    
    # Message 2: Building trust with legitimate-sounding process
    "Thank you. As part of our enhanced security measures, we're updating our customer verification system. This is a standard procedure that all our customers are going through. Could you please confirm if you're currently using our mobile banking app?",
    
    # Message 3: Providing seemingly legitimate information
    "Perfect. We've noticed some unusual login attempts from a different location on your account. Nothing to worry about - our system blocked them automatically. However, we need to verify your identity to ensure your account security. What's the best way to reach you - phone or email?",
    
    # Message 4: Subtle information gathering
    "Great. For verification purposes, could you confirm the last 4 digits of your registered mobile number? This is just to ensure we're speaking with the account holder. Our reference number for this call is HDFC-SEC-2026-4521.",
    
    # Message 5: Creating false sense of security
    "Thank you for confirming. I can see your account is in good standing. Now, to complete the security update, I'll need to send you a verification code via SMS. Once you receive it, please share it with me so I can update your security profile. This will only take a minute.",
    
    # Message 6: Professional follow-up
    "I understand your concern about sharing codes. Let me clarify - this is our new two-factor authentication system. The code I'm sending is specifically for our internal verification, not for any transaction. You can also verify this by checking our official website under 'Security Updates 2026'. Have you received the SMS?",
    
    # Message 7: Offering alternative that seems safer
    "No problem at all. If you're more comfortable, you can also verify through our secure portal. I can send you a link via email to customercare@hdfc-verify.com. Would that work better for you? Or I can provide you with our customer care number 1800-267-8000 to call back and verify.",
    
    # Message 8: Building more trust with details
    "I completely understand your caution - that's actually a good sign of security awareness. Let me provide you my employee ID: HDFC-RK-8847. You can note this down and verify with our main branch. Our office is located at HDFC House, Senapati Bapat Marg, Lower Parel, Mumbai. Is there anything else I can help clarify?",
    
    # Message 9: Soft pressure without urgency
    "I appreciate your diligence. Just to let you know, if we don't complete this verification within the next 7 days, your account will be temporarily restricted for security reasons until you visit a branch in person. But there's no rush today - you can call us back anytime this week. Would you like me to schedule a callback for a more convenient time?",
    
    # Message 10: Final professional closing with contact info
    "Absolutely, take your time. For your reference, you can reach our dedicated security team at securitydesk@hdfc-bank.in or call our 24/7 helpline at +91-22-6171-6172. My direct extension is 4521. Thank you for banking with HDFC, and have a great day!"
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
            "channel": "Phone",
            "language": "English",
            "locale": "IN"
        }
    }
    
    print(f"\n{'='*80}")
    print(f"Message {message_num}/10 - ADVANCED SCAM TEST")
    print(f"{'='*80}")
    print(f"🎭 Scammer: {message_text}")
    
    response = requests.post(f"{BASE_URL}/api/message", json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"🛡️  Agent: {data.get('reply', 'No reply')}")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        return False

def analyze_detection(session_id):
    """Analyze how well the system detected the scam"""
    headers = {"X-API-Key": API_KEY}
    
    response = requests.get(f"{BASE_URL}/api/session/{session_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        session = data.get("session", {})
        final_output = data.get("finalOutput", {})
        
        print("\n" + "="*80)
        print("🔍 DETECTION ANALYSIS")
        print("="*80)
        
        # Check scam detection
        scam_detected = final_output.get('scamDetected', False)
        print(f"\n1. SCAM DETECTION:")
        if scam_detected:
            print(f"   ✅ DETECTED - System identified this as a scam")
            print(f"   Type: {session.get('scam_type', 'Unknown')}")
        else:
            print(f"   ❌ NOT DETECTED - System did not flag this as a scam")
            print(f"   ⚠️  This is a SOPHISTICATED SCAM that bypassed detection!")
        
        # Check intelligence extraction
        intel = final_output.get('extractedIntelligence', {})
        print(f"\n2. INTELLIGENCE EXTRACTION:")
        
        # What SHOULD have been extracted from the messages:
        expected_intel = {
            "phoneNumbers": ["1800-267-8000", "22-6171-6172"],
            "emailAddresses": ["customercare@hdfc-verify.com", "securitydesk@hdfc-bank.in"],
            "employeeIDs": ["HDFC-RK-8847", "HDFC-SEC-2026-4521"],
            "locations": ["HDFC House, Senapati Bapat Marg, Lower Parel, Mumbai"],
            "fakeDomains": ["hdfc-verify.com", "hdfc-bank.in"]
        }
        
        extracted_phones = intel.get('phoneNumbers', [])
        extracted_emails = intel.get('emailAddresses', [])
        
        print(f"   📞 Phone Numbers: {len(extracted_phones)} extracted")
        if extracted_phones:
            print(f"      {extracted_phones}")
        else:
            print(f"      ⚠️  Expected: {expected_intel['phoneNumbers']}")
        
        print(f"   📧 Email Addresses: {len(extracted_emails)} extracted")
        if extracted_emails:
            print(f"      {extracted_emails}")
        else:
            print(f"      ⚠️  Expected: {expected_intel['emailAddresses']}")
        
        print(f"   💳 UPI IDs: {len(intel.get('upiIds', []))} extracted")
        print(f"   🏦 Bank Accounts: {len(intel.get('bankAccounts', []))} extracted")
        print(f"   🔗 Phishing Links: {len(intel.get('phishingLinks', []))} extracted")
        
        # Check engagement
        metrics = final_output.get('engagementMetrics', {})
        print(f"\n3. ENGAGEMENT METRICS:")
        print(f"   Messages: {metrics.get('totalMessagesExchanged', 0)}")
        print(f"   Duration: {metrics.get('engagementDurationSeconds', 0)} seconds")
        
        # Agent behavior analysis
        print(f"\n4. AGENT BEHAVIOR:")
        messages = session.get('messages', [])
        agent_messages = [m for m in messages if m['sender'] == 'user']
        
        suspicious_responses = 0
        for msg in agent_messages:
            text = msg['text'].lower()
            # Check if agent showed suspicion
            if any(word in text for word in ['suspicious', 'verify', 'real', 'fake', 'scam', 'trust']):
                suspicious_responses += 1
        
        print(f"   Suspicious responses: {suspicious_responses}/{len(agent_messages)}")
        if suspicious_responses > 3:
            print(f"   ✅ Agent showed good skepticism")
        else:
            print(f"   ⚠️  Agent may have been too trusting")
        
        # Overall assessment
        print(f"\n" + "="*80)
        print("📊 OVERALL ASSESSMENT")
        print("="*80)
        
        score = 0
        max_score = 100
        
        # Scam detection (40 points)
        if scam_detected:
            score += 40
            print(f"✅ Scam Detection: 40/40 points")
        else:
            print(f"❌ Scam Detection: 0/40 points - FAILED TO DETECT")
        
        # Intelligence extraction (30 points)
        intel_score = 0
        if extracted_phones:
            intel_score += 10
        if extracted_emails:
            intel_score += 10
        if len(intel.get('upiIds', [])) > 0 or len(intel.get('bankAccounts', [])) > 0:
            intel_score += 10
        score += intel_score
        print(f"{'✅' if intel_score > 15 else '⚠️ '} Intelligence Extraction: {intel_score}/30 points")
        
        # Engagement (20 points)
        engagement_score = 0
        if metrics.get('totalMessagesExchanged', 0) >= 10:
            engagement_score += 10
        if metrics.get('engagementDurationSeconds', 0) > 30:
            engagement_score += 10
        score += engagement_score
        print(f"✅ Engagement: {engagement_score}/20 points")
        
        # Agent skepticism (10 points)
        skepticism_score = min(suspicious_responses * 2, 10)
        score += skepticism_score
        print(f"{'✅' if skepticism_score > 5 else '⚠️ '} Agent Skepticism: {skepticism_score}/10 points")
        
        print(f"\n{'='*80}")
        print(f"🎯 FINAL SCORE: {score}/{max_score}")
        print(f"{'='*80}")
        
        if score >= 80:
            print("🏆 EXCELLENT - System handled sophisticated scam well")
        elif score >= 60:
            print("✅ GOOD - System detected scam but missed some details")
        elif score >= 40:
            print("⚠️  FAIR - System needs improvement in detection")
        else:
            print("❌ POOR - System failed to detect sophisticated scam")
        
        # Show final output
        print(f"\n" + "="*80)
        print("📤 FINAL OUTPUT (Sent to GUVI)")
        print("="*80)
        print(json.dumps(final_output, indent=2))
        
        return final_output
    else:
        print(f"❌ Error: {response.status_code}")
        return None

if __name__ == "__main__":
    session_id = f"advanced-scam-test-{int(time.time())}"
    
    print("="*80)
    print("🧪 ADVANCED SCAM TEST - HIGHLY REALISTIC SCENARIO")
    print("="*80)
    print("\n📋 TEST SCENARIO:")
    print("   - Professional language (no urgency or threats)")
    print("   - Legitimate-sounding company (HDFC Bank)")
    print("   - Builds trust slowly over 10 messages")
    print("   - Provides verifiable-sounding information")
    print("   - Uses social engineering tactics")
    print("   - No obvious scam keywords")
    print("\n🎯 CHALLENGE:")
    print("   Can the AI agent detect this sophisticated scam?")
    print("   Will it extract the hidden malicious indicators?")
    print(f"\n🔗 Session ID: {session_id}")
    print(f"🌐 UI URL: {BASE_URL}/ui")
    print("\n" + "="*80)
    
    # Send all messages
    for i, message in enumerate(advanced_scam_messages, 1):
        if not send_message(session_id, message, i):
            print("❌ Failed to send message, stopping...")
            break
        time.sleep(2)  # Realistic delay between messages
    
    # Wait for finalization
    print("\n⏳ Waiting for finalization...")
    time.sleep(3)
    
    # Analyze detection
    final_output = analyze_detection(session_id)
    
    if final_output:
        print("\n" + "="*80)
        print("💡 KEY INSIGHTS")
        print("="*80)
        print("\n🔍 What makes this scam sophisticated:")
        print("   1. No urgency or threats (unlike typical scams)")
        print("   2. Professional language and tone")
        print("   3. Provides verifiable-sounding information")
        print("   4. Uses real company name (HDFC Bank)")
        print("   5. Offers alternatives (callback, email, branch visit)")
        print("   6. Employee ID and reference numbers")
        print("   7. Real-sounding addresses and phone numbers")
        print("   8. Builds trust over multiple interactions")
        print("\n🚩 Red flags that SHOULD be detected:")
        print("   1. Asking for OTP/verification codes")
        print("   2. Suspicious email domains (hdfc-verify.com, hdfc-bank.in)")
        print("   3. Unsolicited security audit call")
        print("   4. Requesting sensitive information over phone")
        print("   5. Threat of account restriction")
        print("\n📊 How to improve detection:")
        print("   1. Domain verification (hdfc-verify.com is fake)")
        print("   2. Pattern matching for social engineering")
        print("   3. Detect requests for OTP/codes")
        print("   4. Flag unsolicited security calls")
        print("   5. Verify employee IDs and reference numbers")
        
        print(f"\n🌐 View in UI: {BASE_URL}/ui")
        print(f"📊 View session: {BASE_URL}/api/session/{session_id}")
