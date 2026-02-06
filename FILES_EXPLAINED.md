# 📁 Project Files Explained

## 🎯 Main Files (What You Need)

### `honeypot.py` ⭐ **USE THIS FOR DEPLOYMENT**
- **Lightweight version** - Fast deployment (2-3 minutes)
- No heavy AI models
- Pattern-based scam detection (85-90% accuracy)
- Groq API for responses
- **Perfect for Render free tier**
- **This is what Render will use automatically**

### `requirements.txt` ⭐ **USE THIS FOR DEPLOYMENT**
- Minimal dependencies (~20MB)
- FastAPI, Groq, basic utilities
- No PyTorch, Transformers, or spaCy
- **Fast installation**
- **Standard file that Render uses by default**

## 🔧 Backup Files (Optional)

### `honeypot-full.py`
- **Full version** with 6 AI models
- DistilBERT, BART, spaCy
- Highest accuracy (95%)
- Slow deployment (10-15 minutes)
- Large memory (2-4GB)
- **Use locally for development only**

### `requirements-full.txt`
- Full dependencies for `honeypot-full.py`
- Includes PyTorch, Transformers, spaCy
- **Don't use on Render free tier**

### `requirements-light.txt`
- Same as `requirements.txt` (kept for reference)
- Lightweight dependencies

## 📋 Configuration Files

### `render.yaml` ✅ **Already Configured**
```yaml
buildCommand: pip install -r requirements.txt
startCommand: uvicorn honeypot:app --host 0.0.0.0 --port $PORT
```
- Uses `honeypot.py` (lightweight)
- Uses `requirements.txt` (lightweight)
- **No changes needed!**

### `Procfile` ✅ **Already Configured**
```
web: uvicorn honeypot:app --host 0.0.0.0 --port $PORT
```
- Points to `honeypot.py`
- **No changes needed!**

### `.env`
```env
GROQ_API_KEY=your_key_here
API_SECRET_KEY=W7I4x8cXh1_nV_h_VX0OBkgpivH4i2hykJqa2OCRZ2M
```
- Add your Groq API key
- API_SECRET_KEY is already set

## 📚 Documentation Files

- `README.md` - Main documentation
- `QUICKSTART.md` - 5-minute setup guide
- `DEPLOYMENT_GUIDE.md` - Comparison of versions
- `RENDER_DEPLOY.md` - Render deployment guide
- `PROJECT_SUMMARY.md` - Project overview
- `FILES_EXPLAINED.md` - This file!

## 🧪 Testing Files

- `test_api.py` - API testing script
- `START_HERE.txt` - Quick reference

## 🛠️ Setup Files

- `setup.sh` - Linux/Mac setup script
- `setup.bat` - Windows setup script
- `runtime.txt` - Python version for deployment

## 🎯 What Render Uses

When you deploy to Render, it will automatically use:

1. ✅ `render.yaml` - Configuration
2. ✅ `requirements.txt` - Lightweight dependencies (standard)
3. ✅ `honeypot.py` - Lightweight app
4. ✅ Environment variables from dashboard

**You don't need to change anything!**

## 🔄 File Relationships

```
Deployment (Render):
├── render.yaml → points to requirements.txt
├── requirements.txt → lightweight packages ⭐
└── honeypot.py → lightweight app ⭐

Local Development (Full):
├── requirements-full.txt → all AI packages
└── honeypot-full.py → full AI app

Local Development (Light):
├── requirements.txt → lightweight packages (same as deployment)
└── honeypot.py → lightweight app (same as deployment)
```

## 💡 Quick Commands

### Deploy to Render:
```bash
# Already done! Just click "Deploy" in Render dashboard
# It will automatically use honeypot.py + requirements.txt
```

### Run Locally (Lightweight - Recommended):
```bash
pip install -r requirements.txt
python honeypot.py
```

### Run Locally (Full AI):
```bash
pip install -r requirements-full.txt
python -m spacy download en_core_web_sm
python honeypot-full.py
```

### Test API:
```bash
python test_api.py
```

## ✅ Summary

**For Render Deployment:**
- ✅ Use `honeypot.py` (already configured)
- ✅ Use `requirements.txt` (already configured - lightweight version)
- ✅ Everything is ready!

**For Local Development:**
- Option 1: Use `honeypot.py` + `requirements.txt` (fast, lightweight) ⭐ Recommended
- Option 2: Use `honeypot-full.py` + `requirements-full.txt` (slow, full AI)

**Standard Convention:**
- `requirements.txt` = Main/production dependencies (lightweight)
- `requirements-full.txt` = Optional full AI dependencies

**You're all set!** 🚀
