# 🧠 CardioAI - Google Gemini API Setup Guide

## Quick Setup (5 minutes)

### Step 1: Get Your Google Gemini API Key
1. Go to: **https://ai.google.dev**
2. Click **"Get API Key"**
3. Create a new API key (free tier available)
4. Copy your API key

### Step 2: Set Environment Variable

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
python app.py
```

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python app.py
```

**Mac/Linux (Terminal):**
```bash
export GEMINI_API_KEY=your-api-key-here
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://127.0.0.1:5000**

---

## Features

✅ **Google Gemini API** - Advanced LLM for medical analysis
✅ **Cloud-Based** - No local setup required
✅ **Free Tier** - Up to 60 requests/minute free
✅ **Error Handling** - Graceful errors with setup instructions
✅ **Real-Time Status** - See connection status on UI
✅ **Production Ready** - Ready for deployment

---

## How It Works

1. **Enter Patient Data** - 13 health parameters
2. **Send to Gemini** - AI analyzes in cloud
3. **Get Analysis** - Medical insights & recommendations
4. **View Results** - Risk level + personalized advice

---

## API Information

- **Provider**: Google AI (Generative AI)
- **Model**: `gemini-pro`
- **API Endpoint**: https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
- **Response Time**: 1-3 seconds
- **Free Quota**: 60 requests/minute

---

## Troubleshooting

### Error: "GEMINI_API_KEY environment variable not set"
**Solution**: Set your API key as shown in Step 2 above

### Error: "API Error: Invalid API Key"
**Solution**: Check that your API key is correct at https://ai.google.dev

### Error: "Quota exceeded"
**Solution**: Wait a minute or upgrade to paid tier (if using free tier)

### App shows "Checking..." status
**Solution**: Wait 5 seconds for API check to complete

---

## Environment Setup

### Persistent Setup (Optional)

**Windows (Set Permanently):**
1. Open Environment Variables (Windows + Pause/Break)
2. Click "Environment Variables"
3. Add new User variable:
   - Name: `GEMINI_API_KEY`
   - Value: `your-api-key-here`
4. Restart terminal/app

**Mac/Linux (Add to .bashrc or .zshrc):**
```bash
echo 'export GEMINI_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

---

## File Structure

```
heart-disease-prediction/
├── app.py                 # Flask + Gemini API
├── requirements.txt       # Dependencies
├── templates/
│   └── index.html        # Web UI
└── GEMINI_SETUP.md       # This file
```

---

## Dependencies

```
flask==2.3.0+
google-generativeai==0.3.0+
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Security Notes

✅ API key is NOT sent to browser
✅ All requests server-side authenticated
✅ Patient data sent to Google only for analysis
✅ No data storage by default
✅ API key should be kept secret

---

## Next Steps

1. ✅ Get API key from Google AI
2. ✅ Set GEMINI_API_KEY environment variable
3. ✅ Run the app: `python app.py`
4. ✅ Open browser: http://127.0.0.1:5000
5. ✅ Enter patient data and analyze

**Support**: Check Google AI documentation at https://ai.google.dev/docs

---

**Version**: 1.0 | **Date**: May 14, 2026
