import streamlit as st
import requests
import threading
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import app as flask_app  # Importer ton Flask existant

# --- Configuration Streamlit ---
st.set_page_config(page_title="Front Risque Crédit", layout="wide")

# --- Titre de l'application ---
st.title("Analyse de risque de défaut de crédit")

# --- Input utilisateur ---
client_id = st.text_input("Entrez le Client ID :")

if st.button("Analyser") and client_id:
    API_URL = f"http://127.0.0.1:5000/predict_default?client_id={client_id}"
    
    try:
        response = requests.get(API_URL, timeout=60)  # timeout pour éviter blocage
        if response.status_code != 200:
            st.error(f"Erreur API : {response.json().get('error')}")
        else:
            data = response.json()
            client_info = data.get("client_info", {})
            prediction = data.get("prediction", {})
            recommendation = data.get("recommendation", {})
            
            # --- Informations client ---
            st.subheader("Informations Client")
            st.json(client_info)
            
            # --- Prédiction et recommandations ---
            st.subheader("Prédiction et recommandations")
            st.metric("Score de risque", round(prediction.get("risk_score", 0), 2))
            st.write(f"Décision : **{recommendation.get('decision', '')}**")
            st.write(f"Niveau de risque : **{recommendation.get('risk_level', '')}**")
            st.write(f"Explication : {recommendation.get('explanation', '')}")
            st.write("Plan d'action :")
            for step in recommendation.get("action_plan", []):
                st.write(f"- {step}")
            
            # --- Insights calculés ---
            st.subheader("Insights clés")
            credit_amount = client_info.get("credit_amount", 0)
            income = client_info.get("income", 0)
            ratio_credit_revenu = credit_amount / income if income else 0
            st.write(f"- Ratio crédit/revenu : {ratio_credit_revenu:.2f}")
            st.write(f"- Ancienneté professionnelle : {client_info.get('years_employed', 0)} ans")
            st.write(f"- Profil stable : âge {client_info.get('age', '')}, statut {client_info.get('family_status', '')}, logement {client_info.get('housing_type', '')}")
            st.write("- Opportunité cross-selling : assurance, épargne, produits complémentaires")
            
            # --- Graphiques ---
            st.subheader("Visualisations")
            
            # 1️⃣ Ratio crédit / revenu
            fig_ratio = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = ratio_credit_revenu,
                title = {'text': "Ratio Crédit / Revenu"},
                gauge = {'axis': {'range': [0, 2]},
                         'bar': {'color': "green" if ratio_credit_revenu <= 1 else "red"},
                         'steps' : [
                             {'range': [0, 0.5], 'color': "lightgreen"},
                             {'range': [0.5, 1], 'color': "yellow"},
                             {'range': [1, 2], 'color': "red"}]}))
            st.plotly_chart(fig_ratio, use_container_width=True)
            
            # 2️⃣ Score de risque
            fig_risk = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction.get("risk_score", 0),
                title={'text': "Score de risque"},
                gauge={'axis': {'range': [0,1]},
                       'bar': {'color': "green" if prediction.get("risk_score", 0)<=0.4 else "orange"},
                       'steps': [
                           {'range':[0,0.4],'color':'lightgreen'},
                           {'range':[0.4,0.7],'color':'yellow'},
                           {'range':[0.7,1],'color':'red'}]}))
            st.plotly_chart(fig_risk, use_container_width=True)
            
            # 3️⃣ Exemple comparatif produits (simulé)
            df_products = pd.DataFrame({
                "Produit": ["Crédit Auto", "Crédit Immobilier", "Crédit Personnel"],
                "Taux de défaut": [0.05, 0.02, 0.08]
            })
            fig_products = px.bar(df_products, x="Produit", y="Taux de défaut",
                                  title="Taux de défaut par produit",
                                  color="Taux de défaut",
                                  color_continuous_scale=px.colors.sequential.Viridis)
            st.plotly_chart(fig_products, use_container_width=True)
            
    except requests.exceptions.ConnectionError:
        st.error("Impossible de se connecter à l'API Flask. Vérifiez que Flask est bien lancé.")
    except requests.exceptions.Timeout:
        st.error("Le serveur Databricks met trop de temps à répondre.")
    except Exception as e:
        st.error(f"Erreur inattendue : {str(e)}")
