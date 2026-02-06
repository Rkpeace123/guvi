# 🚀 Deployment Guide

## Deploy to Render (Recommended - FREE)

### Quick Deploy

1. **Push to GitHub** (already done ✅)
   ```bash
   git push origin main
   ```

2. **Go to Render**
   - Visit: https://render.com
   - Sign up/Login with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Rkpeace123/guvi`
   - Click "Connect"

4. **Configure Service**
   - **Name:** `agentic-honeypot` (or your choice)
   - **Region:** Oregon (US West)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command:**
     ```bash
     uvicorn honeypot:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Free

5. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable":
   
   - **GROQ_API_KEY:** `your_groq_api_key_here`
   - **API_SECRET_KEY:** `W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M`
   - **PYTHON_VERSION:** `3.11.0`

6. **Deploy!**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Your API will be live at: `https://agentic-honeypot.onrender.com`

### Using render.yaml (Automatic)

Render will automatically detect `render.yaml` and use those settings!

Just:
1. Connect your repo
2. Add GROQ_API_KEY in environment variables
3. Deploy!

---

## Deploy to Railway (Alternative - FREE)

1. **Go to Railway**
   - Visit: https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Rkpeace123/guvi`

3. **Add Environment Variables**
   - `GROQ_API_KEY`: your_groq_api_key_here
   - `API_SECRET_KEY`: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M

4. **Configure Start Command**
   - Settings → Start Command:
     ```bash
     uvicorn honeypot:app --host 0.0.0.0 --port $PORT
     ```

5. **Deploy!**
   - Railway auto-deploys on push
   - Get your URL from the dashboard

---

## Deploy to Heroku (Alternative)

1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   
   # Mac
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login & Create App**
   ```bash
   heroku login
   heroku create agentic-honeypot
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set GROQ_API_KEY=your_groq_api_key_here
   heroku config:set API_SECRET_KEY=W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

---

## Testing Your Deployed API

Once deployed, test with:

```bash
# Replace with your actual URL
export API_URL="https://agentic-honeypot.onrender.com"

curl -X POST $API_URL/api/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M" \
  -d '{
    "sessionId": "test-1",
    "message": {
      "text": "URGENT! Your account is blocked. Call 9876543210 now!"
    }
  }'
```

Expected response:
```json
{
  "status": "success",
  "reply": "What?! My account is blocked? I don't understand!"
}
```

---

## Important Notes

### Free Tier Limitations

**Render Free:**
- ✅ 750 hours/month
- ✅ Auto-sleep after 15 min inactivity
- ✅ First request after sleep takes ~30 seconds
- ✅ Perfect for hackathons!

**Railway Free:**
- ✅ $5 credit/month
- ✅ No auto-sleep
- ✅ Faster cold starts

**Heroku Free:**
- ❌ No longer offers free tier
- 💰 Requires paid plan

### Performance Tips

1. **Keep API Warm** (Render/Railway)
   - Use UptimeRobot or similar to ping every 14 minutes
   - Prevents cold starts

2. **Optimize Model Loading**
   - Models are cached after first load
   - Subsequent requests are fast

3. **Monitor Logs**
   ```bash
   # Render
   View in dashboard → Logs
   
   # Railway
   View in dashboard → Deployments → Logs
   
   # Heroku
   heroku logs --tail
   ```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | Yes | - | Get from https://console.groq.com |
| `API_SECRET_KEY` | No | W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M | Fixed API key |
| `PORT` | No | Auto | Set by platform |
| `PYTHON_VERSION` | No | 3.11.0 | Python version |

---

## Troubleshooting

### Build Fails

**Error:** `spaCy model not found`
```bash
# Add to build command:
python -m spacy download en_core_web_sm
```

**Error:** `Out of memory`
- AI models need ~2GB RAM
- Use Render (512MB free) or Railway (8GB free)
- Railway is better for AI models

### Runtime Errors

**Error:** `Module not found`
```bash
# Check requirements.txt includes all dependencies
pip freeze > requirements.txt
```

**Error:** `Port binding failed`
```bash
# Make sure start command uses $PORT
uvicorn honeypot:app --host 0.0.0.0 --port $PORT
```

### API Not Responding

1. Check logs for errors
2. Verify environment variables are set
3. Test health endpoint: `GET /health`
4. Wait for cold start (Render free tier)

---

## GUVI Hackathon Integration

Your deployed API will automatically:
1. ✅ Accept requests from GUVI testing system
2. ✅ Detect scams using 6 AI models
3. ✅ Extract intelligence
4. ✅ Send reports to GUVI callback URL
5. ✅ Use fixed API key: `W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M`

**Submit this URL to GUVI:**
```
https://your-app-name.onrender.com
```

**API Key for GUVI:**
```
W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
```

---

## Quick Commands

```bash
# Check deployment status
curl https://your-app.onrender.com/health

# View API docs
open https://your-app.onrender.com/docs

# Test scam detection
curl -X POST https://your-app.onrender.com/api/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M" \
  -d '{"message": {"text": "URGENT! Account blocked!"}}'
```

---

## Success Checklist

- [ ] Repository pushed to GitHub
- [ ] Render/Railway account created
- [ ] Web service created and connected
- [ ] Environment variables set (GROQ_API_KEY)
- [ ] Build completed successfully
- [ ] API responding to health checks
- [ ] Scam detection working
- [ ] URL submitted to GUVI

🎉 You're deployed and ready for the hackathon!
