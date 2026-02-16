#!/usr/bin/env python3
"""
IMPOSSIBLE SCAM TEST - Nearly Undetectable
This simulates an EXTREMELY sophisticated scammer who:
- Acts like a genuine friend/colleague
- No financial requests at all
- No urgency, threats, or suspicious keywords
- Casual conversation that slowly extracts information
- Uses social engineering without any obvious red flags
- Could easily be mistaken for a real person
"""

import requests
import time
import json

BASE_URL = "http://localhost:8000"
API_KEY = "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

# Nearly impossible to detect - looks like a genuine conversation
impossible_scam_messages = [
    # Message 1: Friendly greeting, no business talk
    "Hey! Long time no see! How have you been? I was just thinking about you the other day.",
    
    # Message 2: Building rapport with shared memories
    "Remember that project we worked on together last year? That was crazy! By the way, I changed my phone number recently. Are you still using the same number?",
    
    # Message 3: Casual information gathering
    "Cool! I should save it. What's your number again? I lost all my contacts when my phone died last week. Such a pain!",
    
    # Message 4: More casual conversation
    "Thanks! I'll save it right now. So what have you been up to? Still working at the same place? I moved to a new company recently - much better work-life balance.",
    
    # Message 5: Subtle probing
    "That's great! Hey, I'm organizing a small reunion for our old team. I'm trying to get everyone's email addresses to send out invites. What's your current email? Still using the old one?",
    
    # Message 6: Creating false urgency (but friendly)
    "Perfect! I'll add you to the list. Oh, and we're planning to do a group gift for our old manager's birthday. We're collecting via UPI to make it easier. Do you use any UPI apps?",
    
    # Message 7: More information gathering
    "Nice! What's your UPI ID? I'll add you to the group. We're thinking of getting him something really nice. Everyone's chipping in around 500-1000 rupees.",
    
    # Message 8: Building more trust
    "Awesome! I'll send you the details later. By the way, are you on WhatsApp? I'm creating a group for the reunion planning. What's your WhatsApp number?",
    
    # Message 9: Final information gathering
    "Great! I'll add you tonight. Oh, one more thing - do you remember our old office address? I'm trying to find some old photos from that time. Was it near Connaught Place or somewhere else?",
    
    # Message 10: Friendly closing
    "Ah yes, that's right! Thanks for reminding me. Okay, I'll let you go now. I'll send you all the reunion details by email soon. Take care and let's catch up properly soon!"
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
            "channel": "WhatsApp",
            "language": "English",
            "locale": "IN"
        }
    }
    
    print(f"\n{'='*80}")
    print(f"Message {message_num}/10 - IMPOSSIBLE SCAM TEST")
    print(f"{'='*80}")
    print(f"👤 'Friend': {message_text}")
    
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
        print("🔍 DETECTION ANALYSIS - IMPOSSIBLE SCAM")
        print("="*80)
        
        # Check scam detection
        scam_detected = final_output.get('scamDetected', False)
        print(f"\n1. SCAM DETECTION:")
        if scam_detected:
            print(f"   ✅ DETECTED - System somehow identified this as a scam!")
            print(f"   Type: {session.get('scam_type', 'Unknown')}")
            print(f"   🎯 IMPRESSIVE - This was designed to be undetectable!")
        else:
            print(f"   ❌ NOT DETECTED - System did not flag this as a scam")
            print(f"   ⚠️  This is EXPECTED - This scam is nearly impossible to detect!")
            print(f"   💡 It looks like a genuine friend catching up")
        
        # Check intelligence extraction
        intel = final_output.get('extractedIntelligence', {})
        print(f"\n2. INTELLIGENCE EXTRACTION:")
        print(f"   (Note: In a real scenario, the victim would provide this info)")
        
        extracted_phones = intel.get('phoneNumbers', [])
        extracted_emails = intel.get('emailAddresses', [])
        extracted_upis = intel.get('upiIds', [])
        
        print(f"   📞 Phone Numbers: {len(extracted_phones)} extracted")
        print(f"   📧 Email Addresses: {len(extracted_emails)} extracted")
        print(f"   💳 UPI IDs: {len(extracted_upis)} extracted")
        
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
        friendly_responses = 0
        
        for msg in agent_messages:
            text = msg['text'].lower()
            # Check if agent showed suspicion
            if any(word in text for word in ['suspicious', 'verify', 'who', 'dont know', 'cant remember']):
                suspicious_responses += 1
            # Check if agent was friendly/trusting
            if any(word in text for word in ['sure', 'yeah', 'okay', 'great', 'nice', 'cool']):
                friendly_responses += 1
        
        print(f"   Suspicious responses: {suspicious_responses}/{len(agent_messages)}")
        print(f"   Friendly responses: {friendly_responses}/{len(agent_messages)}")
        
        if suspicious_responses > friendly_responses:
            print(f"   ✅ Agent maintained skepticism (good!)")
        else:
            print(f"   ⚠️  Agent was too trusting (expected for this scenario)")
        
        # Overall assessment
        print(f"\n" + "="*80)
        print("📊 DIFFICULTY ASSESSMENT")
        print("="*80)
        
        print(f"\n🎭 Why this scam is NEARLY IMPOSSIBLE to detect:")
        print(f"   1. ❌ No urgency or threats")
        print(f"   2. ❌ No financial keywords (bank, account, OTP, etc.)")
        print(f"   3. ❌ No suspicious links or domains")
        print(f"   4. ❌ Friendly, casual tone (like a real friend)")
        print(f"   5. ❌ Shared memories and context")
        print(f"   6. ❌ Legitimate reasons for asking info (reunion, gift)")
        print(f"   7. ❌ No immediate requests for money")
        print(f"   8. ❌ Uses social channels (WhatsApp)")
        
        print(f"\n🚩 Subtle red flags (very hard to detect):")
        print(f"   1. Asking for phone number (could be legitimate)")
        print(f"   2. Asking for email (could be legitimate)")
        print(f"   3. Asking for UPI ID (could be legitimate for group gift)")
        print(f"   4. Gathering multiple pieces of information")
        print(f"   5. Creating false familiarity")
        
        print(f"\n💡 How a human would fall for this:")
        print(f"   - Seems like a genuine old friend/colleague")
        print(f"   - Reunion and gift are believable scenarios")
        print(f"   - No immediate financial request")
        print(f"   - Information gathering seems innocent")
        print(f"   - Later, scammer uses this info for identity theft")
        
        # Show final output
        print(f"\n" + "="*80)
        print("📤 FINAL OUTPUT")
        print("="*80)
        print(json.dumps(final_output, indent=2))
        
        # Final verdict
        print(f"\n" + "="*80)
        print("🏆 FINAL VERDICT")
        print("="*80)
        
        if scam_detected:
            print(f"🎯 AMAZING - System detected an almost undetectable scam!")
            print(f"   This shows advanced pattern recognition capabilities.")
        else:
            print(f"✅ EXPECTED - This scam is designed to be undetectable")
            print(f"   Even humans would likely fall for this.")
            print(f"   The scammer is playing the long game - gathering info")
            print(f"   for future identity theft or targeted attacks.")
        
        print(f"\n💡 Real-world impact:")
        print(f"   - Scammer now has: phone, email, UPI ID, workplace info")
        print(f"   - Can use this for: identity theft, targeted phishing")
        print(f"   - Can impersonate victim to others")
        print(f"   - Can create convincing follow-up scams")
        
        return final_output
    else:
        print(f"❌ Error: {response.status_code}")
        return None

if __name__ == "__main__":
    session_id = f"impossible-scam-test-{int(time.time())}"
    
    print("="*80)
    print("🧪 IMPOSSIBLE SCAM TEST - NEARLY UNDETECTABLE")
    print("="*80)
    print("\n📋 TEST SCENARIO:")
    print("   - Pretends to be an old friend/colleague")
    print("   - Casual, friendly conversation")
    print("   - NO financial keywords or urgency")
    print("   - NO suspicious links or domains")
    print("   - Legitimate-sounding reasons (reunion, gift)")
    print("   - Slowly gathers personal information")
    print("   - Uses social engineering without red flags")
    print("\n🎯 CHALLENGE:")
    print("   This is DESIGNED to be undetectable!")
    print("   Even humans would likely fall for this.")
    print("   Can the AI agent maintain skepticism?")
    print(f"\n🔗 Session ID: {session_id}")
    print(f"🌐 UI URL: {BASE_URL}/ui")
    print("\n" + "="*80)
    
    # Send all messages
    for i, message in enumerate(impossible_scam_messages, 1):
        if not send_message(session_id, message, i):
            print("❌ Failed to send message, stopping...")
            break
        time.sleep(2)  # Realistic delay
    
    # Wait for finalization
    print("\n⏳ Waiting for finalization...")
    time.sleep(3)
    
    # Analyze detection
    final_output = analyze_detection(session_id)
    
    if final_output:
        print(f"\n🌐 View in UI: {BASE_URL}/ui")
        print(f"📊 View session: {BASE_URL}/api/session/{session_id}")
        print("\n" + "="*80)
        print("🎓 LESSON LEARNED")
        print("="*80)
        print("Not all scams are obvious. The most dangerous ones:")
        print("  - Build trust over time")
        print("  - Use social engineering")
        print("  - Gather information for later attacks")
        print("  - Appear completely legitimate")
        print("\nThis is why human awareness and education are crucial!")
