#!/usr/bin/env python3
"""
Enhanced Response Generator
===========================

Multi-tier response generation system with 100% reliability.

Features:
- 3-tier fallback system (AI → Pattern → Emergency)
- Scam-type aware responses
- Stage-based conversation strategies
- Quality scoring for natural responses
- Context-aware generation

Tiers:
1. Groq Llama 3.3 70B (AI-powered, best quality)
2. Enhanced pattern-based (high quality fallback)
3. Emergency fallback (always works)

Author: Team YUKT
License: MIT
"""

import random
import re
from typing import List, Dict, Optional
from groq import Groq
import os

class EnhancedResponseGenerator:
    """Multi-tier response generation with quality scoring
    Ensures ALWAYS human-like responses even if primary API fails"""
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
        self.response_cache = {}  # Cache for similar contexts
        self.quality_threshold = 0.7  # Minimum quality score
        self.used_responses = {}  # Track used responses per session
    
    def generate(self, message: str, message_count: int, intelligence: Dict,
                 conversation_history: List[Dict], scam_type: str = "Unknown") -> str:
        """Generate response with multiple fallback layers
        Tier 1: Groq Llama 3.3 70B
        Tier 2: Enhanced pattern-based
        Tier 3: Emergency fallback"""
        
        # Tier 1: Try Groq API (Primary - Best Quality)
        if self.groq_client:
            try:
                response = self._generate_groq(message, message_count, conversation_history, scam_type)
                if response and self._assess_quality(response) >= self.quality_threshold:
                    return response
            except Exception as e:
                print(f"⚠️ Groq API failed: {e}, falling back to Tier 2")
        
        # Tier 2: Enhanced pattern-based (High Quality Fallback)
        response = self._generate_enhanced_pattern(message, message_count, intelligence, scam_type)
        if self._assess_quality(response) >= self.quality_threshold:
            return response
        
        # Tier 3: Emergency fallback (Always works)
        return self._generate_emergency_fallback(message_count)
    
    def _generate_groq(self, message: str, message_count: int, 
                       conversation_history: List[Dict], scam_type: str = "Unknown") -> Optional[str]:
        """Generate using Groq Llama 3.3 70B"""
        
        # Build context from last 5 messages
        context = self._build_context(conversation_history[-5:])
        
        # Determine strategy based on stage
        if message_count <= 2:
            strategy = "worried_victim"
        elif message_count <= 5:
            strategy = "questioning_cautious"
        elif message_count <= 8:
            strategy = "skeptical_probing"
        else:
            strategy = "highly_suspicious"
        
        # Scam-type specific context
        scam_context = self._get_scam_context(scam_type)
        
        strategies = {
            "worried_victim": "You are extremely worried and confused. Show genuine fear and concern. Ask basic questions. Keep responses SHORT (1-2 sentences max).",
            "questioning_cautious": "You're concerned but want to verify. Ask for proof, phone numbers, or employee IDs. Show hesitation about giving personal info. Keep it SHORT.",
            "skeptical_probing": "You're becoming suspicious but still engaging. Question their legitimacy. Ask probing questions. Mention checking with your bank directly. SHORT responses.",
            "highly_suspicious": "You're now very skeptical. Express doubt openly. Mention reporting to authorities or calling official numbers. Be brief but firm."
        }
        
        prompt = f"""You are roleplaying as a potential scam victim to gather intelligence.

CRITICAL RULES:
1. Keep responses VERY SHORT (1-2 sentences maximum)
2. Sound natural, like a real person texting
3. Show appropriate emotion for the stage
4. Ask questions that extract information (phone numbers, names, accounts)
5. NEVER reveal you know it's a scam
6. Use casual language, contractions (I'm, don't, can't)

SCAM TYPE DETECTED: {scam_type}
{scam_context}

STRATEGY: {strategies[strategy]}

CONVERSATION CONTEXT:
{context}

SCAMMER'S LATEST MESSAGE:
"{message}"

Generate ONLY your response as the victim (1-2 sentences max):"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model="openai/gpt-oss-120b",  # Using GPT OSS 120B for better quality
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85,  # Slightly higher for more natural variation
                max_tokens=100,    # Force brevity
                top_p=0.9
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Clean up response
            reply = self._clean_response(reply)
            return reply
            
        except Exception as e:
            print(f"Groq error: {e}")
            return None
    
    def _generate_enhanced_pattern(self, message: str, message_count: int, 
                                   intelligence: Dict, scam_type: str = "Unknown") -> str:
        """Enhanced pattern-based responses with context awareness"""
        
        msg_lower = message.lower()
        
        # Detect what scammer is asking for
        asking_for_money = any(w in msg_lower for w in ["send", "transfer", "pay", "rupees", "amount"])
        asking_for_otp = any(w in msg_lower for w in ["otp", "code", "verification"])
        asking_for_account = any(w in msg_lower for w in ["account number", "account no"])
        asking_for_password = any(w in msg_lower for w in ["password", "pin", "cvv"])
        has_link = "http" in msg_lower or "www" in msg_lower or ".com" in msg_lower
        has_phone = bool(re.search(r'\d{10}', message))
        threatening = any(w in msg_lower for w in ["blocked", "suspend", "freeze", "expire", "last chance"])
        
        # Scam-type specific responses
        is_lottery = "lottery" in scam_type.lower() or "prize" in scam_type.lower()
        is_cashback = "cashback" in scam_type.lower() or "refund" in scam_type.lower()
        is_job = "job" in scam_type.lower() or "employment" in scam_type.lower()
        
        # Stage 1: Early (1-2 messages)
        if message_count <= 2:
            if is_lottery:
                return random.choice([
                    "Really?! I won something? What prize is it?",
                    "Wow! I never win anything! How did I win?",
                    "This is amazing! What do I need to do to claim it?",
                    "I can't believe it! Is this for real? How much did I win?"
                ])
            elif is_cashback:
                return random.choice([
                    "Cashback? From which transaction? I don't remember.",
                    "How much cashback? Which app is this from?",
                    "Really? I'm getting money back? That's great!",
                    "Refund for what? Can you tell me more details?"
                ])
            elif is_job:
                return random.choice([
                    "A job offer? What kind of work is it?",
                    "Work from home? That sounds interesting! Tell me more.",
                    "How much can I earn? What are the requirements?",
                    "Is this a real job? What company is this?"
                ])
            elif threatening:
                return random.choice([
                    "What?! My account is blocked? I'm so worried!",
                    "Oh no! Why is this happening? I don't understand!",
                    "This is really scary. Can you explain what's wrong?",
                    "I'm panicking! What did I do? How do I fix this?"
                ])
            else:
                return random.choice([
                    "I'm concerned about this. Can you help me understand?",
                    "Is this really from my bank? How do I verify?",
                    "I want to make sure this is legitimate first.",
                    "What's happening with my account? I'm confused."
                ])
        
        # Stage 2: Middle (3-5 messages)
        elif message_count <= 5:
            if asking_for_money:
                return random.choice([
                    "Why do I need to send money to verify my account? That seems wrong.",
                    "I don't think banks ask for money like this. Can I call you?",
                    "I'm not comfortable sending money. Is there another way?",
                    "How much? Why? Can you give me an official number to call back?"
                ])
            elif asking_for_otp:
                return random.choice([
                    "My bank told me never to share OTP. Why do you need it?",
                    "I'm not comfortable sharing that. Can we verify another way?",
                    "Banks don't ask for OTP over calls. How do I know this is real?",
                    "I need to verify your identity first. What's your employee ID?"
                ])
            elif asking_for_account:
                return random.choice([
                    "Don't you already have my account number? Why are you asking?",
                    "I'm not sharing that without verification. Can I call you back?",
                    "What's your phone number? I want to verify with my bank first.",
                    "Give me a reference number for this call first."
                ])
            elif has_link:
                return random.choice([
                    "That link looks suspicious. Can I go to the official website instead?",
                    "I'm not comfortable clicking unknown links. Is there another way?",
                    "How do I know that's a real bank link? It doesn't look official.",
                    "Can you send this through official email? I don't trust random links."
                ])
            elif has_phone:
                return random.choice([
                    "Is that the official customer service number? Let me verify.",
                    "I'd rather use the number on my bank card. What's your name?",
                    "Can you give me your employee ID? I want to call back and confirm.",
                    "That doesn't match the number on my bank's website. Explain?"
                ])
            else:
                return random.choice([
                    "Can you give me an official contact number I can verify?",
                    "How do I know this is really from my bank? Prove it.",
                    "What department are you from? What's your supervisor's name?",
                    "I need more information before I do anything. Who are you exactly?"
                ])
        
        # Stage 3: Late (6-10 messages) - More variety and escalation
        else:
            if asking_for_password or asking_for_otp:
                responses = [
                    "No way. Banks NEVER ask for passwords. I'm reporting this.",
                    "This is definitely a scam. I'm calling the police.",
                    "I know what you're doing. I'm not falling for this scam.",
                    "Stop calling me. I'm reporting this number to cyber crime.",
                    "You're a scammer. I'm blocking this number and reporting you.",
                    "Nice try. Real banks don't ask for OTP. I'm done here.",
                    "I've recorded this conversation. I'm sending it to the authorities.",
                    "You think I'm stupid? I know this is fraud. Goodbye."
                ]
                return random.choice(responses)
            elif threatening:
                responses = [
                    "You can't scare me anymore. I'm calling my bank's official number.",
                    "I don't believe you. Real banks don't threaten customers like this.",
                    "I'm going to the bank branch in person. This feels like fraud.",
                    "I'll check with the police. This sounds like a scam to me.",
                    "Your threats don't work on me. I'm reporting this to RBI.",
                    "Real bank employees don't talk like this. I'm hanging up.",
                    "I'm taking screenshots of this conversation for evidence.",
                    "You're trying to scam me. I'm not scared of your fake threats."
                ]
                return random.choice(responses)
            elif asking_for_money:
                responses = [
                    "Banks don't ask customers to send money. This is clearly a scam.",
                    "You want ME to pay YOU? That's not how banks work. Goodbye.",
                    "I'm not sending a single rupee. This is fraud.",
                    "Nice try, but I'm not transferring any money to you.",
                    "You're asking for money? That proves this is a scam.",
                    "Real banks don't charge fees like this. I'm reporting you."
                ]
                return random.choice(responses)
            else:
                responses = [
                    "I want to verify this at my bank branch. I'm going there now.",
                    "I'm going to call my bank's official customer service to confirm.",
                    "This doesn't add up. I'm reporting this conversation.",
                    "I've been keeping a record of this. Something's not right here.",
                    "Let me speak to your manager. Give me their direct number.",
                    "I'll verify this myself through official channels. Goodbye.",
                    "I'm done with this conversation. I'll handle it at the bank.",
                    "This whole thing seems suspicious. I'm ending this call now."
                ]
                return random.choice(responses)
    
    def _generate_emergency_fallback(self, message_count: int) -> str:
        """Emergency fallback - always returns something reasonable"""
        
        fallbacks = {
            "early": [
                "I'm worried about this. Can you explain more?",
                "This is concerning. What should I do?",
                "I need to understand what's happening."
            ],
            "middle": [
                "Can I call you back to verify this?",
                "How do I know this is legitimate?",
                "I want to check with my bank first."
            ],
            "late": [
                "I'm going to verify this myself.",
                "I don't feel comfortable with this.",
                "I need to speak with my bank directly."
            ]
        }
        
        stage = "early" if message_count <= 2 else "middle" if message_count <= 5 else "late"
        return random.choice(fallbacks[stage])
    
    def _build_context(self, messages: List[Dict]) -> str:
        """Build conversation context string"""
        context_lines = []
        for msg in messages:
            sender = "Scammer" if msg.get("sender") == "scammer" else "You"
            text = msg.get("text", "")[:100]  # Limit length
            context_lines.append(f"{sender}: {text}")
        return "\n".join(context_lines)
    
    def _get_scam_context(self, scam_type: str) -> str:
        """Get context-specific guidance based on scam type"""
        contexts = {
            "Prize/Lottery Scam": "Act excited about winning! Ask what you won, how to claim it, if there are fees.",
            "Cashback/Refund Scam": "Act pleased about getting money back. Ask which transaction, how much, which app.",
            "Job/Employment Scam": "Act interested in the opportunity. Ask about salary, work details, company name.",
            "Banking/Financial Fraud": "Act worried about your account. Ask for verification, employee ID, official number.",
            "UPI/Payment Scam": "Act confused about the payment request. Ask why they need your UPI, what it's for.",
            "Phishing Link Scam": "Act hesitant about clicking links. Ask if there's another way, if it's official.",
            "KYC/Verification Scam": "Act confused why you need to verify. Ask what happens if you don't, who they are.",
            "Tax/Penalty Scam": "Act scared about penalties. Ask for proof, reference number, official contact.",
            "Investment/Trading Scam": "Act interested in making money. Ask about returns, risks, company registration."
        }
        return contexts.get(scam_type, "Act naturally based on the situation. Ask questions to extract information.")
    
    def _clean_response(self, response: str) -> str:
        """Clean up AI response"""
        # Remove common prefixes
        prefixes = ["You: ", "Response: ", "Victim: ", "Me: "]
        for prefix in prefixes:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        # Remove quotes
        response = response.strip('"\'')
        
        # Limit to 2 sentences max
        sentences = response.split('. ')
        if len(sentences) > 2:
            response = '. '.join(sentences[:2]) + '.'
        
        return response
    
    def _assess_quality(self, response: str) -> float:
        """Assess response quality (0-1 score)"""
        if not response or len(response) < 5:
            return 0.0
        
        score = 1.0
        
        # Penalize if too long (>200 chars)
        if len(response) > 200:
            score -= 0.3
        
        # Penalize if contains obvious AI markers
        ai_markers = ["as an ai", "i cannot", "i'm sorry", "however", "furthermore"]
        if any(marker in response.lower() for marker in ai_markers):
            score -= 0.5
        
        # Bonus for natural language markers
        natural_markers = ["i'm", "don't", "can't", "what?", "!"]
        if any(marker in response.lower() for marker in natural_markers):
            score += 0.1
        
        return max(0.0, min(1.0, score))
