import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Assistant Scoring Bancaire",
    layout="wide"
)

API_BASE_URL = st.sidebar.text_input(
    "🔗 URL Backend API",
    value="http://localhost:5000"
)

# =============================
# SIDEBAR
# =============================
st.sidebar.title("🏦 Scoring Bancaire")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Accueil",
        "🧮 Scoring Client",
        "📊 Visualisations",
        "🩺 Monitoring",
        "💬 Feedback"
    ]
)

# =============================
# PAGE : ACCUEIL
# =============================
if page == "🏠 Accueil":
    st.title("🚀 Assistant Intelligent de Scoring Bancaire")

    st.markdown("""
    ### 🎯 Objectif
    Cette application aide les **conseillers bancaires** à évaluer le **risque de crédit**
    d’un client de manière **rapide, fiable et explicable**.

    ### ✅ Fonctionnalités
    - Analyse automatique des profils clients  
    - Calcul d’un score de risque en temps réel  
    - Visualisations explicatives  
    - Recommandations d’octroi de crédit  
    - Traçabilité et conformité réglementaire  

    ### 🛠️ Architecture
    - **Frontend** : Streamlit  
    - **Backend** : Flask API  
    - **ML Engine** : Azure Databricks  
    - **Storage** : MongoDB Atlas  
    """)

# =============================
# PAGE : SCORING CLIENT
# =============================
elif page == "🧮 Scoring Client":
    st.title("🧮 Évaluation du risque client")

    with st.form("scoring_form"):
        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Âge", min_value=18, max_value=100, value=35)
            income = st.number_input("Revenus annuels (€)", min_value=0, value=45000)
            employment_years = st.number_input("Ancienneté professionnelle (années)", min_value=0, value=5)

        with col2:
            loan_amount = st.number_input("Montant du prêt (€)", min_value=0, value=150000)
            loan_duration = st.number_input("Durée du prêt (années)", min_value=1, value=20)
            has_defaults = st.selectbox("Antécédents de défaut ?", ["Non", "Oui"])

        submitted = st.form_submit_button("📡 Calculer le score")

    if submitted:
        payload = {
            "age": age,
            "income": income,
            "employment_years": employment_years,
            "loan_amount": loan_amount,
            "loan_duration": loan_duration,
            "has_defaults": has_defaults == "Oui"
        }

        try:
            response = requests.post(
                f"{API_BASE_URL}/predict",
                json=payload,
                timeout=5
            )
            result = response.json()

            st.success("Score calculé avec succès")

            st.metric(
                label="📉 Score de risque",
                value=result.get("score", "N/A")
            )

            st.write("### 📌 Recommandation")
            st.info(result.get("recommendation", "Non disponible"))

        except Exception as e:
            st.error(f"Erreur lors de l'appel API : {e}")

# =============================
# PAGE : VISUALISATIONS
# =============================
elif page == "📊 Visualisations":
    st.title("📊 Explication du score")

    st.markdown("Visualisation des principaux facteurs de risque (exemple)")

    data = pd.DataFrame({
        "Feature": ["Revenus", "Montant du prêt", "Ancienneté", "Antécédents"],
        "Impact": [0.4, 0.3, 0.2, 0.1]
    })

    fig = px.bar(
        data,
        x="Feature",
        y="Impact",
        title="Contribution des variables au score"
    )

    st.plotly_chart(fig, use_container_width=True)

# =============================
# PAGE : MONITORING
# =============================
elif page == "🩺 Monitoring":
    st.title("🩺 État des services")

    if st.button("🔄 Vérifier l'état"):
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            st.success(response.json())
        except Exception as e:
            st.error(f"Backend indisponible : {e}")

# =============================
# PAGE : FEEDBACK
# =============================
elif page == "💬 Feedback":
    st.title("💬 Feedback Conseiller")

    feedback = st.text_area("Votre retour sur la décision proposée")

    if st.button("📤 Envoyer le feedback"):
        try:
            response = requests.post(
                f"{API_BASE_URL}/feedback",
                json={"feedback": feedback},
                timeout=5
            )
            st.success("Feedback envoyé avec succès")
        except Exception as e:
            st.error(f"Erreur : {e}")
