#!/usr/bin/env python3
"""
RED FLAG DETECTION SYSTEM
Identifies suspicious patterns and behaviors in scam conversations
"""

from typing import Dict, List
import re

class RedFlagDetector:
    """Detects red flags in scam conversations"""
    
    def __init__(self):
        self.red_flags = {
            "urgency_pressure": {
                "patterns": ["urgent", "immediately", "now", "asap", "hurry", "quick", "today", "right now"],
                "severity": "HIGH",
                "description": "Creates artificial urgency to prevent victim from thinking"
            },
            "threat_intimidation": {
                "patterns": ["blocked", "suspended", "freeze", "locked", "deactivate", "expire", "legal action", "arrest", "penalty"],
                "severity": "HIGH",
                "description": "Uses threats to scare victim into compliance"
            },
            "credential_request": {
                "patterns": ["otp", "cvv", "pin", "password", "aadhar", "pan", "account number"],
                "severity": "CRITICAL",
                "description": "Requests sensitive credentials that legitimate entities never ask for"
            },
            "money_request": {
                "patterns": ["send money", "transfer", "pay", "deposit", "registration fee", "processing fee", "tax"],
                "severity": "CRITICAL",
                "description": "Requests money transfer, a clear scam indicator"
            },
            "suspicious_links": {
                "patterns": ["http://", "https://", "bit.ly", "tinyurl", "click here", "link"],
                "severity": "HIGH",
                "description": "Contains suspicious links that may lead to phishing sites"
            },
            "authority_impersonation": {
                "patterns": ["bank officer", "police", "government", "tax department", "cyber cell", "rbi", "income tax"],
                "severity": "HIGH",
                "description": "Impersonates authority figures to gain trust"
            },
            "too_good_to_be_true": {
                "patterns": ["won", "winner", "prize", "lottery", "cashback", "refund", "free", "guaranteed"],
                "severity": "MEDIUM",
                "description": "Offers unrealistic rewards or benefits"
            },
            "information_harvesting": {
                "patterns": ["verify your", "confirm your", "update your", "provide your", "share your"],
                "severity": "MEDIUM",
                "description": "Attempts to harvest personal information"
            },
            "no_verification_offered": {
                "patterns": ["don't call", "don't visit", "only through this", "secret", "confidential"],
                "severity": "HIGH",
                "description": "Discourages victim from verifying through official channels"
            },
            "grammar_spelling_errors": {
                "patterns": [],  # Detected through analysis
                "severity": "LOW",
                "description": "Poor grammar or spelling typical of scam messages"
            }
        }
    
    def detect_red_flags(self, message: str, conversation_history: List[Dict] = None) -> Dict:
        """Detect all red flags in a message"""
        
        msg_lower = message.lower()
        detected_flags = []
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        # Check each red flag category
        for flag_name, flag_data in self.red_flags.items():
            patterns = flag_data["patterns"]
            
            # Check if any pattern matches
            matches = [p for p in patterns if p in msg_lower]
            
            if matches:
                detected_flags.append({
                    "flag": flag_name,
                    "severity": flag_data["severity"],
                    "description": flag_data["description"],
                    "matched_patterns": matches
                })
                severity_counts[flag_data["severity"]] += 1
        
        # Calculate overall risk score
        risk_score = (
            severity_counts["CRITICAL"] * 10 +
            severity_counts["HIGH"] * 5 +
            severity_counts["MEDIUM"] * 2 +
            severity_counts["LOW"] * 1
        )
        risk_score = min(risk_score / 30.0, 1.0)  # Normalize to 0-1
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "CRITICAL"
        elif risk_score >= 0.5:
            risk_level = "HIGH"
        elif risk_score >= 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        # Analyze conversation patterns if history provided
        conversation_flags = []
        if conversation_history:
            conversation_flags = self._analyze_conversation_patterns(conversation_history)
        
        return {
            "red_flags": detected_flags,
            "conversation_flags": conversation_flags,
            "severity_counts": severity_counts,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "total_flags": len(detected_flags) + len(conversation_flags)
        }
    
    def _analyze_conversation_patterns(self, history: List[Dict]) -> List[Dict]:
        """Analyze conversation patterns for red flags"""
        
        flags = []
        scammer_messages = [m for m in history if m.get("sender") == "scammer"]
        
        if len(scammer_messages) < 2:
            return flags
        
        # Check for escalating urgency
        urgency_words = ["urgent", "immediately", "now", "asap", "hurry"]
        urgency_count = sum(1 for m in scammer_messages if any(w in m.get("text", "").lower() for w in urgency_words))
        
        if urgency_count >= 2:
            flags.append({
                "flag": "escalating_pressure",
                "severity": "HIGH",
                "description": f"Scammer repeatedly emphasizes urgency ({urgency_count} times)"
            })
        
        # Check for multiple credential requests
        credential_words = ["otp", "password", "pin", "cvv", "account"]
        credential_requests = sum(1 for m in scammer_messages if any(w in m.get("text", "").lower() for w in credential_words))
        
        if credential_requests >= 2:
            flags.append({
                "flag": "persistent_credential_harvesting",
                "severity": "CRITICAL",
                "description": f"Multiple attempts to obtain credentials ({credential_requests} times)"
            })
        
        # Check for changing story
        if len(scammer_messages) >= 3:
            first_msg = scammer_messages[0].get("text", "").lower()
            last_msg = scammer_messages[-1].get("text", "").lower()
            
            # Simple check: if topics change drastically
            first_topics = set(["bank", "upi", "account", "kyc", "prize", "lottery", "job", "tax"])
            first_mentioned = [t for t in first_topics if t in first_msg]
            last_mentioned = [t for t in first_topics if t in last_msg]
            
            if first_mentioned and last_mentioned and not any(t in last_mentioned for t in first_mentioned):
                flags.append({
                    "flag": "inconsistent_narrative",
                    "severity": "HIGH",
                    "description": "Scammer's story changes during conversation"
                })
        
        return flags
    
    def generate_red_flag_summary(self, detection_result: Dict) -> str:
        """Generate human-readable summary of red flags"""
        
        if detection_result["total_flags"] == 0:
            return "No red flags detected."
        
        summary_parts = []
        summary_parts.append(f"Risk Level: {detection_result['risk_level']} ({detection_result['risk_score']:.0%})")
        summary_parts.append(f"Total Flags: {detection_result['total_flags']}")
        
        # List critical and high severity flags
        critical_high = [f for f in detection_result["red_flags"] if f["severity"] in ["CRITICAL", "HIGH"]]
        if critical_high:
            summary_parts.append("Critical Issues:")
            for flag in critical_high:
                summary_parts.append(f"  - {flag['description']}")
        
        return " | ".join(summary_parts)
