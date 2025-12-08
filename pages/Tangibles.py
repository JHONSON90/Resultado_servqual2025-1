import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit.elements.lib.layout_utils import Height

st.set_page_config(page_title="Tangibles", layout="wide")

color_map = {
    '5': '#40916c',  # Verde Oscuro (Bootstrap success)
    '4': '#95d5b2',  # Verde Claro
    '3': '#eeef20',  # Amarillo (Bootstrap warning)
    '2': '#ee6055',  # Naranja
    '1': '#bc4b51'
}


df = pl.read_csv("Formatos_Listos/Cuantitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Int64}, ignore_errors=True)
df2 = pl.read_csv("Formatos_Listos/Cualitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.String}, ignore_errors=True)
df3 = pl.read_csv("Formatos_Listos/para_niv_satisfaccion.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Float64}, ignore_errors=True)

st.title(":blue[Tangibles]")

st.text("Cumplimiento del servicio prometido de manera precisa y confiable.")
# 2. Incluir señalización visible que oriente trámites, filas y turnos reduce el estrés y mejora la percepción de orden.  
# 3. Asegurar rampas, pasamanos, zonas para adultos mayores y personas con movilidad reducida.  
# 4. La percepción de higiene tiene alto impacto en la calidad percibida en espacios públicos.  
# 5. Terminales de autoservicio o pantallas informativas pueden mejorar la percepción tecnológica de la entidad.  

# """)

#st.write(df.select("variable").unique())


st.title("Otros")


st.subheader("¿Qué sugerencias tiene para Empopasto?")
pregunta22 = df2.filter(pl.col("variable") == "pregunta22")

sugerencias = pregunta22.select(["value"])

for (row,) in sugerencias.iter_rows():
    st.markdown(f":material/arrow_right: {row}")

