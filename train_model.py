import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Charger les données depuis le fichier CSV
data = pd.read_csv('login_history.csv')

# Prétraitement des données
X = data[['ip_address', 'user_agent', 'timestamp']]  # Colonnes pertinentes
y = data['is_brute_force']  # Colonne indiquant si c'est une attaque brute force

# Séparer les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entraîner le modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

# Sauvegarder le modèle entraîné
joblib.dump(model, 'brute_force_model.pkl')
