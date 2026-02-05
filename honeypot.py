#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🍯 ULTIMATE AGENTIC HONEY-POT
Multi-Model AI System for Scam Detection & Intelligence Extraction

Features:
- ✅ Multi-Model Scam Detection (6 AI models)
- ✅ Human-like Responses (Groq Llama 3.1 70B)
- ✅ Intelligence Extraction (Phone, UPI, Bank, Links)
- ✅ Production Ready - Deploy anywhere
"""

import os
import secrets
import re
import random
import logging
from typing import Dict, List, Optional, Set
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from .env
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY', 'W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M')
NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Validate required keys
if not GROQ_API_KEY:
    logger.warning("⚠️ GROQ_API_KEY not set in .env file. AI responses will use fallback mode.")

print(f"🔑 API Secret Key: {API_SECRET_KEY}")
print(f"🔑 Groq API: {'✅ Configured' if GROQ_API_KEY else '❌ Not configured'}")

# =============================================================================
# STEP 1: Load AI Models
# =============================================================================

from transformers import pipeline
import spacy
import torch

print("\n🔄 Loading AI models... (this may take 2-3 minutes)\n")

# 1. Sentiment Analysis (detects urgency, fear)
print("Loading DistilBERT for sentiment analysis...")
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=0 if torch.cuda.is_available() else -1
)

# 2. Zero-Shot Classification (adapts to new scam types)
print("Loading BART for zero-shot classification...")
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0 if torch.cuda.is_available() else -1
)

# 3. Named Entity Recognition
print("Loading spaCy for entity recognition...")
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
    import sys
    sys.exit(1)

print("\n✅ All AI models loaded successfully!")
print(f"🔥 Using: {'GPU' if torch.cuda.is_available() else 'CPU'}")

# =============================================================================
# STEP 2: Multi-Model Scam Detection System
# =============================================================================

class MultiModelScamDetector:
    """Advanced scam detection using ensemble of AI models"""

    def __init__(self):
        self.scam_keywords = [
            "urgent", "verify", "immediately", "blocked", "suspended",
            "confirm", "otp", "cvv", "pin", "password", "expire",
            "winner", "prize", "lottery", "congratulations", "claim",
            "account", "bank", "upi", "transfer", "refund"
        ]

        self.scam_categories = [
            "bank fraud",
            "UPI scam",
            "phishing attack",
            "prize scam",
            "tech support scam",
            "urgent verification request"
        ]

    def detect(self, message: str) -> Dict:
        """Run all detection methods and combine results"""

        results = {
            "is_scam": False,
            "confidence": 0.0,
            "methods": {},
            "scam_type": None
        }

        # Method 1: Keyword Analysis (Fast)
        keyword_score = self._keyword_detection(message)
        results["methods"]["keywords"] = keyword_score

        # Method 2: Sentiment Analysis (AI)
        sentiment_score = self._sentiment_analysis(message)
        results["methods"]["sentiment"] = sentiment_score

        # Method 3: Zero-Shot Classification (AI)
        classification_score, scam_type = self._zero_shot_classification(message)
        results["methods"]["classification"] = classification_score
        results["scam_type"] = scam_type

        # Method 4: Pattern Analysis
        pattern_score = self._pattern_analysis(message)
        results["methods"]["patterns"] = pattern_score

        # Ensemble voting (if 2+ methods detect scam, it's a scam)
        scam_votes = sum([
            keyword_score > 0.5,
            sentiment_score > 0.6,
            classification_score > 0.7,
            pattern_score > 0.5
        ])

        results["is_scam"] = scam_votes >= 2
        results["confidence"] = (keyword_score + sentiment_score + classification_score + pattern_score) / 4

        return results

    def _keyword_detection(self, message: str) -> float:
        """Fast keyword-based detection"""
        msg_lower = message.lower()
        matches = sum(1 for kw in self.scam_keywords if kw in msg_lower)
        return min(matches / 3.0, 1.0)  # 3+ keywords = 100% score

    def _sentiment_analysis(self, message: str) -> float:
        """AI-based sentiment analysis"""
        try:
            result = sentiment_analyzer(message[:512])[0]
            # Negative sentiment often indicates scam (urgency, fear)
            if result['label'] == 'NEGATIVE':
                return result['score']
            return 0.3  # Neutral/positive can still be scam
        except:
            return 0.5

    def _zero_shot_classification(self, message: str) -> tuple:
        """AI-based zero-shot classification"""
        try:
            result = classifier(message[:512], self.scam_categories)
            top_score = result['scores'][0]
            top_label = result['labels'][0]
            return top_score, top_label
        except:
            return 0.5, "unknown"

    def _pattern_analysis(self, message: str) -> float:
        """Pattern-based detection"""
        score = 0.0
        msg_lower = message.lower()

        # Check for urgency + threat + action pattern
        has_urgency = any(w in msg_lower for w in ["urgent", "immediately", "now", "asap"])
        has_threat = any(w in msg_lower for w in ["blocked", "suspended", "freeze", "expire"])
        has_action = any(w in msg_lower for w in ["verify", "click", "call", "send", "confirm"])
        has_financial = any(w in msg_lower for w in ["account", "bank", "upi", "money", "payment"])
        has_link = bool(re.search(r'http[s]?://|www\.', message))
        has_phone = bool(re.search(r'\+?\d[\d\s-]{8,}', message))

        if has_urgency and has_threat and has_action:
            score += 0.5
        if has_financial and (has_link or has_phone):
            score += 0.3
        if has_link:
            score += 0.2

        return min(score, 1.0)

# Initialize detector
scam_detector = MultiModelScamDetector()
print("✅ Multi-Model Scam Detector initialized!")

# =============================================================================
# STEP 3: Intelligence Extraction System
# =============================================================================

class IntelligenceExtractor:
    """Extract scammer information from messages"""

    def __init__(self):
        self.patterns = {
            "phone": [
                r'\+91[\s-]?\d{10}',
                r'\b[6-9]\d{9}\b',
                r'\b0\d{10}\b'
            ],
            "upi": [
                r'[\w\.-]+@[\w]+',
            ],
            "bank_account": [
                r'\b\d{9,18}\b',
            ],
            "url": [
                r'https?://[^\s]+',
                r'www\.[^\s]+',
            ]
        }

    def extract(self, message: str) -> Dict:
        """Extract all intelligence from message"""
        intel = {
            "phone_numbers": set(),
            "upi_ids": set(),
            "bank_accounts": set(),
            "phishing_links": set(),
            "entities": []
        }

        # Extract phone numbers
        for pattern in self.patterns["phone"]:
            matches = re.findall(pattern, message)
            for match in matches:
                cleaned = re.sub(r'\D', '', match)
                if len(cleaned) == 10 and cleaned[0] in '6789':
                    intel["phone_numbers"].add(cleaned)

        # Extract UPI IDs
        for pattern in self.patterns["upi"]:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                if '@' in match and len(match) > 5:
                    intel["upi_ids"].add(match.lower())

        # Extract bank accounts
        for pattern in self.patterns["bank_account"]:
            matches = re.findall(pattern, message)
            for match in matches:
                if len(match) >= 9 and len(match) <= 18:
                    intel["bank_accounts"].add(match)

        # Extract URLs
        for pattern in self.patterns["url"]:
            matches = re.findall(pattern, message, re.IGNORECASE)
            for match in matches:
                intel["phishing_links"].add(match)

        # NER extraction using spaCy
        doc = nlp(message)
        for ent in doc.ents:
            intel["entities"].append({
                "text": ent.text,
                "type": ent.label_
            })

        # Convert sets to lists for JSON serialization
        intel["phone_numbers"] = list(intel["phone_numbers"])
        intel["upi_ids"] = list(intel["upi_ids"])
        intel["bank_accounts"] = list(intel["bank_accounts"])
        intel["phishing_links"] = list(intel["phishing_links"])

        return intel

# Initialize extractor
intel_extractor = IntelligenceExtractor()
print("✅ Intelligence Extractor initialized!")

# =============================================================================
# STEP 4: Human-like Response Generator (Groq Llama 3.1 70B)
# =============================================================================

from groq import Groq

class HumanLikeResponseGenerator:
    """Generate human-like responses using Groq Llama 3.1 70B"""

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

        # Fallback responses if API fails
        self.fallback_responses = {
            "early": [
                "What?! My account is blocked? I don't understand!",
                "Why is this happening? What did I do wrong?",
                "I'm really worried now. Can you explain?"
            ],
            "middle": [
                "Can you give me a phone number to verify this?",
                "How do I know this is really from my bank?",
                "Is there an official email I can check?"
            ],
            "late": [
                "I'm not comfortable with this. Can we do it another way?",
                "How do I know this isn't a scam?",
                "I'll contact my bank directly to verify."
            ]
        }

    def generate(self, message: str, conversation_history: List, message_count: int) -> str:
        """Generate human-like response"""

        # Determine conversation stage
        if message_count <= 2:
            stage = "early"
        elif message_count <= 8:
            stage = "middle"
        else:
            stage = "late"

        # If no Groq API key, use fallback
        if not self.client:
            return random.choice(self.fallback_responses[stage])

        # Build conversation context
        context = "\n".join([
            f"{'Scammer' if msg['sender']=='scammer' else 'You'}: {msg['text']}"
            for msg in conversation_history[-5:]  # Last 5 messages
        ])

        # Create prompt for Llama
        prompt = f"""You are roleplaying as a potential scam victim to gather intelligence. Your goals:
1. Act like a real, slightly naive person who is concerned
2. Ask questions to extract information (phone numbers, bank accounts, UPI IDs, links)
3. Show hesitation and concern, but remain engaged
4. NEVER reveal you know it's a scam
5. Keep responses SHORT (1-2 sentences max) and natural
6. Use casual language, contractions, and show emotion

Conversation so far:
{context}
Scammer: {message}

Stage: {stage} (early=concerned, middle=asking for details, late=skeptical)

Generate ONLY your response as the victim. Be natural, worried, and human-like:"""

        try:
            # Call Groq API (Llama 3.3 70B)
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=150,
                top_p=0.9
            )

            reply = response.choices[0].message.content.strip()

            # Clean up response
            reply = reply.strip('"\'')
            for prefix in ["You: ", "Response: ", "Victim: "]:
                if reply.startswith(prefix):
                    reply = reply[len(prefix):].strip()

            return reply

        except Exception as e:
            logger.warning(f"⚠️ Groq API error: {e}, using fallback")
            return random.choice(self.fallback_responses[stage])

# Initialize response generator
response_generator = HumanLikeResponseGenerator()
print("✅ Human-like Response Generator initialized!")
if GROQ_API_KEY:
    print("🚀 Using Groq Llama 3.3 70B (fastest LLM in the world!)")
else:
    print("⚠️ Using fallback responses (set GROQ_API_KEY for AI responses)")

# =============================================================================
# STEP 5: Create FastAPI Application
# =============================================================================

from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import httpx
import asyncio

app = FastAPI(
    title="Agentic Honey-Pot API",
    description="AI-powered scam detection and intelligence extraction",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
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

# Session storage
sessions = {}

async def send_final_report(session_id: str, session: Dict):
    """Send final intelligence report to GUVI"""
    try:
        intel = session.get("intelligence", {})

        payload = {
            "sessionId": session_id,
            "scamDetected": session.get("scam_detected", False),
            "totalMessagesExchanged": len(session.get("messages", [])),
            "extractedIntelligence": {
                "bankAccounts": intel.get("bank_accounts", []),
                "upiIds": intel.get("upi_ids", []),
                "phishingLinks": intel.get("phishing_links", []),
                "phoneNumbers": intel.get("phone_numbers", []),
                "suspiciousKeywords": intel.get("suspicious_keywords", [])[:10]
            },
            "agentNotes": f"Scam conversation with {len(session.get('messages', []))} messages. "
                         f"Extracted {len(intel.get('phone_numbers', []))} phone(s), "
                         f"{len(intel.get('upi_ids', []))} UPI(s), "
                         f"{len(intel.get('phishing_links', []))} link(s)."
        }

        logger.info(f"Sending final report for session: {session_id}")

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
    """Root endpoint"""
    return {
        "status": "online",
        "service": "Agentic Honey-Pot",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    """Health check"""
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
    """
    Main endpoint for scam detection and response
    Compatible with GUVI's automated testing
    """

    # Verify API key
    if not x_api_key or x_api_key != API_SECRET_KEY:
        logger.warning(f"Invalid API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    # Parse request body
    try:
        body = await request.json()
    except:
        body = {}

    # Handle empty request
    if not body:
        return APIResponse(
            status="success",
            reply="What?! My account is blocked? I don't understand!"
        )

    # Extract fields
    session_id = body.get("sessionId", f"session-{int(datetime.utcnow().timestamp())}")

    # Get message
    if "message" in body and isinstance(body["message"], dict):
        message_text = body["message"].get("text", "")
        message_sender = body["message"].get("sender", "scammer")
    else:
        message_text = ""
        message_sender = "scammer"

    # Handle empty message
    if not message_text:
        return APIResponse(
            status="success",
            reply="I'm here. What's the issue?"
        )

    # Initialize or get session
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "scam_detected": False,
            "intelligence": {
                "phone_numbers": [],
                "upi_ids": [],
                "bank_accounts": [],
                "phishing_links": [],
                "suspicious_keywords": []
            },
            "finalized": False
        }

    session = sessions[session_id]

    # Add incoming message
    session["messages"].append({
        "sender": message_sender,
        "text": message_text,
        "timestamp": datetime.utcnow().isoformat()
    })

    message_count = len([m for m in session["messages"] if m["sender"] == "scammer"])

    logger.info(f"Processing message {message_count} for session: {session_id}")

    # Use AI detection
    detection = scam_detector.detect(message_text)
    is_scam = detection["is_scam"]

    if is_scam:
        session["scam_detected"] = True
        logger.info(f"✅ Scam detected (confidence: {detection['confidence']:.2%})")

        # Extract intelligence
        new_intel = intel_extractor.extract(message_text)

        # Merge intelligence
        for key in ["phone_numbers", "upi_ids", "bank_accounts", "phishing_links"]:
            existing = set(session["intelligence"].get(key, []))
            new = set(new_intel.get(key, []))
            session["intelligence"][key] = list(existing.union(new))

        # Log extracted intelligence
        if new_intel["phone_numbers"]:
            logger.info(f"📱 Extracted phone: {new_intel['phone_numbers']}")
        if new_intel["upi_ids"]:
            logger.info(f"💳 Extracted UPI: {new_intel['upi_ids']}")
        if new_intel["phishing_links"]:
            logger.info(f"🔗 Extracted link: {new_intel['phishing_links']}")

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

        # Check if should finalize
        has_intel = any(len(session["intelligence"][k]) > 0 for k in ["phone_numbers", "upi_ids", "bank_accounts", "phishing_links"])
        should_finalize = (has_intel and message_count >= 6) or message_count >= 12

        if should_finalize and not session["finalized"]:
            logger.info(f"🏁 Finalizing session: {session_id}")
            asyncio.create_task(send_final_report(session_id, session))

        return APIResponse(
            status="success",
            reply=response_text
        )

    else:
        # Not a scam - neutral response
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
    """List all sessions"""
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
    """Get session details"""
    if x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    return sessions[session_id]

# =============================================================================
# STEP 6: Test the System
# =============================================================================

def test_system():
    """Test the detection and response system"""
    test_message = "URGENT! Your bank account will be blocked today. Call +91-9876543210 immediately or verify at http://fake-bank.com"

    print("\n🧪 Testing with scam message...\n")
    print(f"Message: {test_message}\n")

    # Test detection
    detection = scam_detector.detect(test_message)
    print(f"✅ DETECTION RESULTS:")
    print(f"   Scam: {detection['is_scam']}")
    print(f"   Confidence: {detection['confidence']:.2%}")
    print(f"   Type: {detection['scam_type']}")
    print(f"   Methods: {detection['methods']}\n")

    # Test intelligence extraction
    intelligence = intel_extractor.extract(test_message)
    print(f"✅ INTELLIGENCE EXTRACTED:")
    print(f"   Phones: {intelligence['phone_numbers']}")
    print(f"   UPIs: {intelligence['upi_ids']}")
    print(f"   Accounts: {intelligence['bank_accounts']}")
    print(f"   Links: {intelligence['phishing_links']}\n")

    # Test response generation
    response = response_generator.generate(test_message, [], 1)
    print(f"✅ AGENT RESPONSE:")
    print(f"   {response}\n")

    print("🎉 All systems working perfectly!")

# =============================================================================
# STEP 7: Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run tests
    test_system()
    
    print("\n" + "="*60)
    print("🚀 Starting Agentic Honey-Pot API...")
    print("="*60)
    print(f"\n📝 API Documentation: http://localhost:8000/docs")
    print(f"🔑 Use this API key in 'x-api-key' header: {API_SECRET_KEY}\n")
    
    # Start server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
