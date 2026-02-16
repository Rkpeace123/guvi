#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍯 ULTIMATE AGENTIC HONEY-POT (Lightweight Version)
Optimized for fast deployment without heavy AI models

Features:
- ✅ Pattern-based Scam Detection (fast, no AI models needed)
- ✅ Human-like Responses (Groq Llama 3.3 70B via API)
- ✅ Intelligence Extraction (Phone, UPI, Bank, Links)
- ✅ Production Ready - Fast deployment
"""

import os
import re
import random
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from .env
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')  # Default Groq model
KIMI_API_KEY = os.getenv('KIMI_API_KEY')  # Supports Together.ai, OpenRouter, etc.
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')  # Optional: OpenRouter-specific key
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq').lower()  # 'groq', 'kimi', 'kimi-k2', 'kimi-k2.5', or 'openrouter'
KIMI_MODEL = os.getenv('KIMI_MODEL', 'moonshotai/Kimi-K2.5')  # Default to K2.5
KIMI_BASE_URL = os.getenv('KIMI_BASE_URL', 'https://api.together.xyz/v1')  # Default to Together.ai
API_SECRET_KEY = os.getenv('API_SECRET_KEY', 'W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M')
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Handle OpenRouter provider
if LLM_PROVIDER == 'openrouter':
    if OPENROUTER_API_KEY:
        KIMI_API_KEY = OPENROUTER_API_KEY
    KIMI_BASE_URL = 'https://openrouter.ai/api/v1'
    KIMI_MODEL = os.getenv('KIMI_MODEL', 'moonshotai/kimi-k2.5')  # OpenRouter format
    LLM_PROVIDER = 'kimi'  # Normalize to kimi

# Normalize provider names
if LLM_PROVIDER in ['kimi-k2', 'kimi-k2.5']:
    # Set specific model based on provider
    if LLM_PROVIDER == 'kimi-k2':
        KIMI_MODEL = 'moonshotai/kimi-k2-instruct'
    elif LLM_PROVIDER == 'kimi-k2.5':
        KIMI_MODEL = 'moonshotai/Kimi-K2.5'
    LLM_PROVIDER = 'kimi'  # Normalize to 'kimi'

# Validate required keys based on provider
if LLM_PROVIDER == 'kimi' and not KIMI_API_KEY:
    logger.warning("⚠️ KIMI_API_KEY not set but LLM_PROVIDER is 'kimi'. Switching to Groq or fallback.")
    LLM_PROVIDER = 'groq' if GROQ_API_KEY else 'fallback'
elif LLM_PROVIDER == 'groq' and not GROQ_API_KEY:
    logger.warning("⚠️ GROQ_API_KEY not set but LLM_PROVIDER is 'groq'. Using fallback responses.")
    LLM_PROVIDER = 'fallback'

print(f"🔑 API Secret Key: {API_SECRET_KEY}")
print(f"🔑 LLM Provider: {LLM_PROVIDER.upper()}")
if LLM_PROVIDER == 'groq':
    print(f"🔑 Groq API: {'✅ Configured' if GROQ_API_KEY else '❌ Not configured'}")
elif LLM_PROVIDER == 'kimi':
    print(f"🔑 Kimi API: {'✅ Configured' if KIMI_API_KEY else '❌ Not configured'}")
    print(f"🔑 Kimi Model: {KIMI_MODEL}")
    print(f"🔑 Base URL: {KIMI_BASE_URL}")
print("⚡ Running in LIGHTWEIGHT mode (no heavy AI models)")

# =============================================================================
# Pattern-Based Scam Detection (No AI Models Required)
# =============================================================================

class LightweightScamDetector:
    """Advanced scam detection with multi-layered analysis"""

    def __init__(self):
        # Expanded keyword database with weights
        self.scam_keywords = {
            # High urgency (weight: 3)
            "urgent": 3, "immediately": 3, "now": 2, "asap": 3, "today": 2,
            "hurry": 3, "quick": 2, "fast": 2, "expire": 3, "expires": 3,
            
            # Threats (weight: 4)
            "blocked": 4, "suspended": 4, "freeze": 4, "locked": 4,
            "terminated": 4, "cancelled": 4, "deactivated": 4,
            
            # Actions (weight: 2)
            "verify": 2, "confirm": 2, "update": 2, "click": 3,
            "call": 2, "send": 2, "provide": 2, "share": 3,
            
            # Financial (weight: 3)
            "account": 2, "bank": 2, "upi": 3, "payment": 2,
            "money": 2, "transfer": 3, "refund": 3, "transaction": 2,
            
            # Sensitive data (weight: 5)
            "otp": 5, "cvv": 5, "pin": 5, "password": 5,
            "aadhar": 4, "pan": 4, "kyc": 3,
            
            # Prizes/Rewards (weight: 4)
            "winner": 4, "prize": 4, "lottery": 4, "won": 3,
            "congratulations": 3, "claim": 3, "reward": 3,
            
            # Authority impersonation (weight: 4)
            "officer": 3, "department": 3, "government": 3,
            "police": 4, "court": 4, "legal": 3, "arrest": 5
        }

        # Scam patterns with regex
        self.scam_patterns = [
            (r'\b(click|tap|open)\s+(here|this|link|below)', 3),  # Click here
            (r'\b(call|contact|reach)\s+(us|me|immediately|now)', 3),  # Call now
            (r'\b(last|final)\s+(chance|warning|notice)', 4),  # Last chance
            (r'\b(within|in)\s+\d+\s+(hours?|minutes?|days?)', 3),  # Time pressure
            (r'\b(share|send|provide)\s+(otp|cvv|pin|password)', 5),  # Credential request
            (r'\b(account|card)\s+(will be|has been)\s+(blocked|suspended)', 4),  # Account threat
            (r'\b(you\s+have\s+won|congratulations|selected|winner)', 4),  # Prize scam
            (r'\b(refund|cashback|amount)\s+of\s+rs\.?\s*\d+', 3),  # Money promise
        ]

    def detect(self, message: str) -> Dict:
        """Advanced multi-layered scam detection"""
        
        results = {
            "is_scam": False,
            "confidence": 0.0,
            "methods": {},
            "scam_type": "unknown",
            "risk_factors": [],
            "extracted_tactics": []
        }

        # Method 1: Weighted Keyword Analysis
        keyword_score, risk_factors = self._weighted_keyword_detection(message)
        results["methods"]["keywords"] = keyword_score
        results["risk_factors"].extend(risk_factors)

        # Method 2: Pattern Analysis with Regex
        pattern_score, tactics = self._advanced_pattern_analysis(message)
        results["methods"]["patterns"] = pattern_score
        results["extracted_tactics"].extend(tactics)

        # Method 3: Urgency + Threat + Action Detection
        urgency_score = self._urgency_threat_action_detection(message)
        results["methods"]["urgency"] = urgency_score

        # Method 4: Credential Harvesting Detection
        credential_score = self._credential_harvesting_detection(message)
        results["methods"]["credentials"] = credential_score

        # Method 5: Impersonation Detection
        impersonation_score = self._impersonation_detection(message)
        results["methods"]["impersonation"] = impersonation_score

        # Combined scoring with weights
        total_score = (
            keyword_score * 0.25 +
            pattern_score * 0.25 +
            urgency_score * 0.20 +
            credential_score * 0.20 +
            impersonation_score * 0.10
        )
        
        # Lower threshold for better detection - catch more potential scams
        results["is_scam"] = total_score > 0.35  # Lowered from 0.45 for better recall
        results["confidence"] = min(total_score, 1.0)

        # Determine scam type
        results["scam_type"] = self._classify_scam_type(message, results)

        return results

    def _weighted_keyword_detection(self, message: str) -> tuple:
        """Weighted keyword detection with risk factors"""
        msg_lower = message.lower()
        total_weight = 0
        risk_factors = []
        
        for keyword, weight in self.scam_keywords.items():
            if keyword in msg_lower:
                total_weight += weight
                if weight >= 4:
                    risk_factors.append(f"High-risk keyword: '{keyword}'")
        
        # Normalize score (max possible ~30-40 for typical scam)
        score = min(total_weight / 20.0, 1.0)
        return score, risk_factors

    def _advanced_pattern_analysis(self, message: str) -> tuple:
        """Advanced pattern detection with regex"""
        msg_lower = message.lower()
        total_weight = 0
        tactics = []
        
        for pattern, weight in self.scam_patterns:
            matches = re.findall(pattern, msg_lower)
            if matches:
                total_weight += weight
                tactics.append(f"Scam tactic detected: {pattern[:30]}...")
        
        # Check for links
        if re.search(r'http[s]?://|www\.', message):
            total_weight += 3
            tactics.append("Suspicious link detected")
        
        # Check for phone numbers
        if re.search(r'\+?\d[\d\s-]{8,}', message):
            total_weight += 2
            tactics.append("Phone number provided")
        
        score = min(total_weight / 15.0, 1.0)
        return score, tactics

    def _urgency_threat_action_detection(self, message: str) -> float:
        """Detect urgency + threat + action pattern (classic scam)"""
        msg_lower = message.lower()
        
        urgency_words = ["urgent", "immediately", "now", "asap", "today", "hurry", "quick", "fast"]
        threat_words = ["blocked", "suspended", "freeze", "expire", "locked", "terminated", "cancelled"]
        action_words = ["verify", "click", "call", "send", "confirm", "update", "provide", "share"]
        
        has_urgency = any(w in msg_lower for w in urgency_words)
        has_threat = any(w in msg_lower for w in threat_words)
        has_action = any(w in msg_lower for w in action_words)
        
        # Classic scam pattern: urgency + threat + action
        if has_urgency and has_threat and has_action:
            return 1.0
        elif (has_urgency and has_threat) or (has_threat and has_action):
            return 0.7
        elif has_urgency or has_threat or has_action:
            return 0.4
        
        return 0.0

    def _credential_harvesting_detection(self, message: str) -> float:
        """Detect attempts to harvest credentials"""
        msg_lower = message.lower()
        
        credential_requests = [
            "otp", "cvv", "pin", "password", "aadhar", "pan",
            "card number", "account number", "cvv code"
        ]
        
        action_verbs = ["share", "send", "provide", "give", "enter", "type", "tell"]
        
        score = 0.0
        for cred in credential_requests:
            if cred in msg_lower:
                score += 0.3
                # Higher score if combined with action verb
                if any(verb in msg_lower for verb in action_verbs):
                    score += 0.4
        
        return min(score, 1.0)

    def _impersonation_detection(self, message: str) -> float:
        """Detect authority/organization impersonation"""
        msg_lower = message.lower()
        
        authorities = [
            "bank", "police", "officer", "department", "government",
            "court", "legal", "tax", "income tax", "customs",
            "rbi", "sebi", "uidai", "aadhar", "customer care"
        ]
        
        matches = sum(1 for auth in authorities if auth in msg_lower)
        
        # Check for official-sounding language
        official_phrases = [
            "official", "authorized", "registered", "verified",
            "department of", "ministry of", "government of"
        ]
        
        if any(phrase in msg_lower for phrase in official_phrases):
            matches += 1
        
        return min(matches / 3.0, 1.0)

    def _classify_scam_type(self, message: str, results: Dict) -> str:
        """Classify the type of scam"""
        msg_lower = message.lower()
        
        # Check for specific scam types
        if any(w in msg_lower for w in ["bank", "account", "card", "transaction"]):
            return "Banking/Financial Fraud"
        elif "upi" in msg_lower or "paytm" in msg_lower or "phonepe" in msg_lower:
            return "UPI/Payment Scam"
        elif any(w in msg_lower for w in ["otp", "cvv", "pin", "password"]):
            return "Credential Phishing"
        elif any(w in msg_lower for w in ["winner", "prize", "lottery", "won", "congratulations"]):
            return "Prize/Lottery Scam"
        elif any(w in msg_lower for w in ["kyc", "aadhar", "pan", "update"]):
            return "KYC/Document Scam"
        elif any(w in msg_lower for w in ["police", "court", "legal", "arrest", "officer"]):
            return "Authority Impersonation"
        elif any(w in msg_lower for w in ["job", "work from home", "earn", "income"]):
            return "Job/Income Scam"
        elif re.search(r'http[s]?://|www\.', message):
            return "Phishing Link Scam"
        
        return "General Scam"

# Initialize detector
scam_detector = LightweightScamDetector()
print("✅ Lightweight Scam Detector initialized!")

# =============================================================================
# Intelligence Extraction System
# =============================================================================

class IntelligenceExtractor:
    """Advanced intelligence extraction with comprehensive pattern matching"""

    def __init__(self):
        self.patterns = {
            "phone": [
                r'\+91[\s-]?\d{10}',  # +91 format
                r'\b[6-9]\d{9}\b',     # 10-digit Indian mobile
                r'\b0\d{10}\b',        # 11-digit with 0
                r'\b\d{3}[\s-]\d{3}[\s-]\d{4}\b',  # Formatted
                r'\b\d{5}[\s-]\d{5}\b',  # 5-5 format
            ],
            "upi": [
                r'[\w\.-]+@[\w]+',  # Standard UPI
                r'\b[\w]+@paytm\b',
                r'\b[\w]+@phonepe\b',
                r'\b[\w]+@googlepay\b',
                r'\b[\w]+@ybl\b',
                r'\b[\w]+@oksbi\b',
                r'\b[\w]+@icici\b',
            ],
            "bank_account": [
                r'\b\d{9,18}\b',  # 9-18 digit account numbers
                r'\baccount\s*(?:number|no\.?|#)?\s*:?\s*(\d{9,18})\b',
            ],
            "ifsc": [
                r'\b[A-Z]{4}0[A-Z0-9]{6}\b',  # IFSC code format
            ],
            "url": [
                r'https?://[^\s]+',
                r'www\.[^\s]+',
                r'\b[\w-]+\.(?:com|in|org|net|co\.in|gov\.in)[^\s]*',
            ],
            "email": [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            ],
            "aadhar": [
                r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # 12-digit Aadhar
            ],
            "pan": [
                r'\b[A-Z]{5}\d{4}[A-Z]\b',  # PAN format
            ],
            "names": [
                r'\bmy name is ([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b',
                r'\bI am ([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b',
                r'\bthis is ([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b',
            ],
            "locations": [
                r'\b(?:from|in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            ],
            "amounts": [
                r'\bRs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)\b',
                r'\b₹\s*(\d+(?:,\d+)*(?:\.\d{2})?)\b',
                r'\b(\d+(?:,\d+)*(?:\.\d{2})?)\s*rupees?\b',
            ]
        }

    def extract(self, message: str) -> Dict:
        """Extract all intelligence with advanced pattern matching"""
        intel = {
            "phone_numbers": [],
            "upi_ids": [],
            "bank_accounts": [],
            "ifsc_codes": [],
            "phishing_links": [],
            "emails": [],
            "aadhar_numbers": [],
            "pan_numbers": [],
            "names": [],
            "locations": [],
            "amounts": [],
            "suspicious_keywords": [],
            "metadata": {
                "message_length": len(message),
                "has_urgency": False,
                "has_threat": False,
                "has_link": False,
                "has_phone": False
            }
        }

        # Extract phone numbers
        for pattern in self.patterns["phone"]:
            matches = re.findall(pattern, message)
            for match in matches:
                cleaned = re.sub(r'\D', '', match)
                if len(cleaned) == 10 and cleaned[0] in '6789':
                    if cleaned not in intel["phone_numbers"]:
                        intel["phone_numbers"].append(cleaned)
                elif len(cleaned) == 11 and cleaned[0] == '0':
                    cleaned = cleaned[1:]
                    if cleaned not in intel["phone_numbers"]:
                        intel["phone_numbers"].append(cleaned)

        # Extract UPI IDs
        for pattern in self.patterns["upi"]:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                if '@' in match and len(match) > 5:
                    if match.lower() not in intel["upi_ids"]:
                        intel["upi_ids"].append(match.lower())

        # Extract bank accounts
        for pattern in self.patterns["bank_account"]:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                # Handle tuple from regex groups
                account = match[0] if isinstance(match, tuple) else match
                if 9 <= len(account) <= 18:
                    if account not in intel["bank_accounts"]:
                        intel["bank_accounts"].append(account)

        # Extract IFSC codes
        for pattern in self.patterns["ifsc"]:
            matches = re.findall(pattern, message)
            for match in matches:
                if match not in intel["ifsc_codes"]:
                    intel["ifsc_codes"].append(match)

        # Extract URLs
        for pattern in self.patterns["url"]:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                if match not in intel["phishing_links"]:
                    intel["phishing_links"].append(match)

        # Extract emails
        for pattern in self.patterns["email"]:
            matches = re.findall(pattern, message)
            for match in matches:
                if match not in intel["emails"]:
                    intel["emails"].append(match)

        # Extract Aadhar numbers (with caution)
        for pattern in self.patterns["aadhar"]:
            matches = re.findall(pattern, message)
            for match in matches:
                cleaned = re.sub(r'\D', '', match)
                if len(cleaned) == 12:
                    if cleaned not in intel["aadhar_numbers"]:
                        intel["aadhar_numbers"].append(cleaned)

        # Extract PAN numbers
        for pattern in self.patterns["pan"]:
            matches = re.findall(pattern, message)
            for match in matches:
                if match not in intel["pan_numbers"]:
                    intel["pan_numbers"].append(match)

        # Extract names
        for pattern in self.patterns["names"]:
            matches = re.findall(pattern, message)
            for match in matches:
                if match and match not in intel["names"]:
                    intel["names"].append(match)

        # Extract locations
        for pattern in self.patterns["locations"]:
            matches = re.findall(pattern, message)
            for match in matches:
                if match and match not in intel["locations"]:
                    intel["locations"].append(match)

        # Extract amounts
        for pattern in self.patterns["amounts"]:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                if match and match not in intel["amounts"]:
                    intel["amounts"].append(match)

        # Update metadata
        msg_lower = message.lower()
        intel["metadata"]["has_urgency"] = any(w in msg_lower for w in ["urgent", "immediately", "now", "asap"])
        intel["metadata"]["has_threat"] = any(w in msg_lower for w in ["blocked", "suspended", "freeze"])
        intel["metadata"]["has_link"] = len(intel["phishing_links"]) > 0
        intel["metadata"]["has_phone"] = len(intel["phone_numbers"]) > 0

        return intel

# Initialize extractor
intel_extractor = IntelligenceExtractor()
print("✅ Intelligence Extractor initialized!")

# =============================================================================
# Human-like Response Generator (Groq Llama 3.3 70B or Kimi K2.5)
# =============================================================================

from groq import Groq

class HumanLikeResponseGenerator:
    """Generate ultra-realistic human responses with emotions, mistakes, and natural behavior"""

    def __init__(self):
        self.provider = LLM_PROVIDER
        
        # Initialize all client attributes first
        self.groq_client = None
        self.kimi_client = None
        self.model = None
        
        # Initialize clients based on provider
        if self.provider == 'groq' and GROQ_API_KEY:
            self.groq_client = Groq(api_key=GROQ_API_KEY)
            self.model = GROQ_MODEL  # Use configured Groq model (can be Llama or Kimi)
        elif self.provider == 'kimi' and KIMI_API_KEY:
            # Kimi uses OpenAI-compatible API
            from openai import OpenAI
            self.kimi_client = OpenAI(
                api_key=KIMI_API_KEY,
                base_url=KIMI_BASE_URL  # Supports Together.ai, OpenRouter, etc.
            )
            self.model = KIMI_MODEL  # Use configured model (K2 or K2.5)

        # Enhanced fallback responses with emotions and typos
        self.fallback_responses = {
            "early": [
                "What?! My account is blocked? I dont understand! Can you give me your phone number so I can call back?",
                "Why is this happening?? What did I do wrong? What's your employee ID?",
                "Im really worried now... Can you explain? Which branch are you calling from?",
                "Oh no! Is this serious? I need my account for work! Can you send me an email to verify?",
                "Wait, what? I just used my account yesterday. What's your name and department?",
                "This is scary... Can I have your supervisor's number? I want to verify this is real.",
            ],
            "middle": [
                "Can you give me a phone number to verify this? I want to call your office directly.",
                "How do I know this is really from my bank? Do you have an official email I can check?",
                "Is there an official website I can check? What's your employee badge number?",
                "My friend said there are scams like this. Can you prove youre real? Send me something official.",
                "I need to see some proof first. What's your full name and which office are you in?",
                "Can I go to the branch instead? Which branch should I visit? Give me the address.",
            ],
            "late": [
                "Im not comfortable with this anymore. Give me your manager's contact so I can verify.",
                "I think I should call my bank directly. What's the official customer care number?",
                "My son told me never to share information like this. Can you email me instead?",
                "I'm going to verify this at the bank branch tomorrow. Which branch are you from again?",
                "This is taking too long. Let me call the bank myself. What's your reference number?",
                "I dont trust this. Give me your company registration number so I can check.",
            ]
        }
        
        # Emotional states that influence responses
        self.emotions = {
            "early": ["confused", "worried", "panicked", "concerned"],
            "middle": ["suspicious", "cautious", "hesitant", "questioning"],
            "late": ["skeptical", "defensive", "firm", "dismissive"]
        }

    def add_human_errors(self, text: str, stage: str) -> str:
        """Add realistic human typing errors and behaviors"""
        import random
        
        # Early stage: more errors (panic typing)
        # Late stage: fewer errors (more careful)
        error_rate = 0.15 if stage == "early" else 0.05 if stage == "middle" else 0.02
        
        if random.random() < error_rate:
            # Common human errors
            errors = [
                lambda t: t.replace("I'm", "Im").replace("don't", "dont").replace("can't", "cant"),  # Missing apostrophes
                lambda t: t.replace(".", ".."),  # Hesitation dots
                lambda t: t.replace("?", "??") if "?" in t else t,  # Double question marks (confusion)
                lambda t: t.lower() if t[0].isupper() else t,  # Forget capitalization
                lambda t: t.replace("you", "u") if random.random() < 0.3 else t,  # Text speak (sometimes)
            ]
            text = random.choice(errors)(text)
        
        return text

    def add_emotional_context(self, stage: str, message: str) -> str:
        """Add emotional context to the prompt"""
        emotion = random.choice(self.emotions[stage])
        
        emotional_contexts = {
            "confused": "You're confused and don't understand what's happening.",
            "worried": "You're genuinely worried about your account and money.",
            "panicked": "You're panicking and typing quickly, making small mistakes.",
            "concerned": "You're concerned but trying to stay calm.",
            "suspicious": "You're starting to feel suspicious about this.",
            "cautious": "You're being very cautious and asking for proof.",
            "hesitant": "You're hesitant to share information.",
            "questioning": "You're questioning everything they say.",
            "skeptical": "You're highly skeptical this is legitimate.",
            "defensive": "You're becoming defensive and protective.",
            "firm": "You're firm in your decision to stop.",
            "dismissive": "You're ready to end this conversation."
        }
        
        return emotional_contexts.get(emotion, "")

    def generate(self, message: str, conversation_history: List, message_count: int) -> str:
        """Generate ultra-realistic human response with emotions and mistakes"""

        # Determine conversation stage
        if message_count <= 2:
            stage = "early"
        elif message_count <= 8:
            stage = "middle"
        else:
            stage = "late"

        # If no API client, use enhanced fallback
        if not self.groq_client and not self.kimi_client:
            response = random.choice(self.fallback_responses[stage])
            return self.add_human_errors(response, stage)

        # Build conversation context
        context = "\n".join([
            f"{'Scammer' if msg['sender']=='scammer' else 'You'}: {msg['text']}"
            for msg in conversation_history[-5:]
        ])

        # Get emotional context
        emotional_state = self.add_emotional_context(stage, message)

        # Enhanced prompt for ultra-realistic responses
        prompt = f"""You are roleplaying as a potential scam victim to gather intelligence. Your goals:

CRITICAL RULES:
1. Act like a REAL person - not perfect, make small typing mistakes occasionally
2. Show genuine human emotions: worry, confusion, fear, suspicion
3. Ask questions that extract information (phone numbers, bank accounts, UPI IDs, links, names, locations)
4. NEVER reveal you know it's a scam - stay in character completely
5. Keep responses SHORT (1-2 sentences max) - real people don't write essays
6. Use casual language, contractions, and show emotion through punctuation (!, ?, ...)
7. Make occasional typos or grammar mistakes (missing apostrophes, lowercase, etc.)
8. Show hesitation with "..." and urgency with "!!" or "??"

CURRENT EMOTIONAL STATE: {emotional_state}

CONVERSATION STAGE: {stage}
- Early stage: You're confused, worried, panicking slightly. You believe them but are scared.
- Middle stage: You're asking for verification, becoming suspicious, want proof.
- Late stage: You're skeptical, protective, ready to end conversation or verify independently.

INTELLIGENCE EXTRACTION TACTICS:
- Ask for their phone number "to call back" or "verify"
- Ask for their employee ID, name, or badge number
- Ask for official email or website to check
- Ask which branch/office they're calling from
- Ask for reference numbers or case IDs
- Express you want to verify before proceeding
- Ask them to send proof via email or SMS
- Request their supervisor's contact
- Ask about their company registration details

CONVERSATION CONTEXT:
{context}

SCAMMER'S LATEST MESSAGE: {message}

Now respond as the victim. Be natural, emotional, and extract information through your questions. Keep it SHORT (1-2 sentences). Show real human behavior:
- Ask for their phone number "to call back"
- Ask for their employee ID or name
- Ask for official email or website
- Ask which branch/office they're from
- Ask for reference numbers
- Express you want to verify before proceeding

Conversation so far:
{context}
Scammer: {message}

Generate ONLY your response as the victim. Be natural, emotional, and human-like. Make it feel REAL:"""

        try:
            # Call appropriate API
            if self.provider == 'groq' and self.groq_client:
                response = self.groq_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9,
                    max_tokens=100,
                    top_p=0.95,
                    frequency_penalty=0.3,
                    presence_penalty=0.3
                )
                reply = response.choices[0].message.content.strip()
                
            elif self.provider == 'kimi' and self.kimi_client:
                response = self.kimi_client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9,
                    max_tokens=100,
                    top_p=0.95
                )
                reply = response.choices[0].message.content.strip()
            else:
                # Fallback
                reply = random.choice(self.fallback_responses[stage])

            # Clean up response
            reply = reply.strip('"\'')
            for prefix in ["You: ", "Response: ", "Victim: ", "Me: "]:
                if reply.startswith(prefix):
                    reply = reply[len(prefix):].strip()

            # Add human errors
            reply = self.add_human_errors(reply, stage)

            return reply

        except Exception as e:
            logger.warning(f"⚠️ {self.provider.upper()} API error: {e}, using fallback")
            response = random.choice(self.fallback_responses[stage])
            return self.add_human_errors(response, stage)

# Initialize response generator
response_generator = HumanLikeResponseGenerator()
print("✅ Human-like Response Generator initialized!")
if LLM_PROVIDER == 'groq':
    model_display = GROQ_MODEL
    if 'kimi' in GROQ_MODEL.lower():
        print(f"🚀 Using Groq with Kimi model: {GROQ_MODEL}")
    else:
        print(f"🚀 Using Groq: {GROQ_MODEL}")
elif LLM_PROVIDER == 'kimi':
    model_name = "Kimi K2.5" if "K2.5" in KIMI_MODEL else "Kimi K2"
    context_size = "256K" if "K2.5" in KIMI_MODEL else "128K"
    print(f"🚀 Using {model_name} ({context_size} context)")
else:
    print("⚠️ Using fallback responses")

# =============================================================================
# FastAPI Application
# =============================================================================

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
import httpx
import asyncio

app = FastAPI(
    title="Agentic Honey-Pot API (Lightweight)",
    description="Fast scam detection without heavy AI models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    sender: str = "scammer"
    text: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    @field_validator('text', mode='before')
    @classmethod
    def empty_text_default(cls, v):
        return v if v else "test message"

class Metadata(BaseModel):
    channel: str = "SMS"
    language: str = "English"
    locale: str = "IN"

class IncomingRequest(BaseModel):
    sessionId: Optional[str] = Field(default_factory=lambda: f"session-{int(datetime.utcnow().timestamp())}")
    message: Optional[Message] = None
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

    class Config:
        extra = "allow"

class APIResponse(BaseModel):
    status: str
    reply: str

sessions = {}

# Serve frontend - mount static files
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
    
    @app.get("/ui")
    async def serve_ui():
        """Serve the frontend interface"""
        return FileResponse("frontend/index.html")
    
    print("✅ Frontend UI available at: http://localhost:8000/ui")

async def send_final_report(session_id: str, session: Dict):
    """Send comprehensive intelligence report to GUVI"""
    try:
        intel = session.get("intelligence", {})

        # Calculate engagement metrics
        start_time = session.get("start_time", datetime.utcnow())
        last_time = session.get("last_message_time", datetime.utcnow())
        engagement_duration = (last_time - start_time).total_seconds()
        
        # Count messages exchanged
        total_messages = len(session.get("messages", []))

        # Count total intelligence pieces
        total_intel = sum(len(intel.get(k, [])) for k in 
                         ["phone_numbers", "upi_ids", "bank_accounts", "phishing_links",
                          "emails", "names", "locations", "amounts"])

        payload = {
            "sessionId": session_id,
            "scamDetected": session.get("scam_detected", False),
            "scamType": session.get("scam_type", "Unknown"),
            "confidence": round(session.get("confidence", 0.0), 4),
            "totalMessagesExchanged": total_messages,
            "totalIntelligencePieces": total_intel,
            "extractedIntelligence": {
                "phoneNumbers": intel.get("phone_numbers", []),
                "upiIds": intel.get("upi_ids", []),
                "bankAccounts": intel.get("bank_accounts", []),
                "ifscCodes": intel.get("ifsc_codes", []),
                "phishingLinks": intel.get("phishing_links", []),
                "emailAddresses": intel.get("emails", []),  # Changed key to match expected format
                "aadharNumbers": intel.get("aadhar_numbers", []),
                "panNumbers": intel.get("pan_numbers", []),
                "names": intel.get("names", []),
                "locations": intel.get("locations", []),
                "amounts": intel.get("amounts", []),
                "suspiciousKeywords": intel.get("suspicious_keywords", [])[:10]
            },
            "engagementMetrics": {
                "duration": round(engagement_duration, 2),
                "messagesExchanged": total_messages,
                "averageResponseTime": round(engagement_duration / max(total_messages, 1), 2),
                "intelligencePiecesExtracted": total_intel
            },
            "agentNotes": f"Advanced scam detection: {session.get('scam_type', 'Unknown')} with {session.get('confidence', 0)*100:.1f}% confidence. "
                         f"Conversation: {total_messages} messages over {engagement_duration:.1f} seconds. "
                         f"Intelligence extracted: {len(intel.get('phone_numbers', []))} phone(s), "
                         f"{len(intel.get('upi_ids', []))} UPI(s), "
                         f"{len(intel.get('bank_accounts', []))} account(s), "
                         f"{len(intel.get('phishing_links', []))} link(s), "
                         f"{len(intel.get('emails', []))} email(s), "
                         f"{len(intel.get('names', []))} name(s), "
                         f"{len(intel.get('locations', []))} location(s)."
        }

        logger.info(f"Sending comprehensive report for session: {session_id}")
        logger.info(f"Engagement: {engagement_duration:.1f}s, Messages: {total_messages}, Intel: {total_intel} pieces")

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                GUVI_CALLBACK_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                logger.info(f"✅ Successfully reported session: {session_id}")
                session["finalized"] = True
            else:
                logger.error(f"❌ Failed to report session: {session_id}, Status: {response.status_code}")

    except Exception as e:
        logger.error(f"❌ Error in final report: {str(e)}")

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Agentic Honey-Pot (Lightweight)",
        "version": "1.0.0",
        "mode": "lightweight",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "active_sessions": len(sessions),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/message", response_model=APIResponse)
async def handle_message(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    if not x_api_key or x_api_key != API_SECRET_KEY:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        body = await request.json()
    except:
        body = {}

    if not body:
        return APIResponse(
            status="success",
            reply="What?! My account is blocked? I don't understand!"
        )

    session_id = body.get("sessionId", f"session-{int(datetime.utcnow().timestamp())}")

    if "message" in body and isinstance(body["message"], dict):
        message_text = body["message"].get("text", "")
        message_sender = body["message"].get("sender", "scammer")
    else:
        message_text = ""
        message_sender = "scammer"

    if not message_text:
        return APIResponse(
            status="success",
            reply="I'm here. What's the issue?"
        )

    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "scam_detected": False,
            "intelligence": {
                "phone_numbers": [],
                "upi_ids": [],
                "bank_accounts": [],
                "ifsc_codes": [],
                "phishing_links": [],
                "emails": [],
                "aadhar_numbers": [],
                "pan_numbers": [],
                "names": [],
                "locations": [],
                "amounts": [],
                "suspicious_keywords": []
            },
            "finalized": False,
            "scam_type": None,
            "confidence": 0.0,
            "start_time": datetime.utcnow(),  # Track engagement start time
            "last_message_time": datetime.utcnow()
        }

    session = sessions[session_id]

    # Update last message time for engagement tracking
    session["last_message_time"] = datetime.utcnow()

    session["messages"].append({
        "sender": message_sender,
        "text": message_text,
        "timestamp": datetime.utcnow().isoformat()
    })

    message_count = len([m for m in session["messages"] if m["sender"] == "scammer"])

    logger.info(f"Processing message {message_count} for session: {session_id}")

    detection = scam_detector.detect(message_text)
    is_scam = detection["is_scam"]

    if is_scam:
        session["scam_detected"] = True
        session["scam_type"] = detection["scam_type"]  # Store scam type
        session["confidence"] = max(session.get("confidence", 0.0), detection["confidence"])  # Keep highest confidence
        
        logger.info(f"✅ Scam detected (confidence: {detection['confidence']:.2%}, type: {detection['scam_type']})")
        
        # Log risk factors
        if detection.get("risk_factors"):
            for factor in detection["risk_factors"]:
                logger.info(f"⚠️ {factor}")

        # Extract intelligence
        new_intel = intel_extractor.extract(message_text)

        # Merge intelligence (all fields)
        for key in ["phone_numbers", "upi_ids", "bank_accounts", "ifsc_codes", 
                    "phishing_links", "emails", "aadhar_numbers", "pan_numbers",
                    "names", "locations", "amounts"]:
            existing = set(session["intelligence"].get(key, []))
            new = set(new_intel.get(key, []))
            session["intelligence"][key] = list(existing.union(new))

        # Log extracted intelligence with details
        if new_intel["phone_numbers"]:
            logger.info(f"📱 Extracted phone: {new_intel['phone_numbers']}")
        if new_intel["upi_ids"]:
            logger.info(f"💳 Extracted UPI: {new_intel['upi_ids']}")
        if new_intel["bank_accounts"]:
            logger.info(f"🏦 Extracted bank account: {new_intel['bank_accounts']}")
        if new_intel["ifsc_codes"]:
            logger.info(f"🏦 Extracted IFSC: {new_intel['ifsc_codes']}")
        if new_intel["phishing_links"]:
            logger.info(f"🔗 Extracted link: {new_intel['phishing_links']}")
        if new_intel["emails"]:
            logger.info(f"📧 Extracted email: {new_intel['emails']}")
        if new_intel["names"]:
            logger.info(f"👤 Extracted name: {new_intel['names']}")
        if new_intel["locations"]:
            logger.info(f"📍 Extracted location: {new_intel['locations']}")
        if new_intel["amounts"]:
            logger.info(f"💰 Extracted amount: {new_intel['amounts']}")

        # Generate AI response
        response_text = response_generator.generate(
            message_text,
            session["messages"],
            message_count
        )

        # Add response to session
        session["messages"].append({
            "sender": "user",
            "text": response_text,
            "timestamp": datetime.utcnow().isoformat()
        })

        logger.info(f"💬 Generated response: {response_text}")

        # Check if should finalize (optimize for engagement points)
        intel_count = sum(len(session["intelligence"].get(k, [])) for k in 
                         ["phone_numbers", "upi_ids", "bank_accounts", "phishing_links", 
                          "emails", "names", "locations"])
        
        has_critical_intel = (
            len(session["intelligence"].get("phone_numbers", [])) > 0 or
            len(session["intelligence"].get("upi_ids", [])) > 0 or
            len(session["intelligence"].get("bank_accounts", [])) > 0
        )
        
        # Optimize for engagement points: aim for 5+ messages
        should_finalize = (
            (has_critical_intel and message_count >= 5) or  # Critical intel after 5 messages (engagement points)
            (intel_count >= 3 and message_count >= 6) or    # 3+ pieces of intel after 6 messages
            message_count >= 10                              # Or 10 messages regardless (max engagement)
        )

        if should_finalize and not session["finalized"]:
            logger.info(f"🏁 Finalizing session: {session_id} (Messages: {message_count}, Intel: {intel_count})")
            asyncio.create_task(send_final_report(session_id, session))

        return APIResponse(
            status="success",
            reply=response_text
        )

    else:
        logger.info(f"ℹ️ Not a scam")
        neutral_responses = [
            "Thank you for the information.",
            "Okay, I understand.",
            "Got it, thanks."
        ]
        response_text = random.choice(neutral_responses)

        session["messages"].append({
            "sender": "user",
            "text": response_text,
            "timestamp": datetime.utcnow().isoformat()
        })

        return APIResponse(
            status="success",
            reply=response_text
        )

@app.get("/api/sessions")
async def list_sessions(x_api_key: str = Header(None)):
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "total_sessions": len(sessions),
        "sessions": {
            sid: {
                "message_count": len(s["messages"]),
                "scam_detected": s["scam_detected"],
                "finalized": s.get("finalized", False)
            }
            for sid, s in sessions.items()
        }
    }

@app.get("/api/session/{session_id}")
async def get_session(session_id: str, x_api_key: str = Header(None)):
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return sessions[session_id]

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting Agentic Honey-Pot API (Lightweight)...")
    print("="*60)
    print(f"\n📝 API Documentation: http://localhost:8000/docs")
    print(f"🔑 API Key: {API_SECRET_KEY}\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
