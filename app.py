import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect('hotelie.db')
c = conn.cursor()

st.title("🏨 Application de Gestion Hôtelière")

# ======================= Menu principal =======================
menu = st.sidebar.radio("Menu", [
    "Liste des réservations",
    "Liste des clients",
    "Chambres disponibles",
    "Ajouter un client",
    "Ajouter une réservation"
])

# ======================= 1. Réservations =======================
if menu == "Liste des réservations":
    st.subheader("📄 Liste des réservations")
    query = """
    SELECT r.idReservation, c.nomComplet, r.dateDebut, r.dateFin
    FROM Reservation r
    JOIN Client c ON r.idClient = c.idClient
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

# ======================= 2. Clients =======================
elif menu == "Liste des clients":
    st.subheader("👥 Liste des clients")
    df_clients = pd.read_sql_query("SELECT * FROM Client", conn)
    st.dataframe(df_clients)

# ======================= 3. Chambres disponibles =======================
elif menu == "Chambres disponibles":
    st.subheader("🛏️ Chambres disponibles entre deux dates")

    date_debut = st.date_input("Date d'arrivée")
    date_fin = st.date_input("Date de départ")

    if date_debut and date_fin:
        dispo_query = f"""
        SELECT * FROM Chambre
        WHERE idChambre NOT IN (
            SELECT idChambre FROM Reservation
            WHERE dateDebut <= '{date_fin}' AND dateFin >= '{date_debut}'
        )
        """
        df_dispo = pd.read_sql_query(dispo_query, conn)
        st.dataframe(df_dispo)

# ======================= 4. Ajouter un client =======================
elif menu == "Ajouter un client":
    st.subheader("➕ Ajouter un nouveau client")

    nom = st.text_input("Nom complet")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville", value="Paris")
    code_postal = st.number_input("Code postal", step=1)
    email = st.text_input("Email")
    tel = st.text_input("Téléphone")

    if st.button("Ajouter le client"):
        try:
            c.execute("""
                INSERT INTO Client (adresse, ville, codePostal, email, telephone, nomComplet)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (adresse, ville, code_postal, email, tel, nom))
            conn.commit()
            st.success("✅ Client ajouté avec succès.")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")

# ======================= 5. Ajouter une réservation =======================
elif menu == "Ajouter une réservation":
    st.subheader("📅 Ajouter une réservation")

    client_id = st.number_input("ID du client", step=1)
    chambre_id = st.number_input("ID de la chambre", step=1)
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")

    if st.button("Ajouter la réservation"):
        try:
            c.execute("""
                INSERT INTO Reservation (dateDebut, dateFin, idClient, idChambre)
                VALUES (?, ?, ?, ?)
            """, (date_debut, date_fin, client_id, chambre_id))
            conn.commit()
            st.success("✅ Réservation ajoutée avec succès.")
        except Exception as e:
            st.error(f"❌ Erreur : {e}")

# Fermer la connexion à la base de données
conn.close()
