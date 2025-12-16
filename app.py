import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Visualisation Scoring Client",
    layout="wide"
)

API_BASE_URL = st.sidebar.text_input(
    "🔗 URL Backend API",
    value="http://localhost:5000"
)

# =============================
# HEADER
# =============================
st.title("🏦 Visualisation du Scoring Client")
st.markdown(
    "Outil de **consultation et d’analyse** des profils clients pour l’aide à la décision bancaire."
)

st.divider()

# =============================
# INPUT CLIENT ID
# =============================
st.subheader("🔎 Recherche client")

client_id = st.text_input(
    "ID Client",
    placeholder="Ex : CLT_000123"
)

load_client = st.button("📊 Charger les données")

# =============================
# FETCH DATA
# =============================
if load_client and client_id:
    try:
        response = requests.get(
            f"{API_BASE_URL}/client/{client_id}",
            timeout=5
        )
        data = response.json()

        # =============================
        # KPIs
        # =============================
        st.subheader("📌 Indicateurs clés")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Score de risque", data["score"])
        col2.metric("Probabilité de défaut", f"{data['pd']} %")
        col3.metric("Revenus annuels", f"{data['income']} €")
        col4.metric("Montant du prêt", f"{data['loan_amount']} €")

        st.divider()

        # =============================
        # PROFIL CLIENT
        # =============================
        st.subheader("👤 Profil client")

        profile_df = pd.DataFrame.from_dict(
            data["profile"],
            orient="index",
            columns=["Valeur"]
        )

        st.dataframe(profile_df, use_container_width=True)

        # =============================
        # CONTRIBUTION FEATURES
        # =============================
        st.subheader("📊 Facteurs de risque")

        features_df = pd.DataFrame(data["feature_importance"])

        fig = px.bar(
            features_df,
            x="feature",
            y="impact",
            title="Contribution des variables au score"
        )

        st.plotly_chart(fig, use_container_width=True)

        # =============================
        # HISTORIQUE
        # =============================
        st.subheader("🕒 Historique du score")

        history_df = pd.DataFrame(data["history"])

        fig_hist = px.line(
            history_df,
            x="date",
            y="score",
            markers=True,
            title="Évolution du score dans le temps"
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")

elif load_client and not client_id:
    st.warning("Veuillez renseigner un ID client")
