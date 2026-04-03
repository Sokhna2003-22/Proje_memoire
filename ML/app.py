import streamlit as st
import pandas as pd
import joblib

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# CSS DESIGN
# =========================
st.markdown("""
<style>

/* GLOBAL */
body {
    background-color: #F5F7FA;
}

/* HEADER */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 40px;
    border-bottom: 1px solid #eee;
}

.logo {
    display: flex;
    align-items: center;
    font-size: 22px;
    font-weight: bold;
    color: #1E3A5F;
}

.logo-icon {
    background-color: #1E3A5F;
    color: white;
    border-radius: 10px;
    padding: 10px;
    margin-right: 10px;
}

/* TITLE */
.title {
    text-align: center;
    margin-top: 40px;
}

.title h1 {
    font-size: 42px;
    color: #1E3A5F;
}

.subtitle {
    color: #6c757d;
}

/* CARD */
.card {
    background: white;
    padding: 30px;
    border-radius: 20px;
    margin-top: 30px;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.05);
}

/* BUTTONS */
.equip-btn {
    padding: 10px 15px;
    border-radius: 12px;
    border: 1px solid #ddd;
    display: inline-block;
    margin: 5px;
    cursor: pointer;
}

/* SLIDER COLOR */
.stSlider > div[data-baseweb="slider"] > div {
    background: linear-gradient(to right, #1E3A5F, #F39C12);
}

/* MAIN BUTTON */
.stButton>button {
    background-color: #1E3A5F;
    color: white;
    border-radius: 12px;
    padding: 15px;
    width: 100%;
    font-size: 18px;
}

/* RESULT */
.result {
    background: #EEF5FF;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    margin-top: 20px;
}

.price {
    font-size: 40px;
    color: #F39C12;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class="header">
    <div class="logo">
        <div class="logo-icon">🏠</div>
        DakarImmo
    </div>
    <div>Prédiction de prix immobilier à Dakar</div>
</div>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown("""
<div class="title">
    <h1>Estimez le prix de votre bien immobilier</h1>
    <p class="subtitle">Renseignez les caractéristiques pour obtenir une estimation instantanée</p>
</div>
""", unsafe_allow_html=True)

# =========================
# TYPE
# =========================
type_annonce = st.radio("", ["Vente", "Location"], horizontal=True)

# =========================
# CARD FORM
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📐 Caractéristiques")

    surface = st.slider("📏 Surface (m²)", 10, 500, 150)
    chambres = st.slider("🛏️ Nombre de chambres", 0, 10, 3)
    sdb = st.slider("🚿 Salles de bain", 0, 5, 2)
    etages = st.slider("🏢 Étage", 0, 10, 0)
    salons = st.slider("🛋️ Salons", 0, 5, 1)

with col2:
    st.subheader("📍 Localisation & équipements")

    localisation = st.selectbox("📍 Localisation", [
        "Almadies", "Ngor", "Mermoz", "Yoff",
        "Maristes", "Hann", "Plateau"
    ])

    st.markdown("### 🏠 Équipements")

    ascenseur = st.checkbox("🏢 Ascenseur")
    jardin = st.checkbox("🌿 Jardin")
    parking = st.checkbox("🚗 Parking")
    internet = st.checkbox("🌐 Internet")
    piscine = st.checkbox("🏊 Piscine")
    clim = st.checkbox("❄️ Climatisation")
    surveillance = st.checkbox("🛡️ Surveillance")

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
model_loc = joblib.load("model_location.pkl")
model_vente = joblib.load("model_vente.pkl")

# =========================
# BUTTON
# =========================
if st.button("💰 Estimer le prix"):

    data = pd.DataFrame({
        "Surface_m2": [surface],
        "Nb_Chambres": [chambres],
        "Nb_Salles_Bain": [sdb],
        "Nb_Salons": [salons],
        "Nb_Etages": [etages],
        "Ascenseur": [int(ascenseur)],
        "Jardin": [int(jardin)],
        "Parking": [int(parking)],
        "Internet": [int(internet)],
        "Piscine": [int(piscine)],
        "Climatisation": [int(clim)],
        "Surveillance": [int(surveillance)],
        "Localisation": [localisation]
    })

    data = pd.get_dummies(data, columns=['Localisation'], drop_first=True)

    model = model_loc if type_annonce == "Location" else model_vente

    for col in model.feature_names_in_:
        if col not in data.columns:
            data[col] = 0

    data = data[model.feature_names_in_]

    prediction = model.predict(data)[0]

    st.markdown(f"""
    <div class="result">
        <h2>💎 Prix estimé</h2>
        <div class="price">{int(prediction):,} FCFA</div>
    </div>
    """, unsafe_allow_html=True)
