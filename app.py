import streamlit as st
import polars as pl
import plotly.express as px

MI_ESCALA = [
    (0.0,   "#8B0000"),   # rojo muy oscuro → peor
    (0.2,   "#CC0000"),
    (0.35,  "#FF4444"),
    (0.5,   "#FFD700"),   # amarillo neutro
    (0.65,  "#99EE99"),
    (0.8,   "#228B22"),
    (1.0,   "#006400")    # verde muy oscuro → mejor
]

# ACTIVAR GLOBALMENTE (ahora sí funciona sin errores)
px.defaults.color_continuous_scale = MI_ESCALA
#px.defaults.color_discrete_sequence = px.colors.sample_colorscale(MI_ESCALA, 20)


st.set_page_config(page_title="Encuestas Empopasto", layout="wide")
st.sidebar.page_link("app.py", label="Generalidades")
st.sidebar.page_link("pages/Cap_Respuesta.py", label="Capacidad de Respuesta")

#red, orange, yellow, green, blue, violet, gray/grey, rainbow y primary
st.title(":blue[Generalidades]")
st.text("Objetivo: Informar el nivel de satisfacción de los usuarios con los servicios de Empopasto y entregar un análisis completo por dimensión Servqual para orientar acciones de mejora.")
total = pl.read_csv("Data/Encuestas_ONE - Limpia.csv", separator=",", encoding="utf-8")
df = pl.read_csv("Formatos_Listos/Cuantitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Int64}, ignore_errors=True)
df2 = pl.read_csv("Formatos_Listos/Cualitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.String}, ignore_errors=True)

barrios = total.group_by("Barrio").agg(
    pl.len().alias("count")
)
longitudes = pl.read_excel("Data/Latitud y longitud.xlsx")

barrios = barrios.join(longitudes, left_on="Barrio", right_on="Barrio / Sector", how="left")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric("Total de encuestas", total.shape[0], border=True)

with metric2:
    st.metric("Barrios Consultados", barrios.shape[0], border=True)

with metric3:
    st.metric("Comercial", 135, border=True)

with metric4:
    st.metric("Residencial", 465, border=True)

st.subheader("Mapa de Barrios")
fig = px.scatter_map(barrios, lat="Latitud", lon="Longitud", size="count", zoom=11.9, height=700)
st.plotly_chart(fig, theme="streamlit")

#st.map(barrios, lat="Latitud", lon="Longitud", size="count", zoom=11.9, height=700)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Edades")
    edades = total.select("Edad").filter(pl.col("Edad") > 0).cast(pl.Int64)
    edades = edades.group_by("Edad").agg(
        pl.len().alias("count")
    )
    fig = px.histogram(edades, x="Edad", y="count", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, theme="streamlit", width="stretch")

with col4:
    st.subheader("Estratos")
    estratos = total.select(["Subcategoria",  "Desc Subcategoria"])
    estratos = estratos.group_by("Desc Subcategoria").agg(
        pl.len().alias("count")
    )
    fig = px.pie(estratos, names="Desc Subcategoria", values="count", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

