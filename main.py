#!/usr/bin/env python3
"""
ULTIMATE AGENTIC HONEY-POT - COMPETITION-WINNING VERSION
Fully compliant with hackathon evaluation requirements
Includes: Final output submission, engagement metrics, email extraction, auto-finalization
"""

import os
import re
import random
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional

# FastAPI and dependencies
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import httpx

# AI/ML Libraries
from groq import Groq

# Enhanced intelligence extraction
from enhanced_extractor import EnhancedIntelligenceExtractor

# Enhanced response generation
from enhanced_response import EnhancedResponseGenerator

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
KIMI_API_KEY = os.getenv("KIMI_API_KEY")
KIMI_MODEL = os.getenv("KIMI_MODEL", "deepseek/deepseek-r1-0528:free")
KIMI_BASE_URL = os.getenv("KIMI_BASE_URL", "https://openrouter.ai/api/v1")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M")
GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

# Handle OpenRouter
if LLM_PROVIDER == 'openrouter':
    if OPENROUTER_API_KEY:
        KIMI_API_KEY = OPENROUTER_API_KEY
    KIMI_BASE_URL = 'https://openrouter.ai/api/v1'
    LLM_PROVIDER = 'kimi'

# Initialize AI client
if LLM_PROVIDER == 'groq' and GROQ_API_KEY:
    from groq import Groq
    ai_client = Groq(api_key=GROQ_API_KEY)
    ai_model = GROQ_MODEL
    logger.info(f"✅ Using Groq: {GROQ_MODEL}")
elif LLM_PROVIDER == 'kimi' and KIMI_API_KEY:
    from openai import OpenAI
    ai_client = OpenAI(api_key=KIMI_API_KEY, base_url=KIMI_BASE_URL)
    ai_model = KIMI_MODEL
    logger.info(f"✅ Using {KIMI_MODEL} via {KIMI_BASE_URL}")
else:
    ai_client = None
    ai_model = None
    logger.warning("⚠️ No AI client configured - using fallback responses")

# FastAPI app
app = FastAPI(
    title="Ultimate Agentic Honey-Pot - Competition Edition",
    description="Advanced AI System for Scam Detection with Full Evaluation Compliance",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
    
    @app.get("/ui")
    async def serve_ui():
        return FileResponse("frontend/index.html")

# Pydantic models
class Message(BaseModel):
    sender: str = "scammer"
    text: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class Metadata(BaseModel):
    channel: str = "SMS"
    language: str = "English"
    locale: str = "IN"

class IncomingRequest(BaseModel):
    sessionId: Optional[str] = None
    message: Optional[Message] = None
    conversationHistory: List[Message] = []
    metadata: Optional[Metadata] = None

class APIResponse(BaseModel):
    status: str = "success"
    reply: str

# Session storage
sessions = {}

# Scam detector
class AdvancedScamDetector:
    def __init__(self):
        self.scam_keywords = {
            "urgent": 3, "immediately": 3, "now": 2, "asap": 3,
            "blocked": 4, "suspended": 4, "freeze": 4, "locked": 4,
            "verify": 2, "confirm": 2, "update": 2, "click": 3,
            "account": 2, "bank": 2, "upi": 3, "payment": 2,
            "otp": 5, "cvv": 5, "pin": 5, "password": 5,
            "winner": 4, "prize": 4, "lottery": 4, "won": 3,
        }
    
    def detect(self, message: str) -> Dict:
        msg_lower = message.lower()
        
        # Keyword scoring
        keyword_score = sum(weight for kw, weight in self.scam_keywords.items() if kw in msg_lower)
        keyword_score = min(keyword_score / 15.0, 1.0)
        
        # Pattern detection
        has_urgency = any(w in msg_lower for w in ["urgent", "immediately", "now", "asap"])
        has_threat = any(w in msg_lower for w in ["blocked", "suspended", "freeze"])
        has_action = any(w in msg_lower for w in ["verify", "click", "call", "send"])
        has_financial = any(w in msg_lower for w in ["account", "bank", "upi", "otp"])
        
        pattern_score = 0.0
        if has_urgency and has_threat and has_action:
            pattern_score = 1.0
        elif (has_urgency and has_threat) or (has_threat and has_action):
            pattern_score = 0.7
        elif has_urgency or has_threat:
            pattern_score = 0.4
        
        # Combined score
        total_score = (keyword_score * 0.5 + pattern_score * 0.5)
        
        # Classify scam type
        scam_type = "Unknown"
        if "bank" in msg_lower or "account" in msg_lower:
            scam_type = "Banking/Financial Fraud"
        elif "upi" in msg_lower:
            scam_type = "UPI/Payment Scam"
        elif "otp" in msg_lower or "cvv" in msg_lower:
            scam_type = "Credential Phishing"
        elif "winner" in msg_lower or "prize" in msg_lower:
            scam_type = "Prize/Lottery Scam"
        
        return {
            "is_scam": total_score > 0.35,
            "confidence": total_score,
            "scam_type": scam_type
        }

scam_detector = AdvancedScamDetector()

# Initialize enhanced intelligence extractor
intelligence_extractor = EnhancedIntelligenceExtractor()

# Initialize enhanced response generator
response_generator = EnhancedResponseGenerator()

# Intelligence extractor (DEPRECATED - using enhanced version now)
def extract_intelligence(message: str) -> Dict:
    intel = {
        "phoneNumbers": [],
        "upiIds": [],
        "bankAccounts": [],
        "phishingLinks": [],
        "emailAddresses": []
    }
    
    # Phone numbers
    phone_patterns = [r'\+91[\s-]?\d{10}', r'\b[6-9]\d{9}\b']
    for pattern in phone_patterns:
        matches = re.findall(pattern, message)
        for match in matches:
            cleaned = re.sub(r'\D', '', match)
            if len(cleaned) == 10 and cleaned not in intel["phoneNumbers"]:
                intel["phoneNumbers"].append(cleaned)
    
    # UPI IDs
    upi_matches = re.findall(r'[\w\.-]+@[\w]+', message, re.IGNORECASE)
    for match in upi_matches:
        if '@' in match and '.' not in match.split('@')[1]:
            if match.lower() not in intel["upiIds"]:
                intel["upiIds"].append(match.lower())
    
    # Email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, message)
    for match in email_matches:
        if match.lower() not in intel["emailAddresses"]:
            intel["emailAddresses"].append(match.lower())
    
    # Bank accounts
    account_matches = re.findall(r'\b\d{9,18}\b', message)
    for match in account_matches:
        if match not in intel["bankAccounts"]:
            intel["bankAccounts"].append(match)
    
    # URLs
    url_patterns = [r'https?://[^\s]+', r'www\.[^\s]+']
    for pattern in url_patterns:
        url_matches = re.findall(pattern, message, re.IGNORECASE)
        for match in url_matches:
            if match not in intel["phishingLinks"]:
                intel["phishingLinks"].append(match)
    
    return intel

# Advanced response generator
def generate_intelligent_response(message: str, message_count: int, conversation_history: List[Dict], intelligence: Dict) -> str:
    """Generate context-aware, intelligent responses"""
    
    msg_lower = message.lower()
    
    # Determine conversation stage
    if message_count <= 2:
        stage = "early"
    elif message_count <= 6:
        stage = "middle"
    else:
        stage = "late"
    
    # Use AI if available
    if ai_client and ai_model:
        try:
            # Build context
            context = "\n".join([
                f"{'Scammer' if m['sender']=='scammer' else 'You'}: {m['text']}"
                for m in conversation_history[-5:]
            ])
            
            prompt = f"""You are roleplaying as a potential scam victim to extract information from scammers.

CRITICAL RULES:
1. Act like a REAL person - confused, worried, asking questions
2. Extract information by asking for: phone numbers, employee IDs, names, email addresses, office locations
3. Keep responses SHORT (1-2 sentences max)
4. Show emotions: worry, confusion, suspicion
5. NEVER reveal you know it's a scam
6. Make occasional typos (missing apostrophes, etc.)

STAGE: {stage}
- Early: Confused and worried, believe them but scared
- Middle: Asking for verification, becoming suspicious
- Late: Very skeptical, want to verify independently

CONVERSATION:
{context}
Scammer: {message}

Respond as the victim. Be natural and extract information:"""
            
            response = ai_client.chat.completions.create(
                model=ai_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=60  # Reduced for faster response
            )
            
            reply = response.choices[0].message.content.strip()
            reply = reply.strip('"\'')
            for prefix in ["You: ", "Response: ", "Victim: "]:
                if reply.startswith(prefix):
                    reply = reply[len(prefix):].strip()
            
            return reply
            
        except Exception as e:
            logger.warning(f"AI generation failed: {e}, using fallback")
    
    # Fallback responses (context-aware)
    asking_for_money = any(w in msg_lower for w in ["send", "transfer", "pay", "rupees"])
    has_link = "http" in msg_lower or "www" in msg_lower
    has_phone = bool(re.search(r'\d{10}', message))
    asking_for_info = any(w in msg_lower for w in ["account", "otp", "password", "cvv"])
    
    if stage == "early":
        if asking_for_money:
            return "Why do I need to send money? Can you give me your phone number so I can call back?"
        elif has_link:
            return "Im not sure about that link... Can you send me an official email instead?"
        elif asking_for_info:
            return "Wait, why do you need my account number? Dont you already have it? Whats your employee ID?"
        else:
            return "What?! My account is blocked? I dont understand! Can you explain whats happening?"
    
    elif stage == "middle":
        if asking_for_money:
            return "This doesnt sound right. Can I come to the bank branch instead? Which branch are you from?"
        elif has_link:
            return "How do I know that link is safe? Can you give me your full name and department?"
        elif has_phone:
            return "Is that the official number? Can you give me your employee ID so I can verify?"
        else:
            return "Im getting suspicious. Can you prove youre really from my bank? Whats your managers name?"
    
    else:  # late stage
        return "I want to verify this at my bank branch. Let me call the official customer service number first."

# Calculate engagement metrics
def calculate_engagement_metrics(session: Dict) -> Dict:
    messages = session["messages"]
    total_messages = len(messages)
    
    if len(messages) >= 2:
        try:
            first_time = datetime.fromisoformat(messages[0]["timestamp"].replace('Z', '+00:00'))
            last_time = datetime.fromisoformat(messages[-1]["timestamp"].replace('Z', '+00:00'))
            duration = int((last_time - first_time).total_seconds())
        except:
            duration = max(15 * (total_messages // 2), 0)
    else:
        duration = 0
    
    return {
        "totalMessagesExchanged": total_messages,
        "engagementDurationSeconds": duration
    }

# Build final output
def build_final_output(session_id: str, session: Dict) -> Dict:
    intel = session["intelligence"]
    metrics = calculate_engagement_metrics(session)
    
    # Build agent notes
    notes_parts = []
    if session["scam_detected"]:
        scam_type = session.get('scam_type', 'Unknown')
        confidence = session.get('scam_confidence', 0.0)
        notes_parts.append(f"Scam detected: {scam_type} with {confidence:.1%} confidence and {metrics['totalMessagesExchanged']} exchanges.")
        if intel["phoneNumbers"]:
            notes_parts.append(f"Extracted {len(intel['phoneNumbers'])} phone number(s).")
        if intel["upiIds"]:
            notes_parts.append(f"Extracted {len(intel['upiIds'])} UPI ID(s).")
        if intel["bankAccounts"]:
            notes_parts.append(f"Extracted {len(intel['bankAccounts'])} bank account(s).")
        if intel["phishingLinks"]:
            notes_parts.append(f"Detected {len(intel['phishingLinks'])} phishing link(s).")
        if intel["emailAddresses"]:
            notes_parts.append(f"Extracted {len(intel['emailAddresses'])} email(s).")
    else:
        notes_parts.append("No scam pattern detected.")
    
    return {
        "status": "success",
        "sessionId": session_id,
        "scamDetected": session["scam_detected"],
        "scamType": session.get('scam_type', 'Unknown'),
        "confidenceLevel": round(session.get('scam_confidence', 0.0), 2),
        "totalMessagesExchanged": metrics["totalMessagesExchanged"],
        "extractedIntelligence": intel,
        "engagementMetrics": metrics,
        "agentNotes": " ".join(notes_parts)
    }


# GUVI callback
async def send_to_guvi(final_output: Dict):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(GUVI_CALLBACK_URL, json=final_output)
            if response.status_code == 200:
                logger.info(f"✅ Sent to GUVI: {final_output['sessionId']}")
            else:
                logger.error(f"❌ GUVI callback failed: {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Error sending to GUVI: {e}")

# API endpoints
@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Ultimate Agentic Honey-Pot",
        "version": "2.0.0",
        "llm_provider": LLM_PROVIDER,
        "model": ai_model if ai_model else "fallback"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "active_sessions": len(sessions),
        "ai_enabled": ai_client is not None
    }

@app.post("/api/message", response_model=APIResponse)
async def handle_message(request: Request, x_api_key: Optional[str] = Header(None)):
    # Verify API key
    if not x_api_key or x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Parse request
    try:
        body = await request.json()
    except:
        body = {}
    
    if not body:
        return APIResponse(status="success", reply="Hello, how can I help you?")
    
    # Extract session ID
    session_id = body.get("sessionId", f"session-{int(datetime.now(timezone.utc).timestamp())}")
    
    # Extract message
    if "message" in body and isinstance(body["message"], dict):
        message_text = body["message"].get("text", "")
        message_sender = body["message"].get("sender", "scammer")
    else:
        message_text = ""
        message_sender = "scammer"
    
    if not message_text:
        return APIResponse(status="success", reply="I'm here. What's the issue?")
    
    # Initialize session
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "scam_detected": False,
            "intelligence": {
                "phoneNumbers": [],
                "upiIds": [],
                "bankAccounts": [],
                "phishingLinks": [],
                "emailAddresses": []
            },
            "finalized": False,
            "start_time": datetime.now(timezone.utc),
            "scam_type": "Unknown",
            "scam_confidence": 0.0
        }
    
    session = sessions[session_id]
    
    # Add message
    session["messages"].append({
        "sender": message_sender,
        "text": message_text,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    message_count = len([m for m in session["messages"] if m["sender"] == "scammer"])
    logger.info(f"📨 Message {message_count} for {session_id}: {message_text[:80]}...")
    
    # Detect scam
    detection = scam_detector.detect(message_text)
    if detection["is_scam"]:
        session["scam_detected"] = True
        session["scam_type"] = detection["scam_type"]
        session["scam_confidence"] = detection["confidence"]
        logger.info(f"✅ Scam: {detection['scam_type']} ({detection['confidence']:.2%})")
    
    # Extract intelligence using ENHANCED extractor
    message_history = [m["text"] for m in session["messages"]]
    new_intel = intelligence_extractor.extract(message_text, message_history)
    for key in new_intel:
        existing = set(session["intelligence"].get(key, []))
        new_items = set(new_intel[key])
        session["intelligence"][key] = list(existing.union(new_items))
    
    # Log intelligence
    if new_intel["phoneNumbers"]:
        logger.info(f"   📱 Phone: {new_intel['phoneNumbers']}")
    if new_intel["upiIds"]:
        logger.info(f"   💳 UPI: {new_intel['upiIds']}")
    if new_intel["emailAddresses"]:
        logger.info(f"   📧 Email: {new_intel['emailAddresses']}")
    
    # Generate response using ENHANCED generator
    response_text = response_generator.generate(
        message_text,
        message_count,
        session["intelligence"],
        session["messages"]
    )
    
    session["messages"].append({
        "sender": "user",
        "text": response_text,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    logger.info(f"   💬 Reply: {response_text}")
    
    # Auto-finalize after 10 turns
    if message_count >= 10 and not session["finalized"]:
        logger.info(f"🏁 Auto-finalizing {session_id}")
        session["finalized"] = True
        final_output = build_final_output(session_id, session)
        asyncio.create_task(send_to_guvi(final_output))
    
    return APIResponse(status="success", reply=response_text)

@app.get("/api/sessions")
async def list_sessions(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "total_sessions": len(sessions),
        "sessions": {
            sid: {
                "messages": len(s["messages"]),
                "scam_detected": s["scam_detected"],
                "finalized": s["finalized"]
            }
            for sid, s in sessions.items()
        }
    }

@app.get("/api/session/{session_id}")
async def get_session(session_id: str, x_api_key: Optional[str] = Header(None)):
    """Get session details including final output"""
    if not x_api_key or x_api_key != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    final_output = build_final_output(session_id, session)
    
    return {
        "session": session,
        "finalOutput": final_output
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print("\n" + "="*60)
    print("🚀 Starting Ultimate Agentic Honey-Pot...")
    print("="*60)
    print(f"📝 API: http://localhost:{port}/docs")
    print(f"🌐 UI: http://localhost:{port}/ui")
    print(f"🤖 LLM: {LLM_PROVIDER} - {ai_model if ai_model else 'fallback'}")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
