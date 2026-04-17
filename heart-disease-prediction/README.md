# ❤️ CardioAI — Heart Disease Prediction

A full-stack ML web app that predicts heart disease risk using **Logistic Regression** and **Random Forest**, with a dark-themed medical dashboard UI.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure
```
heart-disease-prediction/
├── app.py               # Flask backend + ML models
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Full UI (dark dashboard)
└── README.md
```

---

## 🧠 ML Features

| Feature     | Description                    |
|-------------|-------------------------------|
| age         | Age in years                   |
| sex         | 0=Female, 1=Male               |
| cp          | Chest pain type (0–3)          |
| trestbps    | Resting blood pressure (mm Hg) |
| chol        | Serum cholesterol (mg/dl)      |
| fbs         | Fasting blood sugar > 120      |
| restecg     | Resting ECG results (0–2)      |
| thalach     | Max heart rate achieved        |
| exang       | Exercise-induced angina        |
| oldpeak     | ST depression                  |
| slope       | Slope of peak ST segment       |
| ca          | Major vessels colored (0–3)    |
| thal        | Thalassemia type               |

---

## 📊 Models Used

- **Logistic Regression** — scikit-learn, L2 regularization, max_iter=1000
- **Random Forest** — 100 estimators, random_state=42
- **Ensemble** — Average probability of both models

---

## 🖥️ UI Features

- Live prediction form with all 13 features
- Risk level: HIGH / MODERATE / LOW
- Confusion matrix (both models, matplotlib heatmap)
- Accuracy, Precision, Recall, F1 Score
- Feature importance chart (Random Forest)
- Dataset split stats (80/20 train-test)

---

## ⚙️ Tech Stack

- **Backend**: Python, Flask, scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn (rendered as base64 PNG)
- **Frontend**: Vanilla HTML/CSS/JS (no framework required)
- **Font**: Outfit + Space Mono (Google Fonts)
