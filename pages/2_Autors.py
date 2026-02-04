import streamlit as st
import sqlite3
import pandas as pd


conn = sqlite3.connect("./dat/DistLlibres.db")
c = conn.cursor()

# --- Funcions auxiliars ---
def get_data(query):
    return pd.read_sql_query(query, conn)

def insert_data(query, values):
    c.execute(query, values)
    conn.commit()

# --- Interfície Streamlit ---
st.title("📚 Gestió de Llibreria")
st.set_page_config(page_title="Autors", page_icon="📈")

st.markdown("# Autors")

st.header("Autors")
tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])


# --- Alta ---
with tab1:
    with st.form("form_autor_alta"):
        nom = st.text_input("Nom")
        cognoms = st.text_input("Cognoms")
        telefon = st.text_input("Telèfon")
        pais = st.text_input("País")
        submit = st.form_submit_button("Afegir")
        if submit:
            insert_data("INSERT INTO Autors (nom_autor, cognoms, telefon, pais) VALUES (?, ?, ?, ?)",
                        (nom, cognoms, telefon, pais))
            st.success("Autor afegit ✅")

# --- Baixa ---
with tab2:
    autors = get_data("SELECT * FROM Autors")
    opcions = [f"{row['id_autor']} - {row['nom_autor']} {row['cognoms']}" for _, row in autors.iterrows()]
    seleccio = st.selectbox("Selecciona Autor per eliminar", opcions, key="selectbox_baixa_autor")
    if st.button("Eliminar"):
        id_baixa = int(seleccio.split(" - ")[0])  # extreure l'ID
        insert_data("DELETE FROM Autors WHERE id_autor = ?", (id_baixa,))
        st.success(f"Autor {seleccio} eliminat ✅")

# --- Modificar ---
with tab3:

    autors = get_data("SELECT * FROM Autors")
    opcions = [f"{row['id_autor']} - {row['nom_autor']} {row['cognoms']}" for _, row in autors.iterrows()]
    seleccio = st.selectbox("Selecciona Autor per modificar", opcions, key="selectbox_modificar_autor")
    
    # extreure ID i dades actuals
    id_mod = int(seleccio.split(" - ")[0])
    autor_seleccionat = autors.loc[autors['id_autor'] == id_mod].iloc[0]

    st.write(f"Autor seleccionat: **{id_mod} - {autor_seleccionat['nom_autor']} {autor_seleccionat['cognoms']}**")

    # Inputs amb valors actuals
    nou_nom = st.text_input("Nou nom", value=autor_seleccionat['nom_autor'])
    nous_cognoms = st.text_input("Nous cognoms", value=autor_seleccionat['cognoms'])
    nou_telefon = st.text_input("Nou telèfon", value=autor_seleccionat['telefon'])
    nou_pais = st.text_input("Nou país", value=autor_seleccionat['pais'])

    if st.button("Modificar"):
        insert_data(
            "UPDATE Autors SET nom_autor = ?, cognoms = ?, telefon = ?, pais = ? WHERE id_autor = ?",
            (nou_nom, nous_cognoms, nou_telefon, nou_pais, id_mod)
        )
        st.success(f"Autor {id_mod} modificat ✅")


# --- Consulta ---
with tab4:
    datos = get_data("SELECT * FROM Autors")
    st.dataframe(datos)
