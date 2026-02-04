import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- Connexió a la BD SQLite ---

conn = sqlite3.connect("./dat/DistLlibres.db")
c = conn.cursor()

# --- Funcions auxiliars ---
def get_data(query):
    return pd.read_sql_query(query, conn)

def insert_data(query, values):
    c.execute(query, values)
    conn.commit()

st.set_page_config(page_title="Comandes", page_icon="📈")

st.markdown("# Comandes")
st.sidebar.header("Comandes")
tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])

# --- Alta ---
with tab1:
    st.subheader("Crear nova comanda")
    with st.form("form_comanda_alta"):
        # Selecció de client
        clients = get_data("SELECT * FROM Clients")
        opcions_clients = ["-- Selecciona Client --"] + [
            f"{row['id_client']} - {row['nom_client']} {row['cognoms']}" for _, row in clients.iterrows()
        ]
        seleccio_client = st.selectbox("Client", opcions_clients, index=0)
        id_client = None if seleccio_client == "-- Selecciona Client --" else int(seleccio_client.split(" - ")[0])

        # Dates
        data_alta = st.date_input("Data alta", value=date.today())
        data_estat = st.date_input("Data estat", value=date.today())

        # Estat
        estats = get_data("SELECT * FROM Estats")
        opcions_estats = ["-- Selecciona Estat --"] + [
            f"{row['id_estat']} - {row['nom_estat']}" for _, row in estats.iterrows()
        ]
        seleccio_estat = st.selectbox("Estat", opcions_estats, index=0)
        id_estat = None if seleccio_estat == "-- Selecciona Estat --" else int(seleccio_estat.split(" - ")[0])

        submit = st.form_submit_button("Crear Comanda")
        if submit:
            if id_client and id_estat:
                insert_data(
                    "INSERT INTO Comandes (id_client, data_alta, data_estat, id_estat) VALUES (?, ?, ?, ?)",
                    (id_client, data_alta, data_estat, id_estat)
                )
                st.success("Comanda creada ✅")
            else:
                st.error("Has de seleccionar Client i Estat.")

    st.subheader("Afegir línies de detall")
    comandes = get_data("SELECT * FROM Comandes")
    opcions_comandes = ["-- Selecciona Comanda --"] + [
        f"{row['id_comanda']}" for _, row in comandes.iterrows()
    ]
    seleccio_comanda = st.selectbox("Comanda", opcions_comandes, index=0, key="selectbox_comanda_detall")
    if seleccio_comanda != "-- Selecciona Comanda --":
        id_comanda = int(seleccio_comanda)
        with st.form("form_detall_alta"):
            llibres = get_data("SELECT * FROM Llibres")
            opcions_llibre = ["-- Selecciona Llibre --"] + [
                f"{row['id_llibre']} - {row['titol']}" for _, row in llibres.iterrows()
            ]
            seleccio_llibre = st.selectbox("Llibre", opcions_llibre, index=0)
            id_llibre = None if seleccio_llibre == "-- Selecciona Llibre --" else int(seleccio_llibre.split(" - ")[0])

            quantitat = st.number_input("Quantitat", min_value=1, step=1)
            preu = st.number_input("Preu unitari", min_value=0.0, step=0.1)

            submit_detall = st.form_submit_button("Afegir línia")
            if submit_detall and id_llibre:
                # Calcular id_linia (última +1)
                max_linia = get_data(f"SELECT COALESCE(MAX(id_linia),0)+1 as next FROM ComandesDetall WHERE id_comanda={id_comanda}")
                id_linia = int(max_linia.iloc[0]['next'])
                insert_data(
                    "INSERT INTO ComandesDetall (id_comanda, id_linia, id_llibre, quantitat, preu) VALUES (?, ?, ?, ?, ?)",
                    (id_comanda, id_linia, id_llibre, quantitat, preu)
                )
                st.success("Línia afegida ✅")
            #---- Mostra línies detall
        st.subheader("Línies")
        df_detall = get_data(f"""SELECT CD.id_comanda, 
                   L.titol, CD.quantitat, CD.preu 
            FROM ComandesDetall as CD 
            JOIN Llibres as L ON CD.id_llibre = L.id_llibre
            WHERE CD.id_comanda = {seleccio_comanda} 
            ORDER BY CD.id_comanda, CD.id_linia""")

        st.dataframe(df_detall, use_container_width=True, hide_index=True)

# --- Baixa ---
with tab2:
    st.header("Eliminar Comanda")

    # Ara recuperem també el nom del client
    comandes = get_data("""
        SELECT C.id_comanda, C.id_client, CL.nom_client
        FROM Comandes C
        JOIN Clients CL ON C.id_client = CL.id_client
    """)

    opcions = ["-- Selecciona Comanda --"] + [
        f"{row['id_comanda']} - {row['nom_client']} (ID client: {row['id_client']})"
        for _, row in comandes.iterrows()
    ]

    seleccio = st.selectbox(
        "Selecciona Comanda per eliminar",
        opcions,
        index=0,
        key="selectbox_baixa_comanda"
    )

    if st.button("Eliminar Comanda"):
        if seleccio == "-- Selecciona Comanda --":
            st.error("Has de seleccionar una comanda.")
        else:
            # Extreiem l'id de la comanda (primer element abans del primer " - ")
            id_baixa = int(seleccio.split(" - ")[0])

            insert_data("DELETE FROM ComandesDetall WHERE id_comanda = ?", (id_baixa,))
            insert_data("DELETE FROM Comandes WHERE id_comanda = ?", (id_baixa,))

            st.success(f"Comanda {seleccio} eliminada ✅")


# --- Modificar ---
with tab3:
    comandes = get_data("SELECT * FROM Comandes")
    opcions = ["-- Selecciona Comanda --"] + [
        f"{row['id_comanda']} - Client {row['id_client']}" for _, row in comandes.iterrows()
    ]
    seleccio = st.selectbox("Selecciona Comanda per modificar", opcions, index=0, key="selectbox_modificar_comanda")
    if seleccio != "-- Selecciona Comanda --":
        id_mod = int(seleccio.split(" - ")[0])
        comanda = comandes.loc[comandes['id_comanda'] == id_mod].iloc[0]

        nou_data_estat = st.date_input("Nova data estat", value=pd.to_datetime(comanda['data_estat']).date())
        estats = get_data("SELECT * FROM Estats")
        opcions_estats = [f"{row['id_estat']} - {row['nom_estat']}" for _, row in estats.iterrows()]
        seleccio_estat = st.selectbox("Nou estat", opcions_estats)
        nou_id_estat = int(seleccio_estat.split(" - ")[0])

        if st.button("Modificar Comanda"):
            insert_data(
                "UPDATE Comandes SET data_estat = ?, id_estat = ? WHERE id_comanda = ?",
                (nou_data_estat, nou_id_estat, id_mod)
            )
            st.success(f"Comanda {id_mod} modificada ✅")

# --- Consulta ---
with tab4:
    st.subheader("Llista de Comandes amb detall filtrat")

    df_comandes = get_data("""
        SELECT C.id_comanda,
               C.data_alta,
               CL.nom_client,
               E.nom_estat
        FROM Comandes C
        JOIN Clients CL ON C.id_client = CL.id_client
        JOIN Estats E ON C.id_estat = E.id_estat
        ORDER BY C.id_comanda
    """)

    st.dataframe(df_comandes, use_container_width=True, hide_index = True)
    

    # Selector de comanda
    id_seleccionada = st.selectbox(
        "Selecciona una comanda per veure el detall:",
        df_comandes["id_comanda"]
    )

    if id_seleccionada:
        # Accordion / Expander
        with st.expander(f"Detall de la Comanda {id_seleccionada}", expanded=True):
            df_detall = get_data(f""" SELECT CD.id_comanda, CD.id_linia, L.titol, CD.quantitat,
                                CD.preu FROM ComandesDetall as CD JOIN Llibres as L
                                ON CD.id_llibre = L.id_llibre
                                WHERE CD.id_comanda = {id_seleccionada}
                                ORDER BY CD.id_linia """)
            st.dataframe(df_detall, use_container_width=True, hide_index = True)
