from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# 🔥 Chemin absolu vers le dossier actuel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 🔥 Charger les modèles correctement
model_loc = joblib.load(os.path.join(BASE_DIR, "model_location.pkl"))
model_vente = joblib.load(os.path.join(BASE_DIR, "model_vente.pkl"))

@app.route("/")
def home():
    return "API Immobilier Dakar active 🚀"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Transformer en DataFrame
        df = pd.DataFrame([data])

        # Encodage
        if 'Localisation' in df.columns:
            df = pd.get_dummies(df, columns=['Localisation'], drop_first=True)

        # Choix modèle
        model = model_loc if data.get("Type") == "Location" else model_vente

        # Alignement des colonnes
        for col in model.feature_names_in_:
            if col not in df.columns:
                df[col] = 0

        df = df[model.feature_names_in_]

        # Prédiction
        prediction = model.predict(df)[0]

        return jsonify({
            "prix_estime": int(prediction)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# 🔥 Important pour Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))