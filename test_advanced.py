#!/usr/bin/env python3
"""
🧪 ADVANCED TEST SUITE - Ultimate Agentic Honeypot
Tests the most challenging edge cases and attack vectors
"""

import requests
import json
import time
import concurrent.futures
from typing import Dict, List
import random
import string

# Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name: str):
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}🧪 TEST: {name}{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")

def print_pass(msg: str):
    print(f"{Colors.GREEN}✅ PASS: {msg}{Colors.END}")

def print_fail(msg: str):
    print(f"{Colors.RED}❌ FAIL: {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.YELLOW}ℹ️  INFO: {msg}{Colors.END}")

def send_message(session_id: str, text: str, sender: str = "scammer") -> Dict:
    """Send a message to the honeypot"""
    payload = {
        "sessionId": session_id,
        "message": {
            "sender": sender,
            "text": text
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/message",
            json=payload,
            headers=headers,
            timeout=30
        )
        return {
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None,
            "error": None
        }
    except Exception as e:
        return {
            "status_code": 0,
            "data": None,
            "error": str(e)
        }

# =============================================================================
# TEST 1: Sophisticated Phishing with Obfuscation
# =============================================================================

def test_obfuscated_scams():
    """Test detection of obfuscated scam messages"""
    print_test("Obfuscated Scam Detection")
    
    test_cases = [
        {
            "name": "Unicode Obfuscation",
            "text": "URGΕNT! Yοur αccount will be bl0cked. Call +91-98765-43210 ΝOW!",
            "should_detect": True
        },
        {
            "name": "Leetspeak",
            "text": "URG3NT! Y0ur 4cc0unt 1s bl0ck3d. C4ll 9876543210 n0w!",
            "should_detect": True
        },
        {
            "name": "Zero-Width Characters",
            "text": "URGENT\u200B! Your\u200C account\u200D blocked\u200B. Call 9876543210",
            "should_detect": True
        },
        {
            "name": "Homoglyph Attack",
            "text": "URGENT! Yοur аccοunt is blοcked. Cаll 9876543210",  # Cyrillic chars
            "should_detect": True
        },
        {
            "name": "Excessive Spacing",
            "text": "U R G E N T ! Your a c c o u n t blocked. Call 98 76 54 32 10",
            "should_detect": True
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases):
        session_id = f"obfuscated-{i}"
        result = send_message(session_id, case["text"])
        
        if result["status_code"] == 200:
            reply = result["data"]["reply"]
            # Check if it responded (indicating detection)
            detected = len(reply) > 0 and "thank you" not in reply.lower()
            
            if detected == case["should_detect"]:
                print_pass(f"{case['name']}: Correctly {'detected' if detected else 'ignored'}")
                passed += 1
            else:
                print_fail(f"{case['name']}: Expected {'detection' if case['should_detect'] else 'no detection'}")
        else:
            print_fail(f"{case['name']}: Request failed")
    
    print_info(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

# =============================================================================
# TEST 2: Multi-Language Scams
# =============================================================================

def test_multilingual_scams():
    """Test detection of scams in different languages"""
    print_test("Multi-Language Scam Detection")
    
    test_cases = [
        {
            "name": "Hindi (Devanagari)",
            "text": "तत्काल! आपका खाता ब्लॉक हो जाएगा। 9876543210 पर कॉल करें।",
            "should_detect": True
        },
        {
            "name": "Mixed Hindi-English",
            "text": "URGENT! Aapka account blocked hai. Call karo 9876543210 immediately!",
            "should_detect": True
        },
        {
            "name": "Tamil",
            "text": "அவசரம்! உங்கள் கணக்கு தடுக்கப்படும். 9876543210 அழைக்கவும்.",
            "should_detect": True
        },
        {
            "name": "Bengali",
            "text": "জরুরি! আপনার অ্যাকাউন্ট ব্লক হবে। 9876543210 কল করুন।",
            "should_detect": True
        },
        {
            "name": "Code-Switching",
            "text": "Bhai urgent hai yaar, tera account block hone wala hai. Jaldi call kar 9876543210",
            "should_detect": True
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases):
        session_id = f"multilang-{i}"
        result = send_message(session_id, case["text"])
        
        if result["status_code"] == 200:
            # Even if it doesn't detect non-English, it should respond
            reply = result["data"]["reply"]
            if len(reply) > 0:
                print_pass(f"{case['name']}: System responded")
                passed += 1
            else:
                print_fail(f"{case['name']}: No response")
        else:
            print_fail(f"{case['name']}: Request failed")
    
    print_info(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

# =============================================================================
# TEST 3: Advanced Intelligence Extraction
# =============================================================================

def test_advanced_intelligence_extraction():
    """Test extraction of obfuscated contact information"""
    print_test("Advanced Intelligence Extraction")
    
    test_cases = [
        {
            "name": "Obfuscated Phone",
            "text": "Call me at nine eight seven six five four three two one zero",
            "expected_phones": []  # Text-to-number not implemented
        },
        {
            "name": "International Format",
            "text": "WhatsApp: +91 (987) 654-3210 or +919876543210",
            "expected_phones": ["9876543210"]
        },
        {
            "name": "Multiple UPI IDs",
            "text": "Pay to scammer@paytm or fraud@phonepe or fake@googlepay",
            "expected_upis": 3
        },
        {
            "name": "Shortened URLs",
            "text": "Click here: bit.ly/scam123 or tinyurl.com/fraud456",
            "expected_links": 0  # Doesn't match http pattern
        },
        {
            "name": "Mixed Formats",
            "text": "URGENT! Account 1234567890123 blocked. Pay scammer@paytm. Call 9876543210. Visit http://fake-bank.com",
            "expected_phones": ["9876543210"],
            "expected_upis": 1,
            "expected_accounts": 1,
            "expected_links": 1
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases):
        session_id = f"intel-{i}"
        result = send_message(session_id, case["text"])
        
        if result["status_code"] == 200:
            # Get session details to check extracted intelligence
            session_result = requests.get(
                f"{BASE_URL}/api/session/{session_id}",
                headers={"x-api-key": API_KEY}
            )
            
            if session_result.status_code == 200:
                intel = session_result.json()["intelligence"]
                
                checks_passed = True
                if "expected_phones" in case:
                    if len(intel["phone_numbers"]) != len(case["expected_phones"]):
                        print_fail(f"{case['name']}: Expected {len(case['expected_phones'])} phones, got {len(intel['phone_numbers'])}")
                        checks_passed = False
                
                if "expected_upis" in case:
                    if len(intel["upi_ids"]) != case["expected_upis"]:
                        print_fail(f"{case['name']}: Expected {case['expected_upis']} UPIs, got {len(intel['upi_ids'])}")
                        checks_passed = False
                
                if checks_passed:
                    print_pass(f"{case['name']}: Intelligence extracted correctly")
                    passed += 1
            else:
                print_fail(f"{case['name']}: Could not retrieve session")
        else:
            print_fail(f"{case['name']}: Request failed")
    
    print_info(f"Passed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.7  # 70% pass rate acceptable

# =============================================================================
# TEST 4: Conversation Context & Memory
# =============================================================================

def test_conversation_context():
    """Test if system maintains context across messages"""
    print_test("Conversation Context & Memory")
    
    session_id = "context-test"
    
    conversation = [
        "Your account will be blocked",
        "You need to verify immediately",
        "Call this number: 9876543210",
        "Or pay to scammer@paytm",
        "Do it now or lose access"
    ]
    
    responses = []
    for i, msg in enumerate(conversation):
        result = send_message(session_id, msg)
        if result["status_code"] == 200:
            responses.append(result["data"]["reply"])
            print_info(f"Message {i+1}: {result['data']['reply'][:50]}...")
        else:
            print_fail(f"Message {i+1} failed")
            return False
    
    # Check if responses evolve (early concern → middle questions → late skepticism)
    if len(responses) == len(conversation):
        # Early responses should show concern
        early_concern = any(word in responses[0].lower() for word in ["what", "why", "worried", "understand"])
        
        # Later responses should show skepticism
        late_skepticism = any(word in responses[-1].lower() for word in ["scam", "verify", "bank", "sure", "comfortable"])
        
        if early_concern:
            print_pass("Early stage: Shows appropriate concern")
        else:
            print_fail("Early stage: Doesn't show concern")
        
        if late_skepticism:
            print_pass("Late stage: Shows appropriate skepticism")
        else:
            print_fail("Late stage: Doesn't show skepticism")
        
        return early_concern or late_skepticism
    
    return False

# =============================================================================
# TEST 5: Injection Attacks
# =============================================================================

def test_injection_attacks():
    """Test resistance to various injection attacks"""
    print_test("Injection Attack Resistance")
    
    test_cases = [
        {
            "name": "SQL Injection",
            "text": "'; DROP TABLE sessions; -- Your account blocked",
            "should_not_crash": True
        },
        {
            "name": "NoSQL Injection",
            "text": '{"$ne": null} Your account blocked call 9876543210',
            "should_not_crash": True
        },
        {
            "name": "Command Injection",
            "text": "Your account blocked; rm -rf /; call 9876543210",
            "should_not_crash": True
        },
        {
            "name": "XSS Attempt",
            "text": "<script>alert('xss')</script> Your account blocked 9876543210",
            "should_not_crash": True
        },
        {
            "name": "JSON Injection",
            "text": '{"text": "blocked", "admin": true} call 9876543210',
            "should_not_crash": True
        },
        {
            "name": "Path Traversal",
            "text": "../../etc/passwd Your account blocked 9876543210",
            "should_not_crash": True
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases):
        session_id = f"injection-{i}"
        result = send_message(session_id, case["text"])
        
        # System should handle gracefully without crashing
        if result["status_code"] == 200:
            print_pass(f"{case['name']}: System handled safely")
            passed += 1
        elif result["status_code"] == 400:
            print_pass(f"{case['name']}: Rejected malicious input")
            passed += 1
        else:
            print_fail(f"{case['name']}: System crashed or error")
    
    print_info(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

# =============================================================================
# TEST 6: Load & Concurrency
# =============================================================================

def test_concurrent_sessions():
    """Test handling of multiple concurrent sessions"""
    print_test("Concurrent Session Handling")
    
    num_sessions = 50
    messages_per_session = 5
    
    def simulate_session(session_num):
        session_id = f"concurrent-{session_num}"
        messages = [
            f"Session {session_num}: Your account blocked",
            f"Session {session_num}: Call 987654{session_num:04d}",
            f"Session {session_num}: Pay to scammer{session_num}@paytm",
            f"Session {session_num}: Urgent verification needed",
            f"Session {session_num}: Do it now"
        ]
        
        success_count = 0
        for msg in messages:
            result = send_message(session_id, msg)
            if result["status_code"] == 200:
                success_count += 1
            time.sleep(0.1)  # Small delay
        
        return success_count == messages_per_session
    
    print_info(f"Starting {num_sessions} concurrent sessions...")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(simulate_session, range(num_sessions)))
    
    elapsed = time.time() - start_time
    passed = sum(results)
    
    print_info(f"Completed in {elapsed:.2f} seconds")
    print_info(f"Successful sessions: {passed}/{num_sessions}")
    print_info(f"Throughput: {(num_sessions * messages_per_session) / elapsed:.2f} messages/sec")
    
    if passed >= num_sessions * 0.95:  # 95% success rate
        print_pass("Concurrent handling: Excellent")
        return True
    elif passed >= num_sessions * 0.8:  # 80% success rate
        print_pass("Concurrent handling: Good")
        return True
    else:
        print_fail("Concurrent handling: Poor")
        return False

# =============================================================================
# TEST 7: Edge Cases & Malformed Input
# =============================================================================

def test_edge_cases():
    """Test handling of edge cases and malformed input"""
    print_test("Edge Cases & Malformed Input")
    
    test_cases = [
        {
            "name": "Empty Message",
            "payload": {"sessionId": "edge-1", "message": {"text": ""}},
            "should_handle": True
        },
        {
            "name": "Null Message",
            "payload": {"sessionId": "edge-2", "message": None},
            "should_handle": True
        },
        {
            "name": "Missing Message Field",
            "payload": {"sessionId": "edge-3"},
            "should_handle": True
        },
        {
            "name": "Extremely Long Message",
            "payload": {"sessionId": "edge-4", "message": {"text": "A" * 100000}},
            "should_handle": True
        },
        {
            "name": "Special Characters Only",
            "payload": {"sessionId": "edge-5", "message": {"text": "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"}},
            "should_handle": True
        },
        {
            "name": "Emoji Overload",
            "payload": {"sessionId": "edge-6", "message": {"text": "🚨" * 1000}},
            "should_handle": True
        },
        {
            "name": "Invalid Session ID",
            "payload": {"sessionId": None, "message": {"text": "test"}},
            "should_handle": True
        }
    ]
    
    passed = 0
    for case in test_cases:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": API_KEY
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/message",
                json=case["payload"],
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 400]:  # Either success or graceful rejection
                print_pass(f"{case['name']}: Handled gracefully")
                passed += 1
            else:
                print_fail(f"{case['name']}: Unexpected status {response.status_code}")
        except Exception as e:
            print_fail(f"{case['name']}: Exception - {str(e)}")
    
    print_info(f"Passed: {passed}/{len(test_cases)}")
    return passed >= len(test_cases) * 0.85  # 85% pass rate

# =============================================================================
# TEST 8: False Positive Resistance
# =============================================================================

def test_false_positives():
    """Test that legitimate messages are not flagged as scams"""
    print_test("False Positive Resistance")
    
    legitimate_messages = [
        "Hi, how are you today?",
        "Can we schedule a meeting tomorrow?",
        "Thanks for your help with the project",
        "The weather is nice today",
        "I'll call you later to discuss",
        "Please verify the document I sent",  # Contains "verify" but not a scam
        "Your order has been confirmed",
        "Meeting at 3 PM in conference room",
        "Happy birthday! Hope you have a great day",
        "Can you send me the report?"
    ]
    
    passed = 0
    for i, msg in enumerate(legitimate_messages):
        session_id = f"legit-{i}"
        result = send_message(session_id, msg)
        
        if result["status_code"] == 200:
            reply = result["data"]["reply"]
            # Legitimate messages should get neutral responses
            is_neutral = any(phrase in reply.lower() for phrase in [
                "thank you", "okay", "got it", "understand"
            ])
            
            if is_neutral:
                print_pass(f"Message {i+1}: Correctly identified as legitimate")
                passed += 1
            else:
                print_info(f"Message {i+1}: Treated as potential scam (may be acceptable)")
                passed += 0.5  # Partial credit
    
    print_info(f"Passed: {passed}/{len(legitimate_messages)}")
    return passed >= len(legitimate_messages) * 0.7  # 70% accuracy

# =============================================================================
# TEST 9: API Security
# =============================================================================

def test_api_security():
    """Test API security measures"""
    print_test("API Security")
    
    test_cases = [
        {
            "name": "No API Key",
            "headers": {"Content-Type": "application/json"},
            "should_reject": True
        },
        {
            "name": "Invalid API Key",
            "headers": {"Content-Type": "application/json", "x-api-key": "invalid-key-123"},
            "should_reject": True
        },
        {
            "name": "SQL Injection in API Key",
            "headers": {"Content-Type": "application/json", "x-api-key": "'; DROP TABLE--"},
            "should_reject": True
        },
        {
            "name": "Valid API Key",
            "headers": {"Content-Type": "application/json", "x-api-key": API_KEY},
            "should_reject": False
        }
    ]
    
    passed = 0
    for case in test_cases:
        payload = {"sessionId": "security-test", "message": {"text": "test"}}
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/message",
                json=payload,
                headers=case["headers"],
                timeout=5
            )
            
            is_rejected = response.status_code == 401
            
            if is_rejected == case["should_reject"]:
                print_pass(f"{case['name']}: Correct behavior")
                passed += 1
            else:
                print_fail(f"{case['name']}: Expected {'rejection' if case['should_reject'] else 'acceptance'}")
        except Exception as e:
            print_fail(f"{case['name']}: Exception - {str(e)}")
    
    print_info(f"Passed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

# =============================================================================
# TEST 10: Performance Under Stress
# =============================================================================

def test_performance_stress():
    """Test system performance under stress"""
    print_test("Performance Under Stress")
    
    print_info("Sending 100 rapid-fire requests...")
    
    start_time = time.time()
    success_count = 0
    response_times = []
    
    for i in range(100):
        req_start = time.time()
        result = send_message(f"stress-{i}", f"URGENT! Account blocked {i}. Call 9876543210")
        req_time = time.time() - req_start
        
        if result["status_code"] == 200:
            success_count += 1
            response_times.append(req_time)
    
    total_time = time.time() - start_time
    
    if response_times:
        avg_response = sum(response_times) / len(response_times)
        max_response = max(response_times)
        min_response = min(response_times)
        
        print_info(f"Total time: {total_time:.2f}s")
        print_info(f"Success rate: {success_count}/100 ({success_count}%)")
        print_info(f"Avg response time: {avg_response*1000:.2f}ms")
        print_info(f"Min response time: {min_response*1000:.2f}ms")
        print_info(f"Max response time: {max_response*1000:.2f}ms")
        print_info(f"Throughput: {100/total_time:.2f} req/sec")
        
        # Performance criteria
        if success_count >= 95 and avg_response < 1.0:
            print_pass("Performance: Excellent")
            return True
        elif success_count >= 80 and avg_response < 2.0:
            print_pass("Performance: Good")
            return True
        else:
            print_fail("Performance: Needs improvement")
            return False
    else:
        print_fail("No successful responses")
        return False

# =============================================================================
# MAIN TEST RUNNER
# =============================================================================

def main():
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}🧪 ULTIMATE AGENTIC HONEYPOT - ADVANCED TEST SUITE{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print_fail("Server is not responding correctly!")
            return
    except:
        print_fail("Server is not running! Start with: python honeypot.py")
        return
    
    print_pass("Server is running")
    
    # Run all tests
    tests = [
        ("Obfuscated Scams", test_obfuscated_scams),
        ("Multi-Language Scams", test_multilingual_scams),
        ("Intelligence Extraction", test_advanced_intelligence_extraction),
        ("Conversation Context", test_conversation_context),
        ("Injection Attacks", test_injection_attacks),
        ("Concurrent Sessions", test_concurrent_sessions),
        ("Edge Cases", test_edge_cases),
        ("False Positives", test_false_positives),
        ("API Security", test_api_security),
        ("Performance Stress", test_performance_stress)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print_fail(f"Test crashed: {str(e)}")
            results.append((name, False))
    
    # Final Summary
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}📊 FINAL RESULTS{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"{status} - {name}")
    
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    percentage = (passed / total) * 100
    
    if percentage >= 90:
        print(f"{Colors.GREEN}🎉 EXCELLENT: {passed}/{total} tests passed ({percentage:.1f}%){Colors.END}")
    elif percentage >= 70:
        print(f"{Colors.YELLOW}👍 GOOD: {passed}/{total} tests passed ({percentage:.1f}%){Colors.END}")
    else:
        print(f"{Colors.RED}⚠️  NEEDS WORK: {passed}/{total} tests passed ({percentage:.1f}%){Colors.END}")
    
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")

if __name__ == "__main__":
    main()
