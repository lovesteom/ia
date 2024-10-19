import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib
import socket

# Charger les données des tentatives de connexion
data = pd.read_csv('user_login.csv')

# Encodage des adresses IP en entiers
data['ip_encoded'] = data['IP Address'].apply(lambda x: int.from_bytes(socket.inet_aton(x), 'big'))

# Calculer la différence de temps entre les tentatives (en secondes)
data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data['time_diff'] = data['Timestamp'].diff().dt.total_seconds().fillna(0)

# Préparer les données d'entraînement
features = ['ip_encoded', 'time_diff', 'Success']
X = data[features]

# Normaliser les données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Entraîner un modèle d'Isolation Forest pour la détection d'anomalies
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_scaled)

# Sauvegarder le modèle et le scaler pour une utilisation ultérieure
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("Modèle entraîné et sauvegardé.")
