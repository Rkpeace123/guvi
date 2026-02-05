#!/bin/bash

echo "🍯 Setting up Ultimate Agentic Honeypot..."
echo ""

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Download spaCy model
echo "📥 Downloading spaCy language model..."
python -m spacy download en_core_web_sm

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file and add your API keys:"
echo "   - GROQ_API_KEY (get from: https://console.groq.com)"
echo "   - NGROK_AUTH_TOKEN (optional, for public deployment)"
echo ""
echo "2. Run the honeypot:"
echo "   python honeypot.py"
echo ""
