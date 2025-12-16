import streamlit as st
import requests

st.set_page_config(
    page_title="Mon app Data",
    layout="wide"
)

st.title("🚀 Mon application Streamlit")

st.markdown("Interface front simple (Streamlit)")

st.divider()

# --- Section 1 : Test ---
st.header("🔍 Test")

name = st.text_input("Ton prénom")

if st.button("Dire bonjour"):
    if name:
        st.success(f"Bonjour {name} 😄")
    else:
        st.warning("Entre un prénom")

# --- Section 2 : API ---
st.header("📡 Appel API (exemple)")

api_url = st.text_input(
    "URL API",
    value="https://api.github.com"
)

if st.button("Appeler l'API"):
    try:
        response = requests.get(api_url, timeout=5)
        st.json(response.json())
    except Exception as e:
        st.error(str(e))
