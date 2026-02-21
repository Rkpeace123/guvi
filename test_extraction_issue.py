#!/usr/bin/env python3
"""Test extraction with actual scam messages"""

from enhanced_extractor import EnhancedIntelligenceExtractor

extractor = EnhancedIntelligenceExtractor()

test_messages = [
    "Sure, you can call us at +91-9876543210",
    "transfer Rs.500 to scammer.fraud@fakebank",
    "send your 16‑digit account number 1234567890123456"
]

print("Testing extraction with actual scam messages:")
print("="*80)

for i, msg in enumerate(test_messages, 1):
    print(f"\n{i}. Message: {msg}")
    intel = extractor.extract(msg)
    
    print(f"   Phones: {intel['phoneNumbers']}")
    print(f"   UPIs: {intel['upiIds']}")
    print(f"   Accounts: {intel['bankAccounts']}")
    print(f"   Links: {intel['phishingLinks']}")
    print(f"   Emails: {intel['emailAddresses']}")
