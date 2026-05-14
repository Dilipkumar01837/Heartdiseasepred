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
    prompt = f"""You are a medical AI assistant. Analyze the following patient health data and provide:
1. A brief cardiovascular risk assessment (HIGH/MODERATE/LOW)
2. Key risk factors identified
3. Recommendations for the patient
4. A confidence level (0-100%)

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

Provide concise medical-grade analysis with clear sections."""
    
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
        
        # Generate GenAI analysis
        analysis = generate_genai_analysis(patient_data)
        
        # Parse risk level from analysis
        risk_level = 'MODERATE'
        if 'high' in analysis.lower() and 'high risk' in analysis.lower():
            risk_level = 'HIGH'
        elif 'low' in analysis.lower() and 'low risk' in analysis.lower():
            risk_level = 'LOW'
        
        return jsonify({
            'analysis': analysis,
            'risk_level': risk_level,
            'model': f'GenAI ({MODEL_NAME})',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    """Check if Google Gemini API is available"""
    print(f"DEBUG: GEMINI_API_KEY = {GEMINI_API_KEY}")
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
