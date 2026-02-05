# 🍯 Ultimate Agentic Honeypot

Multi-Model AI System for Scam Detection & Intelligence Extraction

## Features

- ✅ **Multi-Model Scam Detection** (6 AI models)
  - DistilBERT for sentiment analysis
  - BART for zero-shot classification
  - spaCy for entity recognition
  - Pattern matching & keyword detection
  
- ✅ **Human-like Responses** (Groq Llama 3.3 70B)
  - Context-aware conversation
  - Stage-based responses (early/middle/late)
  - Fallback mode if API unavailable

- ✅ **Intelligence Extraction**
  - Phone numbers (Indian format)
  - UPI IDs
  - Bank account numbers
  - Phishing links
  - Suspicious keywords

- ✅ **Production Ready**
  - FastAPI REST API
  - Session management
  - GUVI hackathon integration
  - API key authentication

## Quick Start

### 1. Install Dependencies

```bash
# On Linux/Mac
chmod +x setup.sh
./setup.sh

# On Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Configure API Keys

Edit `.env` file:

```env
# Get FREE Groq API key from: https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here

# Optional: Auto-generated if empty
API_SECRET_KEY=your_api_secret_key_here

# Optional: For ngrok deployment
NGROK_AUTH_TOKEN=your_ngrok_token_here
```

### 3. Run the Honeypot

```bash
python honeypot.py
```

The API will start on `http://localhost:8000`

## API Usage

### Endpoints

- `GET /` - Status check
- `GET /health` - Health check
- `POST /api/message` - Main scam detection endpoint
- `GET /api/sessions` - List all sessions
- `GET /api/session/{session_id}` - Get session details

### Example Request

```bash
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M" \
  -d '{
    "sessionId": "test-session-1",
    "message": {
      "sender": "scammer",
      "text": "URGENT! Your account is blocked. Call 9876543210 now!"
    }
  }'
```

### Example Response

```json
{
  "status": "success",
  "reply": "What?! My account is blocked? I don't understand!"
}
```

## How It Works

1. **Scam Detection**: Incoming messages are analyzed using 4 methods:
   - Keyword matching (fast)
   - Sentiment analysis (AI)
   - Zero-shot classification (AI)
   - Pattern analysis (urgency + threat + action)

2. **Intelligence Extraction**: Extracts scammer information:
   - Phone numbers, UPI IDs, bank accounts, phishing links

3. **Human-like Response**: Generates contextual responses:
   - Early stage: Shows concern and confusion
   - Middle stage: Asks for verification details
   - Late stage: Shows skepticism

4. **Reporting**: Automatically sends intelligence to GUVI callback URL when:
   - 6+ messages exchanged with extracted intelligence
   - OR 12+ messages exchanged

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Incoming Message                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Multi-Model Scam Detector                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ Keywords │ │Sentiment │ │Zero-Shot │ │ Patterns │  │
│  │ Matching │ │ Analysis │ │  Class.  │ │ Analysis │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          Intelligence Extractor                          │
│  📱 Phones  💳 UPI  🏦 Bank Accounts  🔗 Links          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│       Response Generator (Groq Llama 3.3 70B)           │
│  Context-aware, stage-based human-like responses         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Response + Intelligence Report              │
└─────────────────────────────────────────────────────────┘
```

## Requirements

- Python 3.8+
- 4GB+ RAM (for AI models)
- GPU optional (faster inference)

## API Keys

### Groq API (Required for AI responses)
1. Visit https://console.groq.com
2. Sign up for free account
3. Generate API key
4. Add to `.env` file

### ngrok (Optional, for public deployment)
1. Visit https://dashboard.ngrok.com
2. Sign up for free account
3. Get auth token
4. Add to `.env` file

## Testing

The system includes built-in tests that run on startup:

```python
python honeypot.py
```

You'll see test results for:
- Scam detection (confidence scores)
- Intelligence extraction
- Response generation

## Deployment

### Local Development
```bash
python honeypot.py
```

### Production (with ngrok)
```bash
# Set NGROK_AUTH_TOKEN in .env
python deploy.py
```

### Docker (coming soon)
```bash
docker build -t honeypot .
docker run -p 8000:8000 --env-file .env honeypot
```

## License

MIT License - Feel free to use for hackathons and learning!

## Credits

Built for GUVI Hackathon 2026
