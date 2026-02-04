import streamlit as st
import sqlite3
import pandas as pd

# --- Connexió a la BD SQLite ---
st.set_page_config(page_title="Auxiliars", page_icon="📈")

st.markdown("# Auxiliars")
st.sidebar.header("Auxiliars")
conn = sqlite3.connect("./dat/DistLlibres.db")
c = conn.cursor()

# ------------------------------------------------------------------------------------ Funcions auxiliars ---
def get_data(query):
    return pd.read_sql_query(query, conn)

def insert_data(query, values):
    c.execute(query, values)
    conn.commit()

# ----------------------------------------------------------------------------------- Interfície Streamlit ---
#st.title("📚 Gestió de Llibreria")

menu = st.sidebar.selectbox(
    "Menú",
    [ "Categories",  "Editorials",  "Estats"]
)

# --- ------------------------------------------Pantalla genèrica per Categories (exemple CRUD amb pestanyes) ---
if menu == "Categories":
    st.header("Categories")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])

    # --- Alta ---
    with tab1:
        with st.form("form_categoria_alta"):
            nom = st.text_input("Nom Categoria")
            submit = st.form_submit_button("Afegir")
            if submit:
                insert_data("INSERT INTO Categories (nom_categoria) VALUES (?)", (nom,))
                st.success("Categoria afegida ✅")

    # --- Baixa ---
    with tab2:
        categories = get_data("SELECT * FROM Categories")
        opcions = [f"{row['id_categoria']} - {row['nom_categoria']}" for _, row in categories.iterrows()]
        seleccio = st.selectbox("Selecciona Categoria per eliminar", opcions, key="selectbox_baixa")
        if st.button("Eliminar"):
            id_baixa = int(seleccio.split(" - ")[0])  # extreure l'ID
            insert_data("DELETE FROM Categories WHERE id_categoria = ?", (id_baixa,))
            st.success(f"Categoria {seleccio} eliminada ✅")

    # --- Modificar ---
    with tab3:
        categories = get_data("SELECT * FROM Categories")
        opcions = [f"{row['id_categoria']} - {row['nom_categoria']}" for _, row in categories.iterrows()]
        seleccio = st.selectbox("Selecciona Categoria per modificar", opcions, key="selectbox_modificar")
        id_mod = int(seleccio.split(" - ")[0])
        nom_actual = seleccio.split(" - ")[1]
        st.write(f"Categoria seleccionada: **{id_mod} - {nom_actual}**")
        nou_nom = st.text_input("Nou nom de la categoria", value=nom_actual)
        if st.button("Modificar"):
            insert_data("UPDATE Categories SET nom_categoria = ? WHERE id_categoria = ?", (nou_nom, id_mod))
            st.success(f"Categoria {id_mod} modificada ✅")

    # --- Consulta ---
    with tab4:
        st.subheader("Llista de Categories")
        st.dataframe(get_data("SELECT * FROM Categories"))

   

       
#--------------------------------------------------------------------Pantalla genèrica per Editorials---------
if menu == "Editorials":
    st.header("Editorials")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])

    # --- Alta ---
    with tab1:
        with st.form("form_editorial_alta"):
            nom = st.text_input("Nom Editorial")
            submit = st.form_submit_button("Afegir")
            if submit:
                insert_data("INSERT INTO Editorials (nom_editorial) VALUES (?)", (nom,))
                st.success("Editorial afegida ✅")

    # --- Baixa ---
    with tab2:
        editorials = get_data("SELECT * FROM Editorials")
        opcions = [f"{row['id_editorial']} - {row['nom_editorial']}" for _, row in editorials.iterrows()]
        seleccio = st.selectbox("Selecciona Editorial per eliminar", opcions, key="selectbox_baixa_editorial")
        if st.button("Eliminar"):
            id_baixa = int(seleccio.split(" - ")[0])  # extreure l'ID
            insert_data("DELETE FROM Editorials WHERE id_editorial = ?", (id_baixa,))
            st.success(f"Editorial {seleccio} eliminada ✅")

    # --- Modificar ---
    with tab3:
        editorials = get_data("SELECT * FROM Editorials")
        opcions = [f"{row['id_editorial']} - {row['nom_editorial']}" for _, row in editorials.iterrows()]
        seleccio = st.selectbox("Selecciona Editorial per modificar", opcions, key="selectbox_modificar_editorial")
        id_mod = int(seleccio.split(" - ")[0])
        nom_actual = seleccio.split(" - ")[1]
        st.write(f"Editorial seleccionada: **{id_mod} - {nom_actual}**")
        nou_nom = st.text_input("Nou nom de l'editorial", value=nom_actual)
        if st.button("Modificar"):
            insert_data("UPDATE Editorials SET nom_editorial = ? WHERE id_editorial = ?", (nou_nom, id_mod))
            st.success(f"Editorial {id_mod} modificada ✅")

    # --- Consulta ---
    with tab4:
        st.subheader("Llista d'Editorials")
        st.dataframe(get_data("SELECT * FROM Editorials"))
       

# -----------------------------------------------------------------Pantalla genèrica per Estats------------- 
if menu == "Estats":
    st.header("Estats")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])

    # --- Alta ---
    with tab1:
        with st.form("form_estat_alta"):
            nom = st.text_input("Nom Estat")
            submit = st.form_submit_button("Afegir")
            if submit:
                insert_data("INSERT INTO Estats (nom_estat) VALUES (?)", (nom,))
                st.success("Estat afegit ✅")

    # --- Baixa ---
    with tab2:
        estats = get_data("SELECT * FROM Estats")
        opcions = ["-- Selecciona Estat --"] + [
            f"{row['id_estat']} - {row['nom_estat']}" for _, row in estats.iterrows()
        ]
        seleccio = st.selectbox("Selecciona Estat per eliminar", opcions, index=0, key="selectbox_baixa_estat")
        if st.button("Eliminar"):
            if seleccio == "-- Selecciona Estat --":
                st.error("Has de seleccionar un estat abans d'eliminar.")
            else:
                id_baixa = int(seleccio.split(" - ")[0])
                insert_data("DELETE FROM Estats WHERE id_estat = ?", (id_baixa,))
                st.success(f"Estat {seleccio} eliminat ✅")

    # --- Modificar ---
    with tab3:
        estats = get_data("SELECT * FROM Estats")
        opcions = ["-- Selecciona Estat --"] + [
            f"{row['id_estat']} - {row['nom_estat']}" for _, row in estats.iterrows()
        ]
        seleccio = st.selectbox("Selecciona Estat per modificar", opcions, index=0, key="selectbox_modificar_estat")

        if seleccio != "-- Selecciona Estat --":
            id_mod = int(seleccio.split(" - ")[0])
            nom_actual = seleccio.split(" - ")[1]
            st.write(f"Estat seleccionat: **{id_mod} - {nom_actual}**")
            nou_nom = st.text_input("Nou nom de l'estat", value=nom_actual)
            if st.button("Modificar"):
                insert_data("UPDATE Estats SET nom_estat = ? WHERE id_estat = ?", (nou_nom, id_mod))
                st.success(f"Estat {id_mod} modificat ✅")
        else:
            st.info("Selecciona un estat per poder modificar les dades.")

    # --- Consulta ---
    with tab4:
        st.subheader("Llista d'Estats")
        st.dataframe(get_data("SELECT * FROM Estats"))

        

        

