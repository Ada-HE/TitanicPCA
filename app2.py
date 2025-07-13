import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Cargar modelos y transformadores
model = joblib.load('model.pkl')
pca = joblib.load('pca_transform.pkl')
scaler = joblib.load('scaler_t.pkl')
encoder = joblib.load('encoder.pkl')
age_model = joblib.load('age_model.pkl')


@app.route('/')
def form():
    return render_template('formu.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Convertir a DataFrame si es necesario
    input_data = pd.DataFrame([data])

    # Codificar las variables categóricas
    cat_cols = ['Sex', 'Embarked', 'Cabin', 'Ticket']
    input_data[cat_cols] = encoder.transform(input_data[cat_cols])

    # Escalar
    input_scaled = scaler.transform(input_data)

    # PCA
    input_pca = pca.transform(input_scaled)

    # Predicción
    prediction = model.predict(input_pca)

    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)
