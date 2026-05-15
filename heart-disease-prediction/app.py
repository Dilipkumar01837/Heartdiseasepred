from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# ── Google Gemini GenAI Integration ──────────────────────────────────────────
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
MODEL_NAME = 'models/gemini-2.5-flash'

# Configure Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    genai_available = True
else:
    genai_available = False

FEATURES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

def calculate_risk_level(patient_data):
    """Calculate a stable risk level from patient metrics."""
    score = 0
    risk_factors = []

    age = patient_data['age']
    trestbps = patient_data['trestbps']
    chol = patient_data['chol']
    thalach = patient_data['thalach']
    oldpeak = patient_data['oldpeak']

    if age >= 60:
        score += 2
        risk_factors.append('age 60 or older')
    elif age >= 45:
        score += 1
        risk_factors.append('middle-age risk group')

    if patient_data['sex'] == 1:
        score += 1
        risk_factors.append('male sex')

    if patient_data['cp'] == 3:
        score += 3
        risk_factors.append('asymptomatic chest pain pattern')
    elif patient_data['cp'] == 2:
        score += 2
        risk_factors.append('non-anginal chest pain')
    elif patient_data['cp'] == 1:
        score += 1
        risk_factors.append('atypical angina')

    if trestbps >= 160:
        score += 2
        risk_factors.append('very high resting blood pressure')
    elif trestbps >= 140:
        score += 1
        risk_factors.append('elevated resting blood pressure')

    if chol >= 280:
        score += 2
        risk_factors.append('very high cholesterol')
    elif chol >= 240:
        score += 1
        risk_factors.append('high cholesterol')

    if patient_data['fbs'] == 1:
        score += 1
        risk_factors.append('fasting blood sugar above 120 mg/dl')

    if patient_data['restecg'] == 2:
        score += 2
        risk_factors.append('left ventricular hypertrophy ECG finding')
    elif patient_data['restecg'] == 1:
        score += 1
        risk_factors.append('ST-T ECG abnormality')

    if thalach < 120:
        score += 2
        risk_factors.append('low maximum heart rate')
    elif thalach < 150:
        score += 1
        risk_factors.append('reduced maximum heart rate')

    if patient_data['exang'] == 1:
        score += 2
        risk_factors.append('exercise-induced angina')

    if oldpeak >= 2.5:
        score += 2
        risk_factors.append('significant ST depression')
    elif oldpeak >= 1:
        score += 1
        risk_factors.append('mild ST depression')

    if patient_data['slope'] == 2:
        score += 2
        risk_factors.append('downsloping ST segment')
    elif patient_data['slope'] == 1:
        score += 1
        risk_factors.append('flat ST segment')

    if patient_data['ca'] >= 2:
        score += 2
        risk_factors.append('multiple major vessels involved')
    elif patient_data['ca'] == 1:
        score += 1
        risk_factors.append('one major vessel involved')

    if patient_data['thal'] == 2:
        score += 2
        risk_factors.append('reversible thalassemia defect')
    elif patient_data['thal'] == 1:
        score += 1
        risk_factors.append('fixed thalassemia defect')

    if score >= 10:
        risk_level = 'HIGH'
    elif score >= 5:
        risk_level = 'MODERATE'
    else:
        risk_level = 'LOW'

    return risk_level, score, risk_factors

def query_genai_model(prompt):
    """Query Google Gemini AI model"""
    if not genai_available:
        return 'Error: GEMINI_API_KEY not configured. Please set your API key.'
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                max_output_tokens=1024
            )
        )
        return response.text if response.text else 'Unable to generate analysis'
    except Exception as e:
        return f'Error: {str(e)}'

def generate_genai_analysis(patient_data):
    """Generate heart disease risk analysis using Google Gemini"""
    risk_level, risk_score, risk_factors = calculate_risk_level(patient_data)
    risk_factor_text = ', '.join(risk_factors) if risk_factors else 'no major risk factors from rule-based screening'

    prompt = f"""You are a medical AI assistant. Analyze the following patient health data and provide:
1. A brief cardiovascular risk assessment. Use this exact risk level: {risk_level}
2. Key risk factors identified
3. Recommendations for the patient
4. A confidence level (0-100%)
5. A short note that this is educational guidance, not a diagnosis

Patient Data:
- Age: {patient_data['age']} years
- Sex: {"Male" if patient_data['sex'] == 1 else "Female"}
- Chest Pain Type: {["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"][int(patient_data['cp'])]}
- Resting Blood Pressure: {patient_data['trestbps']} mm Hg
- Serum Cholesterol: {patient_data['chol']} mg/dl
- Fasting Blood Sugar > 120: {"Yes" if patient_data['fbs'] == 1 else "No"}
- Resting ECG: {["Normal", "ST-T Abnormality", "LV Hypertrophy"][int(patient_data['restecg'])]}
- Max Heart Rate Achieved: {patient_data['thalach']} bpm
- Exercise-Induced Angina: {"Yes" if patient_data['exang'] == 1 else "No"}
- ST Depression: {patient_data['oldpeak']}
- Slope of ST: {["Upsloping", "Flat", "Downsloping"][int(patient_data['slope'])]}
- Major Vessels Colored: {int(patient_data['ca'])}
- Thalassemia: {["Normal", "Fixed Defect", "Reversible Defect", "Unknown"][int(patient_data['thal'])]}

Rule-based screening result:
- Risk Level: {risk_level}
- Risk Score: {risk_score}
- Main Risk Factors: {risk_factor_text}

Provide concise medical-grade analysis with clear sections. Do not change the risk level."""
    
    return query_genai_model(prompt)

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', features=FEATURES)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        # Ensure all required fields are present
        patient_data = {}
        for feature in FEATURES:
            if feature not in data:
                return jsonify({'error': f'Missing field: {feature}'}), 400
            patient_data[feature] = float(data[feature])
        
        risk_level, risk_score, risk_factors = calculate_risk_level(patient_data)
        analysis = generate_genai_analysis(patient_data)
        
        return jsonify({
            'analysis': analysis,
            'risk_level': risk_level,
            'risk_score': risk_score,
            'risk_factors': risk_factors,
            'model': f'GenAI ({MODEL_NAME})',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Check if Google Gemini API is available"""
    print(f"DEBUG: genai_available = {genai_available}")
    
    if not GEMINI_API_KEY:
        return jsonify({
            'status': 'error',
            'gemini_available': False,
            'message': 'GEMINI_API_KEY environment variable not set',
            'setup_url': 'https://ai.google.dev'
        }), 503
    
    try:
        # List available models first
        models = genai.list_models()
        print(f"DEBUG: Available models = {[m.name for m in models]}")
        
        # Use a known working model
        model_name = 'models/gemini-2.5-flash'
        print(f"DEBUG: Using hardcoded model = {model_name}")
        
        model = genai.GenerativeModel(model_name)
        # Test the API with a simple query
        response = model.generate_content('Say "OK" in one word')
        print(f"DEBUG: API response = {response}")
        if response.text:
            return jsonify({
                'status': 'ok',
                'gemini_available': True,
                'model': model_name,
                'message': f'Google Gemini API is connected and working ({model_name})'
            })
    except Exception as e:
        print(f"DEBUG: API Error = {str(e)}")
        return jsonify({
            'status': 'error',
            'gemini_available': False,
            'message': f'API Error: {str(e)}'
        }), 503
    
    return jsonify({
        'status': 'error',
        'gemini_available': False,
        'message': 'Could not connect to Google Gemini API'
    }), 503

if __name__ == '__main__':
    app.run(debug=True)
