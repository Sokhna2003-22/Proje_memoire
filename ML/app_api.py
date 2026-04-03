from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Charger modèles
model_loc = joblib.load("model_location.pkl")
model_vente = joblib.load("model_vente.pkl")

@app.route("/")
def home():
    return "API Immobilier Dakar active 🚀"

@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    df = pd.DataFrame([data])

    # Encodage
    df = pd.get_dummies(df, columns=['Localisation'], drop_first=True)

    # Choix modèle
    model = model_loc if data["Type"] == "Location" else model_vente

    # Alignement colonnes
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0

    df = df[model.feature_names_in_]

    prediction = model.predict(df)[0]

    return jsonify({
        "prix_estime": int(prediction)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

