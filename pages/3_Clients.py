import streamlit as st
import sqlite3
import pandas as pd

# --- Connexió a la BD SQLite ---

conn = sqlite3.connect("./dat/DistLlibres.db")
c = conn.cursor()

# --- Funcions auxiliars ---
def get_data(query):
    return pd.read_sql_query(query, conn)

def insert_data(query, values):
    c.execute(query, values)
    conn.commit()

st.set_page_config(page_title="Clients", page_icon="📈")

st.markdown("# Clients")
st.sidebar.header("Clients")

st.header("Clients")
tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])

# --- Alta ---
with tab1:
    with st.form("form_client_alta"):
        nom = st.text_input("Nom")
        cognoms = st.text_input("Cognoms")
        adressa = st.text_input("Adreça")
        correu = st.text_input("Correu electrònic")
        telefon = st.text_input("Telèfon")
        submit = st.form_submit_button("Afegir")
        if submit:
            insert_data(
                "INSERT INTO Clients (nom_client, cognoms, adressa, correu, telefon) VALUES (?, ?, ?, ?, ?)",
                (nom, cognoms, adressa, correu, telefon)
            )
            st.success("Client afegit ✅")

# --- Baixa ---
with tab2:
    clients = get_data("SELECT * FROM Clients")
    opcions = [f"{row['id_client']} - {row['nom_client']} {row['cognoms']}" for _, row in clients.iterrows()]
    seleccio = st.selectbox("Selecciona Client per eliminar", opcions, key="selectbox_baixa_client")
    if st.button("Eliminar"):
        id_baixa = int(seleccio.split(" - ")[0])  # extreure l'ID
        insert_data("DELETE FROM Clients WHERE id_client = ?", (id_baixa,))
        st.success(f"Client {seleccio} eliminat ✅")

# --- Modificar ---
with tab3:
    clients = get_data("SELECT * FROM Clients")
    opcions = [f"{row['id_client']} - {row['nom_client']} {row['cognoms']}" for _, row in clients.iterrows()]
    seleccio = st.selectbox("Selecciona Client per modificar", opcions, key="selectbox_modificar_client")
    id_mod = int(seleccio.split(" - ")[0])
    client_seleccionat = clients.loc[clients['id_client'] == id_mod].iloc[0]

    st.write(f"Client seleccionat: **{id_mod} - {client_seleccionat['nom_client']} {client_seleccionat['cognoms']}**")

    nou_nom = st.text_input("Nou nom", value=client_seleccionat['nom_client'])
    nous_cognoms = st.text_input("Nous cognoms", value=client_seleccionat['cognoms'])
    nova_adressa = st.text_input("Nova adreça", value=client_seleccionat['adressa'])
    nou_correu = st.text_input("Nou correu electrònic", value=client_seleccionat['correu'])
    nou_telefon = st.text_input("Nou telèfon", value=client_seleccionat['telefon'])

    if st.button("Modificar"):
        insert_data(
            "UPDATE Clients SET nom_client = ?, cognoms = ?, adressa = ?, correu = ?, telefon = ? WHERE id_client = ?",
            (nou_nom, nous_cognoms, nova_adressa, nou_correu, nou_telefon, id_mod)
        )
        st.success(f"Client {id_mod} modificat ✅")

# --- Consulta ---
with tab4:
    st.subheader("Llista de Clients")
    st.dataframe(get_data("SELECT * FROM Clients"))
