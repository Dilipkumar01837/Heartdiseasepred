from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score,
    recall_score, f1_score, classification_report
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
import joblib
import os

app = Flask(__name__)

# ── Generate synthetic heart disease dataset ──────────────────────────────────
def generate_dataset(n=1000, seed=42):
    np.random.seed(seed)
    age        = np.random.randint(29, 77, n)
    sex        = np.random.randint(0, 2, n)
    cp         = np.random.randint(0, 4, n)
    trestbps   = np.random.randint(94, 200, n)
    chol       = np.random.randint(126, 564, n)
    fbs        = np.random.randint(0, 2, n)
    restecg    = np.random.randint(0, 3, n)
    thalach    = np.random.randint(71, 202, n)
    exang      = np.random.randint(0, 2, n)
    oldpeak    = np.round(np.random.uniform(0, 6.2, n), 1)
    slope      = np.random.randint(0, 3, n)
    ca         = np.random.randint(0, 4, n)
    thal       = np.random.randint(0, 4, n)

    # Approximate target based on risk factors
    risk = (
        (age > 55).astype(int) * 2 +
        (sex == 1).astype(int) +
        (cp > 1).astype(int) * 2 +
        (trestbps > 140).astype(int) +
        (chol > 240).astype(int) +
        (thalach < 130).astype(int) * 2 +
        (exang == 1).astype(int) * 2 +
        (oldpeak > 2).astype(int) * 2 +
        (ca > 1).astype(int) * 2
    )
    target = (risk + np.random.randint(-2, 3, n) > 7).astype(int)

    df = pd.DataFrame({
        'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
        'chol': chol, 'fbs': fbs, 'restecg': restecg,
        'thalach': thalach, 'exang': exang, 'oldpeak': oldpeak,
        'slope': slope, 'ca': ca, 'thal': thal, 'target': target
    })
    return df

# ── Train models at startup ───────────────────────────────────────────────────
df     = generate_dataset()
X      = df.drop('target', axis=1)
y      = df['target']
FEATURES = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_s, y_train)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

def get_metrics(model, X_tr, X_te, y_tr, y_te):
    y_pred = model.predict(X_te)
    y_pred_train = model.predict(X_tr)
    return {
        'accuracy':  round(accuracy_score(y_te, y_pred) * 100, 2),
        'train_acc': round(accuracy_score(y_tr, y_pred_train) * 100, 2),
        'precision': round(precision_score(y_te, y_pred) * 100, 2),
        'recall':    round(recall_score(y_te, y_pred) * 100, 2),
        'f1':        round(f1_score(y_te, y_pred) * 100, 2),
        'cm':        confusion_matrix(y_te, y_pred).tolist(),
        'y_pred':    y_pred.tolist(),
        'y_true':    y_te.tolist()
    }

lr_metrics = get_metrics(lr_model, X_train_s, X_test_s, y_train, y_test)
rf_metrics = get_metrics(rf_model, X_train, X_test, y_train, y_test)

# ── Confusion matrix image ────────────────────────────────────────────────────
def cm_to_base64(cm, title, color):
    fig, ax = plt.subplots(figsize=(4, 3.2))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    sns.heatmap(
        cm, annot=True, fmt='d', cmap=color,
        linewidths=1.5, linecolor='#1a1f2e',
        annot_kws={'size': 18, 'weight': 'bold', 'color': 'white'},
        ax=ax, cbar=False,
        xticklabels=['No Disease', 'Disease'],
        yticklabels=['No Disease', 'Disease']
    )
    ax.set_xlabel('Predicted', color='#8b949e', fontsize=10, labelpad=8)
    ax.set_ylabel('Actual', color='#8b949e', fontsize=10, labelpad=8)
    ax.tick_params(colors='#8b949e', labelsize=9)
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    plt.tight_layout(pad=0.5)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight',
                facecolor='#0d1117', dpi=130)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

lr_cm_img = cm_to_base64(lr_metrics['cm'], 'Logistic Regression', 'Blues')
rf_cm_img = cm_to_base64(rf_metrics['cm'], 'Random Forest', 'Greens')

# ── Feature importance chart ──────────────────────────────────────────────────
def feature_importance_img():
    importances = rf_model.feature_importances_
    idx = np.argsort(importances)[::-1]
    feats = [FEATURES[i] for i in idx]
    vals  = importances[idx]

    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#0d1117')
    colors = ['#ef4444' if v > np.percentile(vals, 70) else '#f97316'
              if v > np.percentile(vals, 40) else '#fb923c' for v in vals]
    bars = ax.barh(feats[::-1], vals[::-1], color=colors[::-1],
                   height=0.6, edgecolor='none')
    ax.set_xlabel('Importance', color='#8b949e', fontsize=10)
    ax.tick_params(colors='#cbd5e1', labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_edgecolor('#30363d')
    ax.spines['left'].set_edgecolor('#30363d')
    ax.xaxis.label.set_color('#8b949e')
    for bar, val in zip(bars, vals[::-1]):
        ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
                f'{val:.3f}', va='center', color='#8b949e', fontsize=8)
    plt.tight_layout(pad=0.5)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight',
                facecolor='#0d1117', dpi=130)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

feat_img = feature_importance_img()

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html',
        lr_metrics=lr_metrics, rf_metrics=rf_metrics,
        lr_cm=lr_cm_img, rf_cm=rf_cm_img,
        feat_img=feat_img,
        features=FEATURES,
        dataset_size=len(df),
        train_size=len(X_train),
        test_size=len(X_test)
    )

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        values = [float(data[f]) for f in FEATURES]
        arr = np.array(values).reshape(1, -1)

        lr_input = scaler.transform(arr)
        lr_pred  = int(lr_model.predict(lr_input)[0])
        lr_prob  = float(lr_model.predict_proba(lr_input)[0][1])

        rf_pred  = int(rf_model.predict(arr)[0])
        rf_prob  = float(rf_model.predict_proba(arr)[0][1])

        # Ensemble
        avg_prob = (lr_prob + rf_prob) / 2
        final    = 1 if avg_prob >= 0.5 else 0

        return jsonify({
            'lr_pred': lr_pred, 'lr_prob': round(lr_prob * 100, 1),
            'rf_pred': rf_pred, 'rf_prob': round(rf_prob * 100, 1),
            'final':   final,   'avg_prob': round(avg_prob * 100, 1),
            'risk_level': 'HIGH' if avg_prob > 0.7 else
                          'MODERATE' if avg_prob > 0.4 else 'LOW'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/model_comparison')
def model_comparison():
    return jsonify({
        'lr': lr_metrics,
        'rf': rf_metrics
    })

if __name__ == '__main__':
    app.run(debug=True)
