import streamlit as st
import sqlite3
import pandas as pd


conn = sqlite3.connect("./dat/DistLlibres.db")
c = conn.cursor()

# -----------------------------------------------------------------------Funcions auxiliars ---
def get_data(query):
    return pd.read_sql_query(query, conn)

def insert_data(query, values):
    c.execute(query, values)
    conn.commit()

# -------------------------------------------------------------------------Interfície Streamlit ---
st.title("📚 Gestió de Llibreria")
st.set_page_config(page_title="Autors", page_icon="📈")

st.markdown("# Llibres")
st.sidebar.header("Llibres")

st.header("Llibres")
tab1, tab2, tab3, tab4 = st.tabs(["➕ Alta", "🗑️ Baixa", "✏️ Modificar", "🔍 Consulta"])

# -------------------------------------------------------------------------------------Alta ---
with tab1:
    with st.form("form_llibre_alta"):
        titol = st.text_input("Títol")
        idioma = st.selectbox("Idioma", ['cat','cast','ang','fra', 'ita','altres'], index=0)

        # Selectors per claus externes amb placeholder
        autors = get_data("SELECT * FROM Autors")
        opcions_autors = ["-- Selecciona Autor --"] + [
            f"{row['id_autor']} - {row['nom_autor']} {row['cognoms']}" for _, row in autors.iterrows()
        ]
        seleccio_autor = st.selectbox("Autor", opcions_autors, index=0)
        id_autor = None if seleccio_autor == "-- Selecciona Autor --" else int(seleccio_autor.split(" - ")[0])

        editorials = get_data("SELECT * FROM Editorials")
        opcions_editorials = ["-- Selecciona Editorial --"] + [
            f"{row['id_editorial']} - {row['nom_editorial']}" for _, row in editorials.iterrows()
        ]
        seleccio_editorial = st.selectbox("Editorial", opcions_editorials, index=0)
        id_editorial = None if seleccio_editorial == "-- Selecciona Editorial --" else int(seleccio_editorial.split(" - ")[0])

        categories = get_data("SELECT * FROM Categories")
        opcions_categories = ["-- Selecciona Categoria --"] + [
            f"{row['id_categoria']} - {row['nom_categoria']}" for _, row in categories.iterrows()
        ]
        seleccio_categoria = st.selectbox("Categoria", opcions_categories, index=0)
        id_categoria = None if seleccio_categoria == "-- Selecciona Categoria --" else int(seleccio_categoria.split(" - ")[0])

        stock = st.number_input("Stock", min_value=0, step=1)
        stock_minim = st.number_input("Stock mínim", min_value=0, step=1)

        submit = st.form_submit_button("Afegir")
        if submit:
            if id_autor and id_editorial and id_categoria:
                insert_data(
                    "INSERT INTO Llibres (titol, idioma, id_autor, id_editorial, id_categoria, stock, stock_minim) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (titol, idioma, id_autor, id_editorial, id_categoria, stock, stock_minim)
                )
                st.success("Llibre afegit ✅")
            else:
                st.error("Has de seleccionar Autor, Editorial i Categoria abans d'afegir el llibre.")



# -----------------------------------------------------------------------------------------Baixa ---
with tab2:
    llibres = get_data("SELECT * FROM Llibres")
    opcions = ["-- Selecciona Llibre --"] + [
        f"{row['id_llibre']} - {row['titol']}" for _, row in llibres.iterrows()
    ]
    seleccio = st.selectbox("Selecciona Llibre per eliminar", opcions, index=0, key="selectbox_baixa_llibre")

    if st.button("Eliminar"):
        if seleccio == "-- Selecciona Llibre --":
            st.error("Has de seleccionar un llibre abans d'eliminar.")
        else:
            id_baixa = int(seleccio.split(" - ")[0])
            insert_data("DELETE FROM Llibres WHERE id_llibre = ?", (id_baixa,))
            st.success(f"Llibre {seleccio} eliminat ✅")

# --------------------------------------------------------------------------------------Modificar ---
with tab3:
    #llibre_seleccionat = None
    llibres = get_data("SELECT * FROM Llibres")
    opcions = ["-- Selecciona Llibre --"] + [
        f"{row['id_llibre']} - {row['titol']}" for _, row in llibres.iterrows()
    ]
    seleccio = st.selectbox("Selecciona Llibre per modificar", opcions, index=0, key="selectbox_modificar_llibre")

    if seleccio == "-- Selecciona Llibre --":
        st.info("Selecciona un llibre per poder modificar les dades.")
        llibre_seleccionat = 0
    else:
        id_mod = int(seleccio.split(" - ")[0])
        llibre_seleccionat = llibres.loc[llibres['id_llibre'] == id_mod].iloc[0]

        st.write(f"Llibre seleccionat: **{id_mod} - {llibre_seleccionat['titol']}**")

        mod_titol = st.text_input("Títol", value=llibre_seleccionat['titol'])
        mod_idioma = st.selectbox("Idioma", ['cat','cast','ang','fra', 'ita','altres'], index=0)
        mod_stock = st.number_input("Stock", min_value=0, step=1, value=int(llibre_seleccionat['stock']))
        mod_stock_minim = st.number_input("Stock mínim", min_value=0, step=1, value=int(llibre_seleccionat['stock_minim']))

        # Selectors amb valor actual
        seleccio_autor = st.selectbox(
            "Autor",
            [f"{row['id_autor']} - {row['nom_autor']} {row['cognoms']}" for _, row in autors.iterrows()],
            index=list(autors['id_autor']).index(llibre_seleccionat['id_autor'])
        )
        mod_id_autor = int(seleccio_autor.split(" - ")[0])

        seleccio_editorial = st.selectbox(
            "Editorial",
            [f"{row['id_editorial']} - {row['nom_editorial']}" for _, row in editorials.iterrows()],
            index=list(editorials['id_editorial']).index(llibre_seleccionat['id_editorial'])
        )
        mod_id_editorial = int(seleccio_editorial.split(" - ")[0])

        seleccio_categoria = st.selectbox(
            "Categoria",
            [f"{row['id_categoria']} - {row['nom_categoria']}" for _, row in categories.iterrows()],
            index=list(categories['id_categoria']).index(llibre_seleccionat['id_categoria'])
        )
        mod_id_categoria = int(seleccio_categoria.split(" - ")[0])

        mod_stock = st.number_input("Nou stock", min_value=0, step=1, value=int(llibre_seleccionat['stock']))
        mod_stock_minim = st.number_input("Nou stock mínim", min_value=0, step=1, value=int(llibre_seleccionat['stock_minim']))

        if st.button("Modificar"):
            insert_data(
                "UPDATE Llibres SET titol = ?, idioma = ?, id_autor = ?, id_editorial = ?, id_categoria = ?, stock = ?, stock_minim = ? WHERE id_llibre = ?",
                (mod_titol, mod_idioma, mod_id_autor, mod_id_editorial, mod_id_categoria, mod_stock, mod_stock_minim, id_mod)
            )
            st.success(f"Llibre {id_mod} modificat ✅")


# --------------------------------------------------------------------------------------Consulta ---
with tab4:
    st.subheader("Llista de Llibres")

    df_llibres = get_data("""
        SELECT 
            L.id_llibre,
            L.titol,
            L.idioma,

            -- Autor complet
            A.nom_autor || ' ' || A.cognoms AS autor,

            -- Editorial
            E.nom_editorial,

            -- Categoria
            C.nom_categoria,

            -- Stock
            L.stock,
            L.stock_minim

        FROM Llibres L
        JOIN Autors A ON L.id_autor = A.id_autor
        JOIN Editorials E ON L.id_editorial = E.id_editorial
        JOIN Categories C ON L.id_categoria = C.id_categoria

        ORDER BY L.id_llibre
    """)

    st.dataframe(df_llibres, use_container_width=True)




