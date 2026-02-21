# AURORA - System Architecture

## Overview
AURORA is an AI-powered honeypot system designed to detect, engage, and extract intelligence from scam conversations.

## System Components

### 1. Core API (`main.py`)
- **FastAPI** web server handling incoming scam messages
- Session management for conversation tracking
- Orchestrates all detection and response systems
- Auto-finalizes sessions after 10 messages

### 2. Scam Detection (`AdvancedScamDetector`)
- **Keyword-based scoring**: 30+ scam keywords with weighted importance
- **Pattern detection**: Identifies urgency + threat + action combinations
- **Scam type classification**: 10+ fraud categories
- **Confidence scoring**: 0-100% confidence level
- **Threshold**: 0.35 (35%) for scam flagging

### 3. Intelligence Extraction (`enhanced_extractor.py`)
- **Phone numbers**: Validates Indian numbers (+91), handles multiple formats
- **UPI IDs**: Extracts payment identifiers (paytm, phonepe, gpay, etc.)
- **Bank accounts**: 9-18 digit account numbers with validation
- **Phishing links**: HTTP/HTTPS URLs, shortened links (bit.ly, tinyurl)
- **Email addresses**: RFC 5322 compliant extraction
- **Context-aware**: Uses conversation history for better extraction

### 4. Red Flag Detection (`red_flag_detector.py`)
- **10 Red Flag Categories**:
  - Urgency pressure (HIGH)
  - Threat/intimidation (HIGH)
  - Credential requests (CRITICAL)
  - Money requests (CRITICAL)
  - Suspicious links (HIGH)
  - Authority impersonation (HIGH)
  - Too-good-to-be-true offers (MEDIUM)
  - Information harvesting (MEDIUM)
  - No verification offered (HIGH)
  - Grammar/spelling errors (LOW)
- **Conversation pattern analysis**: Detects escalating pressure, persistent harvesting
- **Risk scoring**: CRITICAL, HIGH, MEDIUM, LOW levels

### 5. Response Generation (`enhanced_response.py`)
- **3-Tier Fallback System**:
  - Tier 1: Groq Llama 3.3 70B (AI-powered, best quality)
  - Tier 2: Enhanced pattern-based (high quality)
  - Tier 3: Emergency fallback (always works)
- **Scam-type aware**: Responses match the fraud type
  - Lottery: Acts excited, asks about prize
  - Bank fraud: Acts worried, asks for verification
  - Job scam: Acts interested, asks about salary
- **Stage-based strategies**: Early (worried) → Middle (questioning) → Late (suspicious)
- **Quality scoring**: Ensures natural, human-like responses

## Data Flow

```
Incoming Message
    ↓
Session Management (create/retrieve)
    ↓
Scam Detection → Confidence Score + Type
    ↓
Red Flag Detection → Risk Level + Flags
    ↓
Intelligence Extraction → Phone/UPI/Bank/Links/Emails
    ↓
Response Generation (AI/Pattern/Fallback)
    ↓
Session Update + Logging
    ↓
Auto-Finalize (after 10 messages)
    ↓
Send to GUVI Callback
```

## API Endpoints

### POST `/api/message`
- **Purpose**: Handle incoming scam messages
- **Auth**: X-API-Key header required
- **Input**: sessionId, message, conversationHistory, metadata
- **Output**: status, reply

### GET `/api/session/{session_id}`
- **Purpose**: Retrieve session details and final output
- **Auth**: X-API-Key header required
- **Output**: session data, finalOutput

### GET `/api/sessions`
- **Purpose**: List all active sessions
- **Auth**: X-API-Key header required
- **Output**: session summaries

### GET `/health`
- **Purpose**: Health check
- **Output**: status, active_sessions, ai_enabled

### GET `/ui`
- **Purpose**: Serve frontend UI
- **Output**: HTML interface

## Final Output Format

```json
{
  "status": "success",
  "sessionId": "abc123",
  "scamDetected": true,
  "scamType": "Banking/Financial Fraud",
  "confidenceLevel": 0.85,
  "redFlags": [
    {
      "flag": "credential_request",
      "severity": "CRITICAL",
      "description": "Requests sensitive credentials"
    }
  ],
  "totalMessagesExchanged": 10,
  "extractedIntelligence": {
    "phoneNumbers": ["+919876543210"],
    "upiIds": ["scammer@paytm"],
    "bankAccounts": ["1234567890123456"],
    "phishingLinks": ["http://fake-site.com"],
    "emailAddresses": ["scammer@fake.com"]
  },
  "engagementMetrics": {
    "totalMessagesExchanged": 10,
    "engagementDurationSeconds": 120
  },
  "agentNotes": "Scam detected: Banking/Financial Fraud with 85.0% confidence..."
}
```

## Error Handling

- **API key validation**: 401 Unauthorized if missing/invalid
- **Session not found**: 404 Not Found
- **AI fallback**: Graceful degradation to pattern-based responses
- **Extraction errors**: Continues with partial results
- **Logging**: All errors logged with context

## Performance

- **Response time**: < 2 seconds per message
- **AI latency**: ~500ms (Groq Llama 3.3 70B)
- **Fallback latency**: < 50ms (pattern-based)
- **Memory**: ~50MB per session
- **Concurrent sessions**: Unlimited (stateless design)

## Security

- **API key authentication**: All endpoints protected
- **Input sanitization**: Prevents injection attacks
- **Session isolation**: No cross-session data leakage
- **Rate limiting**: Recommended for production
- **HTTPS**: Required for production deployment

## Deployment

- **Platform**: Render, Railway, Fly.io compatible
- **Runtime**: Python 3.11+
- **Dependencies**: 7 core packages (~50MB)
- **Environment variables**: GROQ_API_KEY, API_SECRET_KEY
- **Port**: Configurable (default 8000)

## Monitoring

- **Logging**: INFO level for all operations
- **Metrics tracked**:
  - Scam detection rate
  - Intelligence extraction count
  - Red flag frequency
  - Response generation tier usage
  - Session duration

## Future Enhancements

- Multi-language support (Hindi, Tamil, etc.)
- Image/QR code analysis
- Voice call integration
- Graph-based scammer network analysis
- Reinforcement learning for response optimization
