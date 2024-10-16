from flask import Flask, request, jsonify
import joblib
import pandas as pd
import datetime

app = Flask(__name__)

# Charger votre modèle de prédiction
model = joblib.load('brute_force_model.pkl')  # Modèle sauvegardé au format pickle

# Fonction pour analyser les tentatives de connexion
def analyze_attempt(data):
    username = data.get('username')
    ip_address = data.get('ip_address')
    time = data.get('time')

    # Lire l'historique des connexions depuis le fichier CSV
    df = pd.read_csv('user_login.csv')  # CSV contenant les tentatives de connexion

    # Ajouter la nouvelle tentative de connexion au dataframe pour l'analyse
    new_data = pd.DataFrame({
        'username': [username],
        'ip_address': [ip_address],
        'time': [time],
        'action': ['LOGIN'],  # Spécifier l'action ici
        'failed_attempts': [0]  # Exemple de champ pour les tentatives échouées
    })

    # Préparer les caractéristiques pour le modèle
    features = new_data[['username', 'ip_address', 'time']]

    # Faire la prédiction
    prediction = model.predict(features)

    # Si la prédiction est > 0.5, on considère que c'est une tentative suspecte
    if prediction[0] > 0.5:
        return {"block_ip": ip_address, "message": "Tentative suspecte détectée"}
    else:
        return {"block_ip": None, "message": "Connexion normale"}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    result = analyze_attempt(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
