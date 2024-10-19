from flask import Flask, request, jsonify
import pandas as pd
import joblib
import socket
import random
import string

# Charger le modèle et le scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

app = Flask(__name__)

def encode_ip(ip_address):
    """Convertir l'adresse IP en entier."""
    return int.from_bytes(socket.inet_aton(ip_address), 'big')

def generate_slug(length=8):
    """Générer un slug aléatoire de 8 caractères."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def block_ip(ip_address):
    """Bloquer une IP (logique à définir, par exemple ajout à une liste noire)."""
    print(f"IP {ip_address} bloquée.")

@app.route('/detect', methods=['POST'])
def detect_attack():
    """Endpoint pour détecter si une tentative de connexion est une attaque."""
    data = request.get_json()
    if not data or 'ip_address' not in data:
        return jsonify({"error": "Données invalides"}), 400
    
    ip_address = data['ip_address']
    ip_encoded = encode_ip(ip_address)

    # Créer un DataFrame pour la nouvelle tentative
    new_data = pd.DataFrame([[ip_encoded, 0, 1]], columns=['ip_encoded', 'time_diff', 'Success'])  # Ajoutez votre logique

    # Appliquer le scaler et faire une prédiction
    new_data_scaled = scaler.transform(new_data)
    prediction = model.predict(new_data_scaled)
    
    # Si l'anomalie est détectée (-1), bloquer l'IP
    if prediction[0] == -1:
        block_ip(ip_address)
        slug = generate_slug()
        return jsonify({"status": "blocked", "ip_address": ip_address, "slug": slug})
    
    return jsonify({"status": "allowed", "ip_address": ip_address})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
