import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(page_title="stadístiques de Comandes", layout="wide")
st.title("📦 Estadístiques de Comandes")

# ---------------------------------------------------------
# CARGA DE DATOS DESDE SQLITE
# ---------------------------------------------------------
@st.cache_data
def cargar_datos():
    con = sqlite3.connect("./dat/DistLlibres.db")

    # Consulta combinada
    query = """
        SELECT 
            c.id_comanda,
            c.data_alta,
            cd.quantitat,
            cd.preu,
            (cd.quantitat * cd.preu) AS import_linia
        FROM Comandes c
        JOIN ComandesDetall cd ON c.id_comanda = cd.id_comanda
    """

    df = pd.read_sql_query(query, con)
    con.close()

    # Convertir fechas
    df["data_alta"] = pd.to_datetime(df["data_alta"])
    df["any"] = df["data_alta"].dt.year
    df["mes"] = df["data_alta"].dt.month
    df["mes_nom"] = df["data_alta"].dt.month_name(locale="es_ES")

    return df

df = cargar_datos()

# ---------------------------------------------------------
# FILTRO POR MES
# ---------------------------------------------------------
st.sidebar.header("Filtros")

meses = df["mes_nom"].unique().tolist()
mes_seleccionado = st.sidebar.selectbox("Selecciona un mes", ["Todos"] + meses)

df_filtrado = df.copy()
if mes_seleccionado != "Todos":
    df_filtrado = df[df["mes_nom"] == mes_seleccionado]

# ---------------------------------------------------------
# AGRUPACIÓN POR MES
# ---------------------------------------------------------
df_mes = df.groupby(["any", "mes", "mes_nom"]).agg(
    pedidos=("id_comanda", "nunique"),
    unidades=("quantitat", "sum"),
    importe=("import_linia", "sum")
).reset_index()

df_mes = df_mes.sort_values(["any", "mes"])

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
st.subheader("📊 Indicadors principals")

total_pedidos = df_filtrado["id_comanda"].nunique()
total_unidades = df_filtrado["quantitat"].sum()
total_importe = df_filtrado["import_linia"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Número de comandes", total_pedidos)
col2.metric("Unitats totals", total_unidades)
col3.metric("Import total (€)", f"{total_importe:,.2f}")

st.divider()

# ---------------------------------------------------------
# GRÁFICO 1: Pedidos por mes
# ---------------------------------------------------------
st.subheader("📈 Comandes per mes-any")

# Crear columna mes-año
df_mes["mes_any"] = df_mes["mes_nom"] + " " + df_mes["any"].astype(str)

fig1 = px.bar(
    df_mes,
    x="mes_any",       # agrupació mes-any
    y="pedidos",
    color="any",       # opcional: manté colors per any
    title="Número de Comandes per mes-any",
    barmode="group"
)

fig1.update_layout(
    xaxis_title="Mes-Any",
    yaxis_title="Número de Comandes",
    legend_title="Any",
    bargap=0.20,
    bargroupgap=0.05
)

st.plotly_chart(fig1, use_container_width=True)


# ---------------------------------------------------------
# GRÁFICO 2: Unidades por mes
# ---------------------------------------------------------
st.subheader("📦 Unitats per mes")

fig2 = px.line(
    df_mes,
    x="mes_nom",
    y="unidades",
    color="any",
    markers=True,
    title="Unitats totals per mes"
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------
# GRÁFICO 3: Importe por mes
# ---------------------------------------------------------
st.subheader("💶 Import total per mes")

fig3 = px.area(
    df_mes,
    x="mes_nom",
    y="importe",
    color="any",
    title="Import total per mes (€)"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------
# TABLA FINAL
# ---------------------------------------------------------
st.subheader("📋 Dades filtrades")
st.dataframe(df_filtrado, use_container_width=True)



# ---------------------------------------------------
# --- GRÀFIC DE TARTA ---
st.subheader("🥧 Estats de les comandes")
con = sqlite3.connect("./dat/DistLlibres.db")

query_estats = """ SELECT nom_estat, COUNT(*) AS total FROM Comandes as c
                    JOIN Estats as e on c.id_estat = e.id_estat
                    GROUP BY c.id_estat ORDER BY c.id_estat """
df_estats = pd.read_sql_query(query_estats, con)

fig = px.pie(
    df_estats,
    names="nom_estat",
    values="total",
    title="Distribució dels estats de les comandes",
)

fig.update_traces(textposition="inside", textinfo="percent+label")

st.plotly_chart(fig, use_container_width=True)

