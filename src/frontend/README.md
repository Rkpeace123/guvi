# 🛡️ AURORA Frontend

**Adaptive Unified Risk-Oriented Response Architecture**

## Overview

AURORA is a modern, real-time chat interface for testing the advanced honeypot system. It provides an intuitive way to simulate scammer conversations and observe the system's detection capabilities in action.

## Features

### 🎨 Modern UI
- Dark theme with gradient accents
- Smooth animations and transitions
- Responsive design for all devices
- Real-time updates

### 📊 Live Metrics
- **TRAA Risk Score** - Multi-signal risk aggregation
- **Confidence Level** - Detection confidence
- **FSM State** - Current conversation state
- **Extracted Intelligence** - Phone numbers, UPI IDs, bank accounts, links

### 💬 Chat Interface
- Real-time message exchange
- Typing indicators
- Message timestamps
- Quick test buttons for common scam scenarios

### 📈 Session Management
- Unique session tracking
- Message count
- Risk score visualization
- Export session data as JSON

## Quick Start

### 1. Start the Backend

```bash
# Make sure you're in the project root
python honeypot_advanced_integrated.py
```

The backend will start on `http://localhost:8000`

### 2. Open the Frontend

Simply open `frontend/index.html` in your web browser:

```bash
# On Windows
start frontend/index.html

# On Mac
open frontend/index.html

# On Linux
xdg-open frontend/index.html
```

Or use a local server:

```bash
# Python 3
cd frontend
python -m http.server 8080

# Then open http://localhost:8080
```

### 3. Test the System

Click one of the quick test buttons or type your own message:

- **🚨 Urgent Scam** - Tests high-urgency scam detection
- **🎉 Prize Scam** - Tests reward/lottery scam detection
- **👋 Normal Message** - Tests false positive handling

## Interface Components

### Header
- **AURORA Logo** - Animated pulse effect
- **System Status** - Real-time connection indicator
  - 🟢 Online - System operational
  - 🟡 Connecting - Establishing connection
  - 🔴 Offline - System unavailable

### Sidebar (Left)

#### Session Info
- Session ID (truncated)
- Message count
- Current risk score with color coding:
  - 🟢 Green: Low risk (< 0.4)
  - 🟡 Yellow: Medium risk (0.4 - 0.65)
  - 🔴 Red: High risk (> 0.65)

#### Detection Metrics
- **TRAA Score** - Visual bar + numeric value
- **Confidence** - Visual bar + numeric value
- **FSM State** - Current conversation state badge

#### Extracted Intelligence
- 📞 Phone Numbers
- 💳 UPI IDs
- 🏦 Bank Accounts
- 🔗 Phishing Links

#### Actions
- **New Session** - Start fresh conversation
- **Export Data** - Download session as JSON

### Chat Area (Center)

#### Welcome Screen
- System introduction
- Quick test buttons
- Usage instructions

#### Message Display
- 🎭 Scammer messages (left, gray)
- 🛡️ AURORA responses (right, gradient)
- Message timestamps
- Inline metrics for each response

#### Input Area
- Multi-line text input
- Auto-resize textarea
- Send button (gradient)
- Keyboard shortcuts:
  - `Enter` - Send message
  - `Shift + Enter` - New line

## API Integration

The frontend communicates with the backend via REST API:

### Endpoint: POST /api/message

**Request:**
```json
{
  "sessionId": "aurora-1234567890-abc123",
  "message": {
    "sender": "scammer",
    "text": "Your account is blocked!",
    "timestamp": "2026-02-13T10:30:00Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "Web",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "What?! Why is my account blocked?",
  "advanced_metrics": {
    "traa": {
      "risk_score": 0.85,
      "confidence": 0.92,
      "breakdown": {...}
    },
    "fsm": {
      "state": "confused",
      "message_count": 1
    },
    "dlaa": {
      "style_profile": {...}
    },
    "entities": {
      "extracted": 0,
      "total": 0
    }
  }
}
```

### Endpoint: GET /api/session/{sessionId}

Retrieves complete session data including all messages and extracted intelligence.

### Endpoint: GET /health

Checks system health and availability.

## Customization

### Colors

Edit `style.css` to change the color scheme:

```css
:root {
    --primary: #667eea;        /* Primary gradient start */
    --secondary: #764ba2;      /* Primary gradient end */
    --success: #10b981;        /* Success/low risk */
    --warning: #f59e0b;        /* Warning/medium risk */
    --danger: #ef4444;         /* Danger/high risk */
    --bg-primary: #0f172a;     /* Main background */
    --bg-secondary: #1e293b;   /* Card background */
    --bg-tertiary: #334155;    /* Input background */
}
```

### API Configuration

Edit `script.js` to change API settings:

```javascript
this.apiUrl = 'http://localhost:8000';  // Backend URL
this.apiKey = 'your-api-key-here';      // API key
```

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Features in Detail

### Real-Time Risk Scoring

Watch the risk score update in real-time as the conversation progresses:
- Visual progress bars
- Color-coded indicators
- Numeric values with 2 decimal precision

### FSM State Tracking

Observe the Finite State Machine transitions:
- **Confused** (Messages 1-2) - Initial confusion
- **Curious** (Messages 3-5) - Asking questions
- **Engaged** (Messages 6-8) - Providing information
- **Skeptical** (Messages 9+) - Expressing doubts

### Intelligence Extraction

See extracted entities appear in real-time:
- Automatic detection of sensitive information
- Confidence scoring
- Categorized display

### Session Export

Export complete session data for analysis:
- All messages with timestamps
- Risk scores and metrics
- Extracted intelligence
- FSM state history
- JSON format for easy processing

## Troubleshooting

### "Connection Failed" Error

1. Ensure backend is running: `python honeypot_advanced_integrated.py`
2. Check backend is on port 8000
3. Verify API key matches in both frontend and backend

### Messages Not Sending

1. Check browser console for errors (F12)
2. Verify network connectivity
3. Ensure CORS is enabled on backend

### Metrics Not Updating

1. Check API response in Network tab (F12)
2. Verify session ID is consistent
3. Refresh page and try again

## Development

### File Structure

```
frontend/
├── index.html      # Main HTML structure
├── style.css       # Styling and animations
├── script.js       # JavaScript logic
└── README.md       # This file
```

### Adding Features

1. **New Metric Display**
   - Add HTML in `index.html` sidebar
   - Add CSS styling in `style.css`
   - Update `updateMetrics()` in `script.js`

2. **New Quick Test**
   - Add button in welcome message HTML
   - Set `data-message` attribute
   - Event listener auto-attached

3. **Custom Animations**
   - Define keyframes in `style.css`
   - Apply to elements with `animation` property

## Performance

- Lightweight: ~50KB total (HTML + CSS + JS)
- No external dependencies
- Optimized animations
- Efficient DOM updates
- Smooth 60fps scrolling

## Security

- API key required for all requests
- Input sanitization (HTML escaping)
- No sensitive data stored in browser
- Session data only in memory

## Future Enhancements

- [ ] Dark/Light theme toggle
- [ ] Multiple language support
- [ ] Voice input
- [ ] Graph visualization of scam networks
- [ ] Historical session browser
- [ ] Real-time collaboration
- [ ] Mobile app version

## Credits

Built for GUVI Hackathon 2026

**AURORA** - Adaptive Unified Risk-Oriented Response Architecture

---

For backend documentation, see `README_ADVANCED.md` in the project root.
