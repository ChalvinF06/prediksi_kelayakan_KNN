from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Memuat model dan data pendukung
model = joblib.load('knn_model.pkl')
label_mapping = joblib.load('label_mapping.pkl')
feature_columns = joblib.load('feature_columns.pkl')

@app.route('/')
def home():
    return render_template('index.html', feature_columns=feature_columns)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Mengumpulkan semua nilai input
        input_data = {}
        for feature in feature_columns:
            input_data[feature] = float(request.form.get(feature, 0))
        
        # Membuat DataFrame dari input
        df_input = pd.DataFrame([input_data])
        
        # Prediksi
        prediction = model.predict(df_input)[0]
        prediction_label = label_mapping[prediction]
        
        # Hitung probabilitas
        prediction_proba = model.predict_proba(df_input)[0]
        confidence = prediction_proba[prediction] * 100
        
        return render_template('result.html', 
                              prediction=prediction_label,
                              confidence=confidence,
                              input_data=input_data)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    # Endpoint API untuk integrasi dengan aplikasi lain
    if request.is_json:
        data = request.get_json()
        
        # Validasi input
        for feature in feature_columns:
            if feature not in data:
                return jsonify({"error": f"Missing feature: {feature}"}), 400
        
        # Membuat DataFrame
        input_df = pd.DataFrame([{feature: float(data[feature]) for feature in feature_columns}])
        
        # Prediksi
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]
        
        return jsonify({
            "prediction": label_mapping[prediction],
            "confidence": round(prediction_proba[prediction] * 100, 2),
            "prediction_code": int(prediction)
        })
    
    return jsonify({"error": "Request must be JSON"}), 400

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)