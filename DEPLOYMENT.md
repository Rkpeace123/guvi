# Deployment Guide

## GitHub Repository
✅ **Successfully deployed to GitHub!**

Repository: https://github.com/Rkpeace123/guvi

## Deploy to Render (Recommended)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Rkpeace123/guvi`
3. Configure the service:

**Basic Settings:**
- Name: `guvi-honeypot` (or any name you prefer)
- Region: Choose closest to you
- Branch: `main`
- Root Directory: Leave empty
- Runtime: `Python 3`

**Build & Deploy:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `python honeypot_ultimate.py`

**Instance Type:**
- Free tier is sufficient for testing
- Upgrade to paid if you need more resources

### Step 3: Environment Variables
Add these environment variables in Render dashboard:

```
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_PROVIDER=groq
API_SECRET_KEY=W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
PORT=8000
```

**Important:** Replace `your_actual_groq_api_key_here` with your real Groq API key from https://console.groq.com

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-3 minutes)
3. Your app will be live at: `https://guvi-honeypot.onrender.com`

### Step 5: Test Deployment
```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test API endpoint
curl -X POST https://your-app.onrender.com/api/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M" \
  -d '{
    "sessionId": "test-123",
    "message": {
      "sender": "scammer",
      "text": "URGENT! Your account has been blocked. Call 9876543210"
    }
  }'
```

### Step 6: Submit to GUVI
Once deployed, submit these details on GUVI platform:

1. **Deployment URL**: `https://your-app.onrender.com/api/message`
2. **API Key**: `W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M`
3. **GitHub URL**: `https://github.com/Rkpeace123/guvi`

## Alternative: Deploy to Railway

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project" → "Deploy from GitHub repo"
2. Select `Rkpeace123/guvi`
3. Add environment variables (same as Render)
4. Deploy!

## Alternative: Deploy to Fly.io

### Step 1: Install Fly CLI
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Deploy
```bash
fly auth login
fly launch
fly secrets set GROQ_API_KEY=your_key_here
fly deploy
```

## Troubleshooting

### Issue: App crashes on startup
**Solution**: Check environment variables are set correctly

### Issue: API returns 401 Unauthorized
**Solution**: Verify API key in request header matches `API_SECRET_KEY`

### Issue: Slow responses
**Solution**: 
- Check Groq API key is valid
- Verify `max_tokens=60` in code (for fast responses)
- Consider upgrading to paid tier

### Issue: Final output not showing
**Solution**: 
- Ensure 10 messages are sent
- Check browser console for errors
- Click "View Final Output" button manually

## Monitoring

### Check Logs
**Render**: Dashboard → Logs tab
**Railway**: Dashboard → Deployments → View Logs
**Fly.io**: `fly logs`

### Check Health
```bash
curl https://your-app.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "active_sessions": 0,
  "ai_enabled": true
}
```

## Performance Tips

1. **Use Groq** (not DeepSeek R1) - much faster
2. **Keep max_tokens=60** - faster responses
3. **Monitor API usage** - Groq has rate limits
4. **Use caching** - if implementing advanced features

## Security Notes

1. ✅ API key is required for all endpoints
2. ✅ CORS is enabled for frontend
3. ✅ Environment variables are secure
4. ⚠️ Don't commit `.env` file to GitHub
5. ⚠️ Rotate API keys periodically

## Support

- **GitHub Issues**: https://github.com/Rkpeace123/guvi/issues
- **Render Docs**: https://render.com/docs
- **Groq Docs**: https://console.groq.com/docs

## Next Steps

1. ✅ Deploy to Render/Railway
2. ✅ Test with GUVI evaluation scenarios
3. ✅ Submit to GUVI platform
4. ✅ Monitor performance
5. ✅ Win the hackathon! 🏆
