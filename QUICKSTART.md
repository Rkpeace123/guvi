# 🚀 Quick Start Guide

Get your Ultimate Agentic Honeypot running in 5 minutes!

## Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Step 2: Get Your FREE Groq API Key (1 minute)

1. Go to https://console.groq.com
2. Sign up (it's FREE!)
3. Click "Create API Key"
4. Copy your key

## Step 3: Configure .env File (30 seconds)

Open `.env` and paste your Groq API key:

```env
GROQ_API_KEY=gsk_your_key_here
API_SECRET_KEY=W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
```

(API_SECRET_KEY is already set to: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M)

## Step 4: Run! (30 seconds)

```bash
python honeypot.py
```

You'll see:
```
🔄 Loading AI models...
✅ All AI models loaded successfully!
✅ Multi-Model Scam Detector initialized!
✅ Intelligence Extractor initialized!
✅ Human-like Response Generator initialized!
🚀 Using Groq Llama 3.3 70B

🧪 Testing with scam message...
✅ DETECTION RESULTS:
   Scam: True
   Confidence: 85.50%
   
🚀 Starting Agentic Honey-Pot API...
📝 API Documentation: http://localhost:8000/docs
```

## Step 5: Test It! (1 minute)

Open another terminal and test:

```bash
# Get the fixed API key
export API_KEY="W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M"

# Test the API
curl -X POST http://localhost:8000/api/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{
    "sessionId": "test-1",
    "message": {
      "text": "URGENT! Your account is blocked. Call 9876543210 now!"
    }
  }'
```

You should get a response like:
```json
{
  "status": "success",
  "reply": "What?! My account is blocked? I don't understand!"
}
```

## 🎉 That's It!

Your honeypot is now:
- ✅ Detecting scams with 6 AI models
- ✅ Extracting intelligence (phones, UPI, links)
- ✅ Generating human-like responses
- ✅ Ready for the GUVI hackathon!

## Next Steps

- Visit http://localhost:8000/docs for interactive API documentation
- Check the logs to see scam detection in action
- Deploy with ngrok for public access (see README.md)

## Troubleshooting

**Models taking too long to load?**
- First run downloads ~2GB of AI models
- Subsequent runs are much faster (models are cached)

**No GPU warning?**
- That's fine! CPU works great, just a bit slower
- Models will automatically use CPU

**Groq API errors?**
- Check your API key in .env
- System will use fallback responses if API fails

**Need help?**
- Check README.md for detailed documentation
- All features work without Groq (uses fallback mode)
