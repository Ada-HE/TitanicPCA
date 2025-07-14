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

    # --- Asegura claves y valores por defecto ---
    cleaned_data = {
        'Pclass': int(data.get('Pclass', 0)),
        'Sex': str(data.get('Sex', '')).lower(),
        'Age': data.get('Age', None),  # Puede venir None
        'SibSp': int(data.get('SibSp', 0)),
        'Parch': int(data.get('Parch', 0)),
        'Ticket': str(data.get('Ticket', 'unknown')),
        'Fare': float(data.get('Fare', 0) or 0),
        'Cabin': str(data.get('Cabin', 'Desconocido')),
        'Embarked': str(data.get('Embarked', 'unknown'))
    }

    # ✅ Si no hay Age, predecirlo
    if cleaned_data['Age'] in [None, '', 0]:
        x_age = pd.DataFrame([{
            'Pclass': cleaned_data['Pclass'],
            'SibSp': cleaned_data['SibSp'],
            'Parch': cleaned_data['Parch'],
            'Fare': cleaned_data['Fare']
        }])
        predicted_age = age_model.predict(x_age)[0]
        cleaned_data['Age'] = float(predicted_age)
        print(f"🔍 Age imputado: {predicted_age}")

    input_data = pd.DataFrame([cleaned_data])
    print("\n📊 DataFrame con Age imputado (si aplica):")
    print(input_data)

    # --- Transformación ---
    cat_cols = ['Sex', 'Embarked', 'Cabin', 'Ticket']
    input_data[cat_cols] = encoder.transform(input_data[cat_cols])

    input_scaled = scaler.transform(input_data)
    input_pca = pca.transform(input_scaled)
    prediction = model.predict(input_pca)

    return jsonify({
        'prediction': prediction.tolist(),
        'details': {
            'raw_input': data,
            'cleaned_data': cleaned_data,
            'input_data': input_data.to_dict(orient='records')
        }
    })



if __name__ == '__main__':
    app.run(debug=True)
