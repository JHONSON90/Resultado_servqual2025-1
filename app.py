import streamlit as st
import polars as pl
import plotly.express as px
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import traceback
import time


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

# Ocultar el menú de navegación superior por defecto de Streamlit
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Agregar logos y menú en la sidebar
st.sidebar.image("assets/empopasto_logo.jpg", width="stretch")
st.sidebar.markdown("---")

# Menú de navegación con iconos profesionales
st.sidebar.page_link("app.py", label="📊 Generalidades")
st.sidebar.page_link("pages/aspectos_generales.py", label="📋 Aspectos Generales")
st.sidebar.page_link("pages/acueducto_alcantarillado.py", label="💧 Acueducto y Alcantarillado")
st.sidebar.page_link("pages/gestion_comunicacion.py", label="📢 Gestión y Comunicación")
st.sidebar.page_link("pages/Conclusiones.py", label="✅ Conclusiones")

st.sidebar.markdown("---")
st.sidebar.image("assets/one_logo.jpg", width=80)

#red, orange, yellow, green, blue, violet, gray/grey, rainbow y primary
st.title(":blue[Generalidades]")

conn = st.connection("gsheets", type=GSheetsConnection)
try:
    df_raw = conn.read(worksheet="Cuantitativas", ttl=0)
    # Convertir pandas DataFrame a Polars DataFrame
    df = pl.from_pandas(df_raw)
    placeholder = st.empty()
    placeholder.success(f"✅ Cuantitativas cargadas ({len(df)} filas)")
    time.sleep(0.5)
    placeholder.empty()
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets (Cuantitativas): {str(e)}")
    st.error(f"Traceback: {traceback.format_exc()}")
    st.stop()  # Detiene la ejecución si falla

try:
    df2_raw = conn.read(worksheet="Cualitativas", ttl=0)
    # Convertir pandas DataFrame a Polars DataFrame
    df2 = pl.from_pandas(df2_raw)
    placeholder = st.empty()
    placeholder.success(f"✅ Cualitativas cargadas ({len(df2)} filas)")
    time.sleep(0.5)
    placeholder.empty()
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets (Cualitativas): {str(e)}")
    st.error(f"Traceback: {traceback.format_exc()}")
    st.stop()

try:
    df3_raw = conn.read(worksheet="Limpia", ttl=0)
    # Convertir pandas DataFrame a Polars DataFrame
    total = pl.from_pandas(df3_raw)
    placeholder = st.empty()
    placeholder.success(f"✅ Respuestas totales cargadas ({len(total)} filas)")
    time.sleep(0.5)
    placeholder.empty()
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets (Respuestas totales): {str(e)}")
    st.error(f"Traceback: {traceback.format_exc()}")
    st.stop()

try:
    df3_raw = conn.read(worksheet="Latitud_longitud", ttl=0)
    # Convertir pandas DataFrame a Polars DataFrame
    longitudes = pl.from_pandas(df3_raw)
    placeholder = st.empty()
    placeholder.success(f"✅ Latitudes y Longitudes cargadas ({len(longitudes)} filas)")
    time.sleep(0.5)
    placeholder.empty()
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets (Latitudes y Longitudes): {str(e)}")
    st.error(f"Traceback: {traceback.format_exc()}")
    st.stop()


st.text("Objetivo: Informar el nivel de satisfacción de los usuarios con los servicios de Empopasto y entregar un análisis completo por dimensión Servqual para orientar acciones de mejora.")

barrios = total.group_by("Barrio").agg(
    pl.len().alias("count")
)

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

st.markdown("""
El estudio se fundamenta en la opinión de 600 usuarios residentes en 107 barrios de la ciudad, seleccionados bajo criterios de aleatoriedad para evitar sesgos geográficos. El perfil demográfico obtenido revela un usuario promedio en edad productiva (30 a 50 años), con una alta sensibilidad hacia el costo y la calidad del servicio debido a su condición socioeconómica. Dado que más del 68% de la muestra pertenece a los estratos Bajo-Bajo, Bajo y Medio-Bajo, sumado a un significativo 22.5% del sector comercial, los resultados aquí presentados constituyen un termómetro fiel de la realidad operativa y social que enfrenta la mayoría de la base de clientes de Empopasto en su día a día.
""")

st.markdown("""
**Criterios de Interpretación de Resultados:** Para el análisis de los indicadores, el estudio adopta una escala de valoración porcentual alineada con las metas institucionales. Los resultados superiores al 90% se clasifican como Excelencia, indicando el cumplimiento pleno de la expectativa del usuario. El rango entre 80% y 89.9% corresponde a un nivel Muy Satisfactorio, reflejando una percepción positiva consolidada. Los valores situados entre 70% y 79.9% se consideran Satisfactorios, aunque evidencian oportunidades de mejora latentes. Finalmente, cualquier indicador inferior al 70% se tipifica como Insatisfactorio o Crítico, señalando una brecha significativa entre el servicio recibido y las necesidades del usuario que requiere intervención inmediata.
""")


