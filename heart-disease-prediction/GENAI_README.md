# 🧠 CardioAI - Generative AI Heart Disease Predictor

A modern web application for cardiovascular risk assessment powered by **Generative AI (LLM)** instead of traditional ML models.

## ✨ What Changed

### Previous Version (ML-based)
- ❌ Logistic Regression model
- ❌ Random Forest classifier  
- ❌ Confusion matrices
- ❌ Feature importance charts
- ❌ Static accuracy metrics

### New Version (GenAI-based)
- ✅ Ollama LLM integration (open-source)
- ✅ Natural language medical analysis
- ✅ Contextual cardiovascular risk assessment
- ✅ Personalized recommendations
- ✅ No ML training required
- ✅ Real-time LLM inference

---

## 🚀 Getting Started

### Prerequisites
1. **Install Ollama** (open-source LLM runner)
   - Download: https://ollama.ai
   - Supports: macOS, Linux, Windows (WSL2)

2. **Pull a Language Model**
   ```bash
   ollama pull llama2
   ```
   Other options: `mistral`, `neural-chat`, `orca-mini`, etc.

3. **Start Ollama Server**
   ```bash
   ollama serve
   ```
   Server runs on: `http://localhost:11434` (default)

### Setup & Run
```bash
# Navigate to project
cd c:\Users\Deepikaa\Downloads\gen3\Heartdiseasepred\heart-disease-prediction

# Install dependencies
pip install -r requirements.txt

# Start Flask app
python app.py

# Open in browser
http://127.0.0.1:5000
```

---

## 📋 How It Works

### Patient Input
Enter 13 cardiovascular health parameters:
- Age, Sex
- Chest pain type
- Blood pressure, Cholesterol
- Blood sugar, ECG results
- Heart rate, Exercise tolerance
- ST depression, Slope, Vessels, Thalassemia

### GenAI Analysis
The LLM analyzes all factors together and provides:
- **Risk Level**: HIGH / MODERATE / LOW
- **Key Risk Factors**: Identified cardiovascular concerns
- **Personalized Recommendations**: Medical advice
- **Confidence Level**: LLM confidence in assessment

### Real-time Status
- ✅ Shows if GenAI model is connected
- ⚠️ Alerts if Ollama is offline
- 📊 Live analysis results

---

## 🔧 Configuration

### Custom Ollama Server
```bash
# Set environment variables
export OLLAMA_URL=http://your-server:11434
export OLLAMA_MODEL=mistral
python app.py
```

### Try Different Models
```bash
ollama pull mistral      # Faster, smaller
ollama pull neural-chat  # Medical-optimized
ollama pull llama2       # Balanced
ollama pull orca-mini    # Lightweight
```

---

## 📁 Project Structure

```
heart-disease-prediction/
├── app.py              # Flask backend + GenAI integration
├── requirements.txt    # Dependencies (minimal)
├── templates/
│   └── index.html     # Modern dark UI
└── README.md          # This file
```

### Key Changes from ML Version
```
REMOVED:
- sklearn imports
- Model training code
- Dataset generation
- Confusion matrices
- Feature importance visualization
- Static metrics calculation

ADDED:
- requests library (API calls)
- Ollama integration
- LLM prompt engineering
- Health check endpoint
- Real-time connection status
```

---

## 🎯 API Endpoints

### GET `/`
- Serves the web UI

### POST `/predict`
**Request:**
```json
{
  "age": 55,
  "sex": 1,
  "cp": 0,
  "trestbps": 130,
  "chol": 250,
  "fbs": 0,
  "restecg": 0,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.0,
  "slope": 0,
  "ca": 0,
  "thal": 0
}
```

**Response:**
```json
{
  "analysis": "Detailed LLM analysis...",
  "risk_level": "MODERATE",
  "model": "GenAI (Ollama)",
  "status": "success"
}
```

### GET `/health`
- Checks Ollama server connection
- Returns available models
- Status: `ok` or `error`

---

## 🎨 UI Features

### Modern Design
- Dark medical dashboard theme
- Responsive grid layout
- Smooth animations
- Real-time status indicator
- Animated EKG heartbeat line

### User Experience
- Clear form validation
- Loading spinner during analysis
- Color-coded risk levels (🟢 Low, 🟡 Moderate, 🔴 High)
- Formatted LLM response display
- One-click Clear button

---

## ⚠️ Troubleshooting

### "GenAI Model: Disconnected"
```bash
# Make sure Ollama is running
ollama serve

# Check if port 11434 is accessible
curl http://localhost:11434/api/tags
```

### Slow Analysis
- Ollama first run: Downloads model (~4GB for llama2)
- Try lighter model: `ollama pull orca-mini`
- Increase timeout in `app.py` (line: timeout=30)

### Model Not Found
```bash
# List available models
ollama list

# Pull a model
ollama pull llama2
```

---

## 🔐 Privacy
- ✅ **No cloud**: Runs completely offline
- ✅ **No data upload**: Everything local
- ✅ **Open source**: Transparent, auditable
- ✅ **No ML telemetry**: No model training data collection

---

## 📊 Comparison

| Feature | ML Version | GenAI Version |
|---------|-----------|---------------|
| Model Type | Sklearn classifiers | LLM (Ollama) |
| Accuracy Display | Metrics cards | Natural language |
| Graphs | 3 charts | None |
| Speed | <100ms | 2-10s |
| Training | Required | None |
| Customization | Limited | Full text prompts |
| Offline | Yes | Yes |

---

## 🛠️ Development

### Modify GenAI Prompt
Edit `app.py`, function `generate_genai_analysis()`:
```python
def generate_genai_analysis(patient_data):
    prompt = f"""Your custom medical analysis prompt...
    
    Patient: {patient_data}
    """
    return query_genai_model(prompt)
```

### Add More Health Parameters
1. Update `FEATURES` list in `app.py`
2. Add form field in `index.html`
3. Include in GenAI prompt

---

## 📄 License & Credits
- Heart Disease Prediction Dataset
- Ollama: https://ollama.ai
- Flask Framework
- Modern UI Design

---

**Version**: 2.0 (GenAI) | **Last Updated**: May 14, 2026
