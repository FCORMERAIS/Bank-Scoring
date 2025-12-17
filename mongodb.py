import streamlit as st
from pymongo import MongoClient

# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="Visualisation Client",
    layout="wide"
)

MONGO_URI = "mongodb+srv://sdv_user:SDV2025@cluster0.t2ptc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "default_risk"
COLLECTION_NAME = "users_data"

# =============================
# HEADER
# =============================
st.title("👤 Visualisation du client")
st.markdown("Recherche d’un client à partir de son **SK_CURR_ID**")

st.divider()

# =============================
# INPUT CLIENT ID
# =============================
sk_curr_id = st.text_input(
    "SK_CURR_ID",
    placeholder="Ex : 100001"
)

load_client = st.button("📊 Charger le client")

# =============================
# CONNEXION MONGODB (cache)
# =============================
@st.cache_resource
def get_mongo_client(uri):
    return MongoClient(uri)

client = get_mongo_client(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# =============================
# FETCH DATA
# =============================
if load_client and sk_curr_id:
    try:
        # ⚠️ Si SK_CURR_ID est un INT dans MongoDB
        query_value = int(sk_curr_id) if sk_curr_id.isdigit() else sk_curr_id

        data = collection.find_one({"SK_CURR_ID": query_value})

        if not data:
            st.warning(f"Aucun client trouvé avec SK_CURR_ID : {sk_curr_id}")
        else:
            st.subheader("Informations du client")

            st.write(f"**Prénom :** {data.get('FirstName', 'N/A')}")
            st.write(f"**Nom :** {data.get('LastName', 'N/A')}")

            photo_url = data.get("PhotoURL")
            if photo_url:
                st.image(
                    photo_url,
                    caption=f"{data.get('FirstName', '')} {data.get('LastName', '')}",
                    width=200
                )
            else:
                st.info("Pas de photo disponible pour ce client.")

    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")

elif load_client and not sk_curr_id:
    st.warning("Veuillez renseigner un SK_CURR_ID")
