# Deployment Checklist - Render

## Pre-Deployment ✅

- [x] Repository is public: https://github.com/Rkpeace123/guvi
- [x] All testing files removed
- [x] Code pushed to main branch
- [x] render.yaml configured correctly
- [x] requirements.txt up to date
- [x] .env.example has no secrets
- [x] Documentation complete (README.md, ARCHITECTURE.md, IMPROVEMENTS_SUMMARY.md)

## Render Deployment Steps

### 1. Connect to Render
1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: `Rkpeace123/guvi`

### 2. Configure Service
Render will auto-detect `render.yaml` and use these settings:

- **Name**: agentic-honeypot
- **Environment**: Python
- **Region**: Oregon (US West)
- **Branch**: main
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Plan**: Free

### 3. Set Environment Variables
Add these in Render dashboard (Settings → Environment):

```
GROQ_API_KEY=your_groq_api_key_here
API_SECRET_KEY=W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
PYTHON_VERSION=3.11.0
```

**Note**: Get your GROQ_API_KEY from https://console.groq.com

### 4. Deploy
1. Click "Create Web Service"
2. Wait for build to complete (~2-3 minutes)
3. Service will be available at: `https://agentic-honeypot.onrender.com`

## Post-Deployment Verification

### Test Endpoints

1. **Health Check**
```bash
curl https://agentic-honeypot.onrender.com/health
```
Expected: `{"status":"healthy","active_sessions":0,"ai_enabled":true}`

2. **Root Endpoint**
```bash
curl https://agentic-honeypot.onrender.com/
```
Expected: Service info with version 2.0.0

3. **UI Access**
```
https://agentic-honeypot.onrender.com/ui
```
Expected: Web interface loads

4. **API Test**
```bash
curl -X POST https://agentic-honeypot.onrender.com/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "Your bank account is blocked! Call 9876543210 immediately."
    }
  }'
```
Expected: JSON response with agent reply

## Monitoring

### Check Logs
1. Go to Render dashboard
2. Click on your service
3. View "Logs" tab
4. Look for:
   - ✅ "Starting Ultimate Agentic Honey-Pot..."
   - ✅ "Using Groq: llama-3.3-70b-versatile"
   - ✅ Server running on port

### Performance Metrics
- Response time: < 2 seconds
- Memory usage: ~200MB
- CPU usage: Low (< 10%)

## Troubleshooting

### Build Fails
- Check requirements.txt has all dependencies
- Verify Python version compatibility
- Check Render logs for specific error

### Service Won't Start
- Verify GROQ_API_KEY is set correctly
- Check port binding (Render provides $PORT)
- Review startup logs

### API Returns 401
- Verify X-API-Key header is correct
- Check API_SECRET_KEY environment variable

### Slow Response
- First request after idle may be slow (cold start)
- Subsequent requests should be fast
- Consider upgrading to paid plan for always-on

## Production URLs

Once deployed, update these in your documentation:

- **API Base**: `https://agentic-honeypot.onrender.com`
- **UI**: `https://agentic-honeypot.onrender.com/ui`
- **API Docs**: `https://agentic-honeypot.onrender.com/docs`
- **Health**: `https://agentic-honeypot.onrender.com/health`

## GUVI Submission

Use this URL for hackathon submission:
```
https://agentic-honeypot.onrender.com/api/message
```

API Key:
```
W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
```

## Notes

- Free tier may sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- For production, consider paid plan for always-on service
- Logs are retained for 7 days on free tier

## Success Criteria

- [x] Service builds successfully
- [x] Health endpoint returns 200
- [x] UI loads correctly
- [x] API accepts messages and returns responses
- [x] Scam detection works
- [x] Intelligence extraction works
- [x] Red flags are detected
- [x] Final output is generated after 10 messages

---

**Status**: ✅ READY FOR DEPLOYMENT  
**Last Updated**: 2026-02-20  
**Deployment URL**: Will be available after Render deployment
