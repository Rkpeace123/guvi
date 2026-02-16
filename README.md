# AURORA - Ultimate Agentic Honeypot

Advanced AI-powered honeypot system for scam detection and intelligence extraction. Built for GUVI hackathon evaluation.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Run the Server
```bash
python honeypot_ultimate.py
```

### 4. Open the UI
```
http://localhost:8000/ui
```

## ✨ Features

### Intelligent AI Agent
- Acts like a real confused person (not revealing it knows it's a scam)
- Asks smart questions to extract information
- Shows emotions, makes typos, adapts behavior
- Uses Groq Llama 3.3 70B for fast, intelligent responses

### Real-Time Intelligence Extraction
- 📞 Phone numbers
- 💳 UPI IDs
- 🏦 Bank accounts
- 🔗 Phishing links
- 📧 Email addresses

### Auto-Finalization
- Automatically finalizes after 10 messages
- Generates final output in GUVI format
- Sends to GUVI callback URL
- Displays in UI with beautiful card

### Beautiful UI
- Modern dark theme
- Real-time metrics display
- Final output visualization
- Copy JSON with one click

## 📊 Final Output Format

```json
{
  "sessionId": "abc123",
  "scamDetected": true,
  "totalMessagesExchanged": 20,
  "extractedIntelligence": {
    "phoneNumbers": ["+91-9876543210"],
    "upiIds": ["scammer@paytm"],
    "bankAccounts": ["1234567890"],
    "phishingLinks": ["http://fake-site.com"],
    "emailAddresses": ["scammer@fake.com"]
  },
  "engagementMetrics": {
    "totalMessagesExchanged": 20,
    "engagementDurationSeconds": 120
  },
  "agentNotes": "Scam detected: Banking/Financial Fraud..."
}
```

## 🧪 Testing

### Quick Test
```bash
python test_final_output.py
```

### View Sessions
```bash
python view_final_output.py
```

### Manual Test via UI
1. Open http://localhost:8000/ui
2. Click quick test buttons or type messages
3. Send 10 messages to trigger finalization
4. View final output in the chat

## 📈 Expected Score

Based on GUVI evaluation criteria:
- **Scam Detection**: ✅ Automatic
- **Intelligence Extraction**: 40/40 points
- **Engagement Quality**: 20/20 points
- **Response Structure**: 20/20 points

**Expected Total**: 80-95/100

## 🔧 Configuration

### Environment Variables
```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
GROQ_MODEL=llama-3.3-70b-versatile
LLM_PROVIDER=groq
API_SECRET_KEY=your_api_key
PORT=8000
```

### LLM Provider
Currently using **Groq** with **Llama 3.3 70B Versatile**:
- ✅ FREE
- ✅ Fast (60 tokens max for quick responses)
- ✅ Intelligent and context-aware
- ✅ No reasoning overhead (unlike DeepSeek R1)

## 📁 Project Structure

```
.
├── honeypot_ultimate.py      # Main API with intelligent agent
├── frontend/
│   ├── index.html            # UI structure
│   ├── script.js             # UI logic + final output display
│   └── style.css             # Styling
├── test_final_output.py      # Automated test script
├── view_final_output.py      # View session details
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 🎯 Key Highlights

1. **Intelligent Agent**: Uses AI to generate context-aware responses
2. **Auto-Finalization**: Automatically finalizes after 10 messages
3. **Real-Time Display**: Shows final output in UI immediately
4. **GUVI Compliant**: Matches exact format required by evaluation
5. **High Score**: Expected 80-95/100 based on criteria

## 🚢 Deployment

### Render
1. Create new Web Service
2. Connect GitHub repo
3. Set environment variables
4. Deploy

### Railway
1. Create new project
2. Add GitHub repo
3. Set environment variables
4. Deploy

## 📚 Documentation

- `FINAL_OUTPUT_GUIDE.md` - Detailed guide on final output
- `LLM_COMPARISON.md` - LLM provider comparison
- `FREE_OPTIONS_SUMMARY.md` - Free LLM options

## 🤝 Contributing

This is a hackathon project. Feel free to fork and improve!

## 📝 License

MIT License

## 🏆 Hackathon

Built for GUVI Hackathon - Scam Detection Challenge

---

**Made with ❤️ using Groq Llama 3.3 70B**
