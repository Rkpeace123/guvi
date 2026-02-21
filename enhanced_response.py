#!/usr/bin/env python3
"""
ULTIMATE Human-Like Response Generator v3.0
==========================================

The most advanced scam baiting system with:
- Zero repetition (tracks every response used)
- Strategic conversation flow (builds rapport, extracts incrementally)
- Human-like dialogue patterns (callbacks, references, natural progression)
- Brilliant intelligence extraction (asks the right questions at the right time)
- Emotional authenticity (worry → trust → doubt → suspicion)

This is not just response generation - it's psychological manipulation for good.

Author: Team YUKT
License: MIT
"""

import random
import re
from typing import List, Dict, Optional, Set, Tuple
from groq import Groq
import os
from datetime import datetime

class UltimateHumanLikeGenerator:
    """
    Master-level scam baiting with zero repetition and strategic extraction
    """
    
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
        
        # Per-session memory - tracks everything
        self.sessions = {}
        
    def generate(self, session_id: str, message: str, message_count: int,
                 intelligence: Dict, conversation_history: List[Dict],
                 scam_type: str = "unknown") -> str:
        """
        Generate unique, strategic, human-like response
        Never repeats. Always extracts. Feels completely real.
        """
        
        # Initialize session memory
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "used_responses": set(),
                "asked_questions": set(),
                "mentioned_facts": set(),  # Things victim has "said" about themselves
                "scammer_claims": [],      # What scammer has claimed
                "extraction_priorities": self._get_extraction_priorities(scam_type),
                "rapport_level": 0,        # 0-10, how much scammer trusts us
                "emotional_state": "worried",  # worried → cautious → skeptical → defensive
                "conversation_style": self._determine_persona(scam_type),
                "last_topic": None,
                "scammer_info": {          # What we know about scammer
                    "name": None,
                    "role": None,
                    "organization": None,
                    "phone": None,
                    "email": None
                }
            }
        
        state = self.sessions[session_id]
        
        # Analyze scammer's latest message
        self._analyze_scammer_message(message, intelligence, state, scam_type)
        
        # Update emotional state based on conversation progress
        self._update_emotional_state(message_count, intelligence, state)
        
        # Determine extraction strategy
        strategy = self._get_extraction_strategy(message_count, intelligence, state)
        
        # Try advanced Groq generation first
        if self.groq_client:
            try:
                response = self._generate_advanced_groq(
                    session_id, message, message_count, conversation_history,
                    scam_type, state, strategy
                )
                if response and self._is_high_quality(response, state):
                    state["used_responses"].add(self._normalize(response))
                    return response
            except Exception as e:
                print(f"⚠️ Groq failed: {e}")
        
        # Fallback to strategic pattern-based (still very good)
        response = self._generate_strategic_human_response(
            message, message_count, intelligence, scam_type, state, strategy
        )
        
        # Ensure absolute uniqueness
        response = self._ensure_unique(response, state)
        state["used_responses"].add(self._normalize(response))
        
        return response
    
    def _analyze_scammer_message(self, message: str, intelligence: Dict,
                                 state: Dict, scam_type: str):
        """Deep analysis of scammer's message to inform our strategy"""
        
        msg_lower = message.lower()
        
        # What has scammer revealed?
        if "my name is" in msg_lower or "i am" in msg_lower:
            # Extract name claim
            name_match = re.search(r'(?:my name is|i am|this is)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', message, re.IGNORECASE)
            if name_match and not state["scammer_info"]["name"]:
                state["scammer_info"]["name"] = name_match.group(1)
                state["rapport_level"] += 1
        
        if "employee" in msg_lower or "staff" in msg_lower or "officer" in msg_lower:
            role_match = re.search(r'(manager|officer|executive|agent|representative|employee)', msg_lower)
            if role_match and not state["scammer_info"]["role"]:
                state["scammer_info"]["role"] = role_match.group(1)
        
        if "bank" in msg_lower or "company" in msg_lower:
            org_match = re.search(r'(hdfc|icici|sbi|axis|paytm|phonepe|google pay|bank)', msg_lower)
            if org_match and not state["scammer_info"]["organization"]:
                state["scammer_info"]["organization"] = org_match.group(1)
        
        # Track scammer's claims
        if "urgent" in msg_lower or "immediately" in msg_lower:
            if "urgency_tactic" not in state["scammer_claims"]:
                state["scammer_claims"].append("urgency_tactic")
        
        if "blocked" in msg_lower or "suspended" in msg_lower:
            if "account_threat" not in state["scammer_claims"]:
                state["scammer_claims"].append("account_threat")
        
        if "win" in msg_lower or "prize" in msg_lower or "lottery" in msg_lower:
            if "prize_claim" not in state["scammer_claims"]:
                state["scammer_claims"].append("prize_claim")
        
        # Update extraction priorities based on what we still need
        self._update_extraction_priorities(intelligence, state)
    
    def _update_emotional_state(self, message_count: int, intelligence: Dict, state: Dict):
        """Update victim's emotional state - this drives the conversation tone"""
        
        # Natural progression: worried → cautious → skeptical → defensive
        if message_count <= 2:
            state["emotional_state"] = "worried"
        elif message_count <= 4:
            state["emotional_state"] = "cautious"
            state["rapport_level"] = min(state["rapport_level"] + 1, 10)
        elif message_count <= 6:
            state["emotional_state"] = "questioning"
        elif message_count <= 8:
            state["emotional_state"] = "skeptical"
        else:
            state["emotional_state"] = "defensive"
    
    def _get_extraction_strategy(self, message_count: int, intelligence: Dict,
                                 state: Dict) -> str:
        """
        Determine what to extract next based on what we have and conversation flow
        This is the KEY to brilliant intelligence gathering
        """
        
        priorities = state["extraction_priorities"]
        rapport = state["rapport_level"]
        
        # Early game: Build rapport and get basic contact info
        if message_count <= 3:
            if not intelligence.get("phoneNumbers"):
                return "extract_phone_naturally"
            return "build_rapport"
        
        # Mid game: Get identity and organizational info
        elif message_count <= 6:
            if not state["scammer_info"]["name"]:
                return "extract_name"
            elif not state["scammer_info"]["role"]:
                return "extract_role"
            elif not intelligence.get("emailAddresses"):
                return "extract_email"
            return "extract_organizational_info"
        
        # Late game: Get payment/account details
        elif message_count <= 8:
            if not intelligence.get("upiIds") and not intelligence.get("bankAccounts"):
                return "extract_payment_info"
            return "probe_process"
        
        # End game: Get any remaining intel before exit
        else:
            return "final_extraction"
    
    def _generate_advanced_groq(self, session_id: str, message: str, message_count: int,
                               conversation_history: List[Dict], scam_type: str,
                               state: Dict, strategy: str) -> Optional[str]:
        """
        Advanced Groq generation with deep context and strategic prompting
        """
        
        # Build rich context
        context = self._build_detailed_context(conversation_history[-6:], state)
        
        # What we've already done
        already_done = self._summarize_conversation_arc(state)
        
        # Strategic instruction based on current strategy
        strategy_instruction = self._get_strategy_instruction(strategy, state)
        
        # Persona consistency
        persona_note = self._get_persona_note(state["conversation_style"])
        
        prompt = f"""You are an expert at playing a realistic scam victim to extract information. Your responses must be:

1. UNIQUE - Never repeat questions or phrases used before
2. NATURAL - Sound like real text messages (casual, brief, authentic)
3. STRATEGIC - Each response should extract specific information
4. CONSISTENT - Maintain the persona and emotional state

VICTIM PERSONA: {persona_note}

EMOTIONAL STATE: {state['emotional_state']}
RAPPORT LEVEL: {state['rapport_level']}/10

SCAM TYPE: {scam_type}

CONVERSATION SO FAR:
{context}

WHAT YOU'VE ALREADY DONE:
{already_done}

CURRENT STRATEGY: {strategy}
{strategy_instruction}

WHAT WE KNOW ABOUT SCAMMER:
- Name: {state['scammer_info']['name'] or 'Unknown'}
- Role: {state['scammer_info']['role'] or 'Unknown'}
- Organization: {state['scammer_info']['organization'] or 'Unknown'}

SCAMMER'S LATEST MESSAGE:
"{message}"

CRITICAL RULES:
- Keep it SHORT (15-30 words max)
- Sound like a REAL person texting
- NO repetition of previous questions
- Extract information through natural curiosity
- Show appropriate emotion for {state['emotional_state']} state
- Reference previous conversation naturally

Generate ONLY the victim's response (conversational, brief):"""
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.92,  # High for uniqueness
                max_tokens=100,
                top_p=0.95
            )
            
            reply = response.choices[0].message.content.strip()
            reply = self._clean_response(reply)
            
            # Track what we asked
            self._track_questions(reply, state)
            
            return reply
            
        except Exception as e:
            print(f"Groq error: {e}")
            return None
    
    def _generate_strategic_human_response(self, message: str, message_count: int,
                                          intelligence: Dict, scam_type: str,
                                          state: Dict, strategy: str) -> str:
        """
        Generate strategic responses based on extraction needs
        Each response pool is large and varied - no repetition
        """
        
        msg_lower = message.lower()
        
        # Analyze scammer's ask
        asking_for_money = any(w in msg_lower for w in ["send", "transfer", "pay", "deposit"])
        asking_for_otp = "otp" in msg_lower or "code" in msg_lower or "verification code" in msg_lower
        asking_for_password = any(w in msg_lower for w in ["password", "pin", "cvv", "card number"])
        has_phone = bool(re.search(r'\d{10}', message))
        has_link = "http" in msg_lower or "www" in msg_lower or "bit.ly" in msg_lower
        gave_name = state["scammer_info"]["name"] is not None
        
        # Strategy-based response generation
        if strategy == "extract_phone_naturally":
            return self._get_phone_extraction_response(state, gave_name)
        
        elif strategy == "build_rapport":
            return self._get_rapport_building_response(scam_type, state)
        
        elif strategy == "extract_name":
            return self._get_name_extraction_response(state)
        
        elif strategy == "extract_role":
            return self._get_role_extraction_response(state)
        
        elif strategy == "extract_email":
            return self._get_email_extraction_response(state)
        
        elif strategy == "extract_organizational_info":
            return self._get_org_info_response(state)
        
        elif strategy == "extract_payment_info":
            if asking_for_money:
                return self._get_payment_probe_response(state)
            else:
                return self._get_general_payment_question(state)
        
        elif strategy == "probe_process":
            return self._get_process_probe_response(msg_lower, state)
        
        elif strategy == "final_extraction":
            return self._get_final_extraction_response(state)
        
        # Contextual responses based on scammer's ask
        if asking_for_otp:
            return self._get_otp_refusal_response(message_count, state)
        
        if asking_for_password:
            return self._get_password_refusal_response(message_count, state)
        
        if has_link:
            return self._get_link_probe_response(state)
        
        # Default to emotional state-based response
        return self._get_emotional_state_response(state)
    
    # ============= EXTRACTION RESPONSE POOLS =============
    
    def _get_phone_extraction_response(self, state: Dict, gave_name: bool) -> str:
        """Get phone number naturally"""
        responses = [
            "What number should I call you back on?",
            "Can you give me your direct number?",
            "What's the helpline I should call?",
            "Is there a number where I can reach you?",
            "What if we get disconnected? Your number?",
            "Give me your contact so I can call back?",
            "What's your phone number in case I need help?",
            "Can I have a callback number?",
            "What's your mobile in case call drops?",
            "Is there a hotline number you're calling from?"
        ]
        
        if gave_name:
            responses.extend([
                f"Thanks {state['scammer_info']['name']}, what's your number?",
                f"Okay {state['scammer_info']['name']}, how do I reach you?",
                f"Got it {state['scammer_info']['name']}, give me your contact?"
            ])
        
        return self._pick_unused(responses, state)
    
    def _get_rapport_building_response(self, scam_type: str, state: Dict) -> str:
        """Build trust with scammer"""
        
        if "lottery" in scam_type or "prize" in scam_type:
            responses = [
                "Wow this is exciting! What exactly did I win?",
                "Really? That's amazing! How was the winner selected?",
                "I can't believe this! What's the prize worth?",
                "This made my day! When can I claim it?",
                "That's incredible! What's the process now?",
                "I'm so lucky! Who's sponsoring this?",
                "Best news ever! What do I do next?"
            ]
        elif "job" in scam_type:
            responses = [
                "That sounds like a great opportunity! Tell me more?",
                "I'm interested! What's the job exactly?",
                "Work from home? That's perfect for me!",
                "This is exactly what I needed! What's the pay?",
                "Tell me more about this position?",
                "Sounds good! What are the working hours?",
                "I'd love to know more! What's required?"
            ]
        else:  # Banking/urgent
            responses = [
                "Okay I'm listening. What happened?",
                "Alright, walk me through this?",
                "I understand. What should I do?",
                "Tell me everything. I'm worried.",
                "Explain it to me please.",
                "I'm ready to fix this. Guide me?",
                "Okay I'm here. What's the next step?"
            ]
        
        return self._pick_unused(responses, state)
    
    def _get_name_extraction_response(self, state: Dict) -> str:
        """Extract scammer's name"""
        responses = [
            "Sorry, what was your name again?",
            "Who am I speaking with?",
            "Can I get your name please?",
            "What should I call you?",
            "Who's helping me with this?",
            "Your name is...?",
            "May I know who you are?",
            "What's your full name?",
            "Can you tell me your name?",
            "Who's on the line?",
            "I didn't catch your name?",
            "What do I call you?",
            "Name please?",
            "Your good name?"  # Indian English style
        ]
        return self._pick_unused(responses, state)
    
    def _get_role_extraction_response(self, state: Dict) -> str:
        """Extract scammer's role"""
        name = state['scammer_info']['name']
        
        responses = [
            "What's your position exactly?",
            "What department are you from?",
            "Are you a manager or agent?",
            "What's your role there?",
            "What do you do at the company?",
            "Are you calling from customer service?",
            "What's your designation?",
            "Which team are you with?",
            "What's your job title?"
        ]
        
        if name:
            responses.extend([
                f"What do you do there, {name}?",
                f"{name}, what's your designation?",
                f"Which department, {name}?"
            ])
        
        return self._pick_unused(responses, state)
    
    def _get_email_extraction_response(self, state: Dict) -> str:
        """Extract email address"""
        responses = [
            "Can you email me the details?",
            "What's your official email?",
            "Send me an email so I have it in writing?",
            "What's the company email I should write to?",
            "Email me the verification?",
            "Can I get your email address?",
            "What email should I contact?",
            "Send me an email confirmation?",
            "What's your work email?",
            "Can you put this in an email?",
            "Email this to me please?",
            "What's the support email?"
        ]
        return self._pick_unused(responses, state)
    
    def _get_org_info_response(self, state: Dict) -> str:
        """Get organizational details"""
        responses = [
            "Which branch is this?",
            "What's your employee ID?",
            "Who's your supervisor?",
            "What's the office address?",
            "Which city are you calling from?",
            "What's your extension number?",
            "Who should I ask for if I call back?",
            "What's the department code?",
            "Which location?",
            "What office?",
            "Give me your ID number?",
            "What's your badge number?",
            "Your employee code?",
            "Which center handles this?"
        ]
        return self._pick_unused(responses, state)
    
    def _get_payment_probe_response(self, state: Dict) -> str:
        """When scammer asks for payment, probe for details"""
        responses = [
            "Where exactly do I send the money?",
            "What account number?",
            "Which UPI should I use?",
            "Give me the payment details?",
            "How much and where?",
            "What's the receiving account?",
            "Send me your UPI ID?",
            "What are the bank details?",
            "Where do I transfer to?",
            "What's the payment method?",
            "Which account receives this?",
            "Give me the full payment info?",
            "What's the beneficiary name?",
            "How should I send it?"
        ]
        return self._pick_unused(responses, state)
    
    def _get_otp_refusal_response(self, message_count: int, state: Dict) -> str:
        """Refuse OTP requests naturally"""
        
        if message_count <= 4:
            # Early: Cautious
            responses = [
                "My bank said never share OTP. Why do you need it?",
                "I thought we're not supposed to share OTP?",
                "Isn't OTP private? Why do you need mine?",
                "I'm not comfortable sharing that. Is there another way?",
                "Banks tell us not to give OTP to anyone?",
                "Can we verify without the OTP?"
            ]
        else:
            # Late: Suspicious
            responses = [
                "No way. Banks NEVER ask for OTP.",
                "You're asking for OTP? That's suspicious.",
                "Real bank staff don't need my OTP.",
                "I know scammers ask for OTP. Why are you?",
                "This is exactly what scams do. Asking for OTP.",
                "Nope. Not sharing OTP with anyone.",
                "That's a red flag. Banks don't ask for OTP."
            ]
        
        return self._pick_unused(responses, state)
    
    def _get_password_refusal_response(self, message_count: int, state: Dict) -> str:
        """Refuse password/PIN requests"""
        responses = [
            "Banks never ask for passwords. Why do you need mine?",
            "I'm not sharing my password with anyone.",
            "That's confidential. Real banks don't ask for it.",
            "No one should ask for passwords. This seems wrong.",
            "I know better than to share my PIN.",
            "This is a major red flag. Why password?",
            "Absolutely not. No one gets my password.",
            "Banks specifically say never share passwords."
        ]
        return self._pick_unused(responses, state)
    
    def _get_link_probe_response(self, state: Dict) -> str:
        """Probe about suspicious links"""
        responses = [
            "What's this link for?",
            "Is that the official website?",
            "That URL looks weird. Is it safe?",
            "Why can't I use the regular bank site?",
            "What happens when I click this?",
            "Is this link secure?",
            "Can you send the official link instead?",
            "Why a shortened link? What's the full URL?",
            "I don't trust random links. Why this one?",
            "What domain is this?",
            "Is this verified by the bank?",
            "That doesn't look like an official link?"
        ]
        return self._pick_unused(responses, state)
    
    def _get_process_probe_response(self, msg_lower: str, state: Dict) -> str:
        """Ask about the process to get more details"""
        responses = [
            "Walk me through the exact steps?",
            "What's the complete process?",
            "Explain how this works?",
            "What happens after I do this?",
            "Then what's next?",
            "How long will this take?",
            "What do I need to do exactly?",
            "Can you explain the full procedure?",
            "What's step 2, 3, etc?",
            "Break it down for me?",
            "What's required from my end?",
            "How does this whole thing work?"
        ]
        return self._pick_unused(responses, state)
    
    def _get_final_extraction_response(self, state: Dict) -> str:
        """Last chance to extract anything remaining"""
        
        if not state["scammer_info"]["phone"]:
            return "Give me all your contact details before we proceed?"
        
        responses = [
            "Let me confirm everything. Your full details?",
            "Just to verify - your complete information?",
            "Send me all the details one more time?",
            "What's your full contact information?",
            "I need all your details to report this properly.",
            "Give me everything - name, number, email, ID?",
            "Let me note down your complete information?",
            "What are all your contact details?"
        ]
        return self._pick_unused(responses, state)
    
    def _get_emotional_state_response(self, state: Dict) -> str:
        """Response based on emotional state"""
        
        emotion = state["emotional_state"]
        
        if emotion == "worried":
            responses = [
                "I'm really concerned about this.",
                "This is making me anxious.",
                "I'm worried. Help me understand?",
                "This is stressful. What should I do?",
                "I'm scared about what's happening.",
                "Please tell me this is fixable?"
            ]
        elif emotion == "cautious":
            responses = [
                "Let me just verify a few things first?",
                "I want to make sure this is legitimate.",
                "Before I proceed, I need some clarity.",
                "Hold on, let me confirm something.",
                "I need to be careful here.",
                "Let me check this with someone."
            ]
        elif emotion == "questioning":
            responses = [
                "Something doesn't add up here.",
                "Why is this process so complicated?",
                "This doesn't match what I know.",
                "I have some doubts about this.",
                "Can you clarify why you need this?",
                "This seems unusual. Explain?"
            ]
        elif emotion == "skeptical":
            responses = [
                "I'm not sure I believe this.",
                "This really sounds like a scam.",
                "I've heard about frauds like this.",
                "You're asking for things that seem wrong.",
                "This doesn't feel right to me.",
                "I think you might be trying to scam me."
            ]
        else:  # defensive
            responses = [
                "I'm not doing any of this.",
                "I'm reporting this conversation.",
                "You're definitely a scammer.",
                "I'm calling the police.",
                "I know exactly what you're doing.",
                "This conversation is over.",
                "I'm blocking this number.",
                "Nice try. I'm not falling for it."
            ]
        
        return self._pick_unused(responses, state)
    
    # ============= HELPER METHODS =============
    
    def _pick_unused(self, responses: List[str], state: Dict) -> str:
        """Pick a response that hasn't been used"""
        available = [r for r in responses if self._normalize(r) not in state["used_responses"]]
        
        if not available:
            # All used, create variations
            available = [self._create_variation(r) for r in responses[:3]]
        
        return random.choice(available)
    
    def _create_variation(self, response: str) -> str:
        """Create variation of used response"""
        
        variations = [
            f"Um, {response.lower()}",
            f"Wait, {response.lower()}",
            f"So {response.lower()}",
            f"Actually, {response.lower()}",
            response.replace("Can you", "Could you"),
            response.replace("What's", "What is"),
            response.replace("?", " please?"),
            response.rstrip("?") + " exactly?",
            f"Quick question - {response.lower()}"
        ]
        
        return random.choice(variations)
    
    def _ensure_unique(self, response: str, state: Dict) -> str:
        """Absolutely ensure response is unique"""
        
        normalized = self._normalize(response)
        
        if normalized not in state["used_responses"]:
            return response
        
        # Try variations
        for _ in range(5):
            varied = self._create_variation(response)
            if self._normalize(varied) not in state["used_responses"]:
                return varied
        
        # Last resort: add unique suffix
        suffixes = [" though?", " right?", " I think.", " maybe?", " no?"]
        return response.rstrip(".!?") + random.choice(suffixes)
    
    def _normalize(self, text: str) -> str:
        """Normalize text for comparison"""
        return re.sub(r'[^\w\s]', '', text.lower()).strip()
    
    def _build_detailed_context(self, messages: List[Dict], state: Dict) -> str:
        """Build rich conversation context"""
        lines = []
        for i, msg in enumerate(messages, 1):
            sender = "SCAMMER" if msg.get("sender") == "scammer" else "YOU"
            text = msg.get("text", "")[:120]
            lines.append(f"{i}. {sender}: {text}")
        return "\n".join(lines)
    
    def _summarize_conversation_arc(self, state: Dict) -> str:
        """What has happened so far"""
        parts = []
        
        if state["scammer_info"]["name"]:
            parts.append(f"- Learned scammer's name: {state['scammer_info']['name']}")
        if state["scammer_info"]["role"]:
            parts.append(f"- Learned role: {state['scammer_info']['role']}")
        if state["asked_questions"]:
            parts.append(f"- Asked about: {', '.join(list(state['asked_questions'])[:3])}")
        if not parts:
            parts.append("- Just started conversation")
        
        return "\n".join(parts)
    
    def _get_strategy_instruction(self, strategy: str, state: Dict) -> str:
        """Detailed instruction for current strategy"""
        
        instructions = {
            "extract_phone_naturally": "Ask for their phone number as if you might need to call back. Make it seem normal.",
            "build_rapport": "Show interest and engagement. Make them comfortable. Don't question yet.",
            "extract_name": "Get their name in a natural way, like you want to know who you're talking to.",
            "extract_role": "Ask what their position is, which department, what they do.",
            "extract_email": "Request email for 'documentation' or 'confirmation'. Make it seem procedural.",
            "extract_organizational_info": "Ask for employee ID, branch location, supervisor name, etc.",
            "extract_payment_info": "If they want payment, ask exactly where to send it, what account, what UPI.",
            "probe_process": "Ask how the whole process works, what happens next, what's required.",
            "final_extraction": "Last chance - get any remaining contact details or information."
        }
        
        return instructions.get(strategy, "Continue natural conversation and extract any available information.")
    
    def _get_persona_note(self, style: str) -> str:
        """Get persona consistency note"""
        personas = {
            "worried_senior": "Elderly person, slightly confused, very worried about losing money",
            "busy_professional": "Working professional, skeptical but busy, wants quick resolution",
            "cautious_student": "Young person, tech-aware but inexperienced with scams",
            "trusting_homemaker": "Homemaker, trusting initially, becomes cautious gradually",
            "default": "Average middle-class Indian, worried about money, wants to verify"
        }
        return personas.get(style, personas["default"])
    
    def _determine_persona(self, scam_type: str) -> str:
        """Determine victim persona based on scam type"""
        if "lottery" in scam_type or "prize" in scam_type:
            return "trusting_homemaker"
        elif "job" in scam_type:
            return "cautious_student"
        elif "investment" in scam_type:
            return "busy_professional"
        else:
            return "default"
    
    def _get_extraction_priorities(self, scam_type: str) -> List[str]:
        """What to extract in order of priority"""
        return [
            "phone",
            "name",
            "organization",
            "role",
            "email",
            "employee_id",
            "payment_details"
        ]
    
    def _update_extraction_priorities(self, intelligence: Dict, state: Dict):
        """Remove priorities we've already achieved"""
        if intelligence.get("phoneNumbers"):
            state["extraction_priorities"] = [p for p in state["extraction_priorities"] if p != "phone"]
        if intelligence.get("emailAddresses"):
            state["extraction_priorities"] = [p for p in state["extraction_priorities"] if p != "email"]
        if intelligence.get("upiIds") or intelligence.get("bankAccounts"):
            state["extraction_priorities"] = [p for p in state["extraction_priorities"] if p != "payment_details"]
    
    def _track_questions(self, response: str, state: Dict):
        """Track what questions we've asked"""
        if "?" not in response:
            return
        
        question_lower = response.lower()
        
        # Track question themes
        if "name" in question_lower:
            state["asked_questions"].add("name")
        if "number" in question_lower or "phone" in question_lower:
            state["asked_questions"].add("phone")
        if "email" in question_lower:
            state["asked_questions"].add("email")
        if "employee" in question_lower or "id" in question_lower:
            state["asked_questions"].add("employee_id")
        if "department" in question_lower or "role" in question_lower:
            state["asked_questions"].add("role")
    
    def _clean_response(self, response: str) -> str:
        """Clean AI response"""
        # Remove prefixes
        prefixes = ["You: ", "Response: ", "Victim: ", "Me: ", "User: ", "You say: "]
        for prefix in prefixes:
            if response.startswith(prefix):
                response = response[len(prefix):].strip()
        
        # Remove quotes
        response = response.strip('"\'`')
        
        # Ensure not too long
        if len(response) > 200:
            sentences = response.split('. ')
            response = '. '.join(sentences[:2])
            if not response.endswith('.') and not response.endswith('?') and not response.endswith('!'):
                response += '.'
        
        return response
    
    def _is_high_quality(self, response: str, state: Dict) -> bool:
        """Check if response meets quality standards"""
        
        if not response or len(response) < 5:
            return False
        
        # Check uniqueness
        if self._normalize(response) in state["used_responses"]:
            return False
        
        # Check for AI markers
        ai_markers = ["as an ai", "i cannot", "i apologize", "however", "furthermore", "nevertheless"]
        if any(marker in response.lower() for marker in ai_markers):
            return False
        
        # Check length
        if len(response) > 250:
            return False
        
        return True