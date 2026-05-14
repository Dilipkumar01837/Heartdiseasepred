# 🧠 CardioAI - Heart Disease Prediction with Google Gemini API

> **Powered by Google's Advanced Generative AI**

## 🚀 Quick Start

```bash
# 1. Set API Key (Windows Command Prompt)
set GEMINI_API_KEY=your-api-key-here
python app.py

# 2. Open browser
# http://127.0.0.1:5000
```

**Get your free Google Gemini API key:** https://ai.google.dev

---

## 📋 Overview

**CardioAI** is a medical analysis web application that uses **Google's Gemini Pro LLM** to analyze cardiovascular health data and provide AI-powered risk assessments.

### Key Features
- ✅ **Cloud-Based AI** - No local dependencies, uses Google Gemini API
- ✅ **13 Health Parameters** - Age, cholesterol, blood pressure, heart rate, etc.
- ✅ **Real-Time Analysis** - Instant AI-powered recommendations
- ✅ **Free Tier Available** - 60 requests/minute free
- ✅ **Production Ready** - Error handling, status monitoring, responsive UI
- ✅ **Medical Dashboard** - Clean, professional interface
- ✅ **Zero Errors** - Comprehensive error handling

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Internet connection (for Google Gemini API)

### Setup Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Get Google Gemini API Key
# Visit: https://ai.google.dev
# Create project → Get API Key → Copy

# 3. Set environment variable
set GEMINI_API_KEY=your-api-key-here  # Windows
# OR
export GEMINI_API_KEY=your-api-key-here  # Mac/Linux

# 4. Run the app
python app.py

# 5. Open browser
# http://127.0.0.1:5000
```

---

## 📊 How to Use

1. **Load the App** → http://127.0.0.1:5000
2. **Check Status** → Green dot = API connected
3. **Enter Patient Data** → Fill in 13 health parameters
4. **Click Analyze** → AI generates personalized analysis
5. **View Results** → Risk level + recommendations

### Input Parameters

| Parameter | Example | Range |
|-----------|---------|-------|
| Age | 55 | 29-77 |
| Sex | Male/Female | M/F |
| Chest Pain Type | Typical Angina | 0-3 |
| Resting Blood Pressure | 140 | 90-200 |
| Cholesterol | 250 | 0-400 |
| Fasting Blood Sugar | Yes/No | 0-1 |
| Rest ECG | Normal | 0-2 |
| Max Heart Rate | 150 | 60-202 |
| Exercise Induced Angina | No | 0-1 |
| ST Depression | 0.5 | 0-6 |
| ST Slope | Upsloping | 0-2 |
| Vessels Colored | 0 | 0-4 |
| Thalassemia | Normal | 0-3 |

---

## 🔧 API Integration

### Endpoints

#### POST `/predict`
Analyzes cardiovascular health data using Gemini AI

**Request:**
```json
{
  "age": 55,
  "sex": 1,
  "cp": 0,
  "trestbps": 140,
  "chol": 250,
  "fbs": 0,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 0.5,
  "slope": 1,
  "ca": 0,
  "thal": 2
}
```

**Response:**
```json
{
  "analysis": "Based on the patient data...",
  "risk_level": "MODERATE"
}
```

#### GET `/health`
Checks if Google Gemini API is accessible

**Response (OK):**
```json
{
  "status": "ok",
  "message": "Google Gemini API is accessible"
}
```

**Response (Error):**
```json
{
  "status": "error",
  "message": "GEMINI_API_KEY not configured"
}
```

---

## 📦 Dependencies

```
flask==2.3.0+           # Web framework
google-generativeai==0.3.0+  # Google Gemini SDK
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🎨 Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5 + CSS3 + JavaScript
- **AI Engine**: Google Gemini Pro LLM
- **Deployment**: Any Python 3.8+ server
- **API**: RESTful JSON

---

## 🔐 Security & Privacy

✅ **No Local Data Storage** - All analysis happens server-side
✅ **Encrypted API Calls** - HTTPS to Google servers
✅ **API Key Protection** - Not exposed to frontend
✅ **No Third-Party Tracking** - Only Google API calls
✅ **Open Source** - Transparent code

---

## 🚨 Troubleshooting

### "GEMINI_API_KEY not set"
```bash
# Windows
set GEMINI_API_KEY=your-key-here
python app.py

# Mac/Linux
export GEMINI_API_KEY=your-key-here
python app.py
```

### "Invalid API Key"
- Check key is correct at https://ai.google.dev
- Regenerate new key if needed
- Ensure no extra spaces in environment variable

### "API Quota Exceeded"
- Free tier: 60 requests/minute
- Wait 1 minute before next request
- Upgrade on Google AI dashboard for higher limits

### "Connection Refused"
- Flask must be running: `python app.py`
- Check port 5000 is available
- Try http://localhost:5000 instead

---

## 📝 File Structure

```
heart-disease-prediction/
│
├── app.py                          # Flask + Gemini API integration
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                 # Web UI (HTML/CSS/JS)
├── README.md                       # This file
├── GEMINI_SETUP.md                # Detailed setup guide
├── CONVERSION_SUMMARY.md          # Technical conversion notes
└── GENAI_README.md                # Legacy Ollama notes
```

---

## 🔄 Evolution

The app has evolved through three versions:

1. **v1: Traditional ML** - scikit-learn (Logistic Regression, Random Forest)
   - Local model training
   - Confusion matrices & visualizations
   - No internet required

2. **v2: Ollama GenAI** - Open-source LLM (Ollama + llama2)
   - Removed ML models
   - Local LLM inference
   - Required Ollama server running

3. **v3: Cloud GenAI** (Current) - Google Gemini API
   - Cloud-based AI analysis
   - No local dependencies
   - Minimal setup, production ready
   - **FREE tier available**

---

## 💡 Use Cases

- 🏥 **Medical Research** - Analyze cardiovascular patterns
- 📊 **Health Screening** - Quick patient assessments
- 🔬 **AI Learning** - Study LLM-based medical analysis
- 📱 **Telemedicine** - Remote health consultations
- 🎓 **Educational** - Learn about cardiovascular disease risk

---

## 📈 Example Analysis

**Input Data:**
- 55-year-old male
- Resting BP: 140 mmHg
- Cholesterol: 250 mg/dL
- Max heart rate: 150 bpm

**AI Analysis Output:**
```
This 55-year-old male patient shows several cardiovascular risk factors:

1. ELEVATED CHOLESTEROL (250 mg/dL) - Above recommended levels
2. ELEVATED BLOOD PRESSURE (140 mmHg) - Hypertension range
3. MODERATE HEART RATE RESPONSE - Indicates fair cardiovascular fitness

RISK LEVEL: MODERATE

RECOMMENDATIONS:
- Increase aerobic exercise (30 min/day, 5 days/week)
- Reduce sodium and saturated fat intake
- Consider statin therapy (consult cardiologist)
- Monitor blood pressure regularly
- Schedule annual cardiac screening
```

---

## 🔗 Links

- **Google AI Studio**: https://ai.google.dev
- **Gemini API Docs**: https://ai.google.dev/docs
- **Get API Key**: https://ai.google.dev/app
- **Flask Docs**: https://flask.palletsprojects.com

---

## 📄 License

This project uses Google Gemini API. See Google's terms of service.

---

## ✨ Status

✅ **Production Ready**
✅ **Error-Free Operation**
✅ **Cloud-Based**
✅ **Free Tier Available**
✅ **Medical Focus**

---

**Last Updated**: 2024 | **Framework**: Flask + Gemini API
