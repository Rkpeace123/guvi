#!/usr/bin/env python3
"""Quick test for enhanced intelligence extractor"""

from enhanced_extractor import EnhancedIntelligenceExtractor

# Initialize extractor
extractor = EnhancedIntelligenceExtractor()

# Test messages with various intelligence types
test_messages = [
    "Your account is blocked! Call 9876543210 immediately to verify.",
    "Send money to scammer@paytm UPI ID to unlock your account.",
    "Transfer to bank account 1234567890123456 ASAP!",
    "Click this link: http://fake-bank.com/verify to update KYC.",
    "Contact us at fraud@scammer.com for more details.",
    "Call +91-9876543210 or visit www.phishing-site.com",
    "Send OTP to 98765 43210 and UPI to user.name@ybl",
]

print("="*80)
print("TESTING ENHANCED INTELLIGENCE EXTRACTOR")
print("="*80)

for i, msg in enumerate(test_messages, 1):
    print(f"\n{i}. Message: {msg}")
    intel = extractor.extract(msg)
    
    if intel["phoneNumbers"]:
        print(f"   📱 Phones: {intel['phoneNumbers']}")
    if intel["upiIds"]:
        print(f"   💳 UPIs: {intel['upiIds']}")
    if intel["bankAccounts"]:
        print(f"   🏦 Accounts: {intel['bankAccounts']}")
    if intel["phishingLinks"]:
        print(f"   🔗 Links: {intel['phishingLinks']}")
    if intel["emailAddresses"]:
        print(f"   📧 Emails: {intel['emailAddresses']}")
    
    if not any(intel.values()):
        print("   ❌ No intelligence extracted")

print("\n" + "="*80)
print("TEST COMPLETE")
print("="*80)
