import pandas as pd
import joblib

# Charger le modèle entraîné
model = joblib.load('brute_force_model.pkl')

# Exemple de nouvelles données (données de connexion actuelles)
new_data = {
    'ip_address': '192.168.0.1',
    'user_agent': 'Mozilla/5.0',
    'timestamp': '2023-09-29 10:15:00'
}

# Convertir en DataFrame
df_new_data = pd.DataFrame([new_data])

# Faire la prédiction
prediction = model.predict(df_new_data)
if prediction[0] == 1:
    print("Tentative de brute force détectée !")
else:
    print("Connexion normale.")
