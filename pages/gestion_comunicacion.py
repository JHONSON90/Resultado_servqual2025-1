from turtle import width
import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import traceback
import time

# Ocultar el menú de navegación superior por defecto de Streamlit
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

conn = st.connection("gsheets", type=GSheetsConnection)

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
    df3_raw = conn.read(worksheet="Nivel_Satisfaccion", ttl=0)
    # Convertir pandas DataFrame a Polars DataFrame
    df3 = pl.from_pandas(df3_raw)
    placeholder = st.empty()
    placeholder.success(f"✅ Nivel de Satisfacción cargado ({len(df3)} filas)")
    time.sleep(0.5)
    placeholder.empty()
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets (Nivel_Satisfaccion): {str(e)}")
    st.error(f"Traceback: {traceback.format_exc()}")
    st.stop()


st.title(":blue[Gestion y Comunicacion]")

st.subheader("¿Cómo califica usted las actividades que realiza Empopasto de carácter social y ambiental, que benefician y mejoran la calidad de vida de la comunidad?")

p20_ns = df3.filter(pl.col("variable") == "pregunta20")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p20_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#8B0000","#FFD700","#006400"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
)
    st.plotly_chart(fig, theme="streamlit", width="stretch")

with col2:
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""El indicador de actividades sociales y ambientales presenta un desempeño muy favorable, con una mejora sostenida en los últimos tres años y alcanzando 83,47% en 2025, un resultado que se considera muy satisfactorio dentro de la metodología SERVQUAL.  
    Esta tendencia positiva indica que la empresa:  
    :material/arrow_right: Está fortaleciendo su relación con la comunidad,  
    :material/arrow_right: Está ampliando la efectividad de sus programas sociales y ambientales,  
    :material/arrow_right: Está logrando consolidar una percepción cada vez más favorable respecto a su compromiso social.
""")

col1, col2, col3 = st.columns(3)
with col1:
    pregunta22 = df.filter(pl.col("variable") == "pregunta20")
    pregunta22 = pregunta22.group_by(["Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
        pl.len().alias("count")
    ).filter(pl.col("value") != 0).sort("count", descending=True)

    fig = px.pie(pregunta22, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
with col2:
    fig = px.bar(pregunta22, color="Desc Subcategoria", y="count", x="value", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por Estrato")
    st.plotly_chart(fig, width="stretch")
    
with col3:
    grafico3 = pregunta22.filter(pl.col("value") < 3)
    fig = px.bar(grafico3, y="Barrio", x="count", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas bajas por Barrio")
    st.plotly_chart(fig, width="stretch")

st.markdown("""
El :blue[88.5%] de los usuarios encuestados se declara satisfecho o muy satisfecho con los programas sociales y ambientales desarrollados por EMPOPASTO.  
Esto indica que, en general, la entidad está cumpliendo con sus objetivos en materia de responsabilidad social, educación ambiental y vinculación comunitaria.  
**Dentro del grupo que se muestra satisfecho, la mayor parte de la población corresponde a:**  
    :material/arrow_right: Estrato Bajo: 26,5 %  
    :material/arrow_right: Estrato Único (Comercial): 23,8 %  
    :material/arrow_right: Estrato Medio-Bajo: 23,3 %  
    :material/arrow_right: Estrato Bajo-Bajo: 18,3 %  
Esto demuestra que las iniciativas sociales y ambientales llegan de manera efectiva a los usuarios de menor estrato, que suelen ser quienes más participan en programas comunitarios y acciones educativas.

El :red[11.5%] de los usuarios no está satisfecho con los programas sociales y ambientales.  
Este grupo representa casi una cuarta parte de la población, lo cual sugiere que, si bien los programas son valorados, todavía existe una brecha importante en la percepción de impacto, la cobertura en comunidades y la comunicación de resultados.  
Los barrios con mayor presencia dentro del grupo no satisfecho son Agualongo,  Altos de la colina, La Cruz, La Colina, y otros barrios residenciales con condiciones socioeconómicas similares.  
Estos barrios coinciden con zonas donde, en otras preguntas, ya se observaron inconformidades relacionadas con presión, continuidad o afectaciones por trabajos, lo que indica que la percepción social también se afecta por experiencias negativas en el servicio técnico u operativo.

""")

st.markdown("### ¿Cómo considera usted la gestión actual de EMPOPASTO?")

p21_ns = df3.filter(pl.col("variable") == "pregunta21")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p21_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=480)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
)
    st.plotly_chart(fig, theme="streamlit", width="stretch")

with col2:
    with st.container(
        height=480, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""La valoración de la gestión actual de EMPOPASTO presenta una tendencia creciente en los últimos tres años, pasando de 78,4% a 81,57%.  
    Aunque el indicador continúa en un rango aceptable, la caída acumulada evidencia:  
    :material/arrow_right: Mayor sensibilidad del usuario,  
    :material/arrow_right: Necesidad de fortalecer la comunicación institucional,  
    :material/arrow_right: Atención prioritaria a los barrios críticos,  
    :material/arrow_right: Mejoras urgentes en PQRS y en actividades sociales,  
    :material/arrow_right: Y una estrategia más robusta de presencia comunitaria.     
    Este resultado debe interpretarse como una alerta estratégica, no como una valoración negativa, sino como una oportunidad clara para:  
    :material/arrow_right: reposicionar la gestión,  
    :material/arrow_right: mejorar la confianza ciudadana,  
    :material/arrow_right: priorizar acciones visibles y medibles en el territorio.""")

col1, col2 =st.columns(2)
with col1:
    pregunta21 = df.filter((pl.col("variable") == "pregunta21") & (pl.col("value") != 0))
    pregunta21 = pregunta21.group_by(["Edad", "Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
    pl.len().alias("count")
    ).sort("count", descending=True)

    fig = px.pie(pregunta21, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
    
    pregunta21 = pregunta21.filter(pl.col("value") < 3)
    pregunta21_edad = pregunta21.filter(pl.col("Edad") > 10)

    fig2 = px.histogram(pregunta21_edad, x="Edad", y="count", color="value", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Resultados Bajos por edad")
    st.plotly_chart(fig2)
with col2:
    fig3 = px.bar(pregunta21_edad, x="Desc Subcategoria", y="count", color="value", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Resultados bajos por estrato")
    st.plotly_chart(fig3)
    fig4 = px.bar(pregunta21_edad, x="Barrio", y="count", color="value", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Resultados bajos por barrio")
    st.plotly_chart(fig4)

total_indice = df.filter((pl.col("variable") == "pregunta21")& (pl.col("value") != 0))
total_indice = total_indice.group_by("value").agg(
    pl.len().alias("count")
).sort("count", descending=True)

total_indice = total_indice.with_columns(
    (
        pl.col("count") / pl.col("count").sum()
    ).cast(pl.Float64).round(2).alias("Porcentaje")
)

indice = (442/600)*100

st.markdown("""
La percepción de la gestión actual de EMPOPASTO muestra una evolución positiva, alcanzando en 2025 su mejor valoración con un 81,57%, lo que representa una mejora notable frente a los niveles de 2023 y 2024.  
Esta progresión indica que la ciudadanía reconoce avances en los procesos, la comunicación institucional, las actividades sociales y la operación del servicio.  
Sin embargo, persisten desafíos que deben atenderse para fortalecer aún más la relación empresa–comunidad, especialmente en:  
    :material/arrow_right: mejorar la trazabilidad y respuesta de PQRS,  
    :material/arrow_right: mantener presencia territorial constante,  
    :material/arrow_right: seguir fortaleciendo canales de comunicación,  
    :material/arrow_right: intervenir barrios críticos que afectan la percepción global.  

Entre quienes evaluaron negativamente la gestión, se identifican patrones claros:  
    :material/arrow_right: Estrato Bajo: 40%  
    :material/arrow_right: Estrato Comercial: 33.3%    
    :material/arrow_right: Estrato Medio-Bajo: 13.3%  

Esto indica que la percepción negativa está más marcada en usuarios con:  
    :material/arrow_right: mayor uso de servicio presencial  
    :material/arrow_right: menor acceso a información digital  
    :material/arrow_right: mayor sensibilidad frente a interrupciones o afectaciones  

En cuanto a la edad:  
    :material/arrow_right: 50–60 años: 26.6%  
    :material/arrow_right: 36–45 años: 19.97%  
Estos grupos suelen tener mayores expectativas sobre continuidad, claridad en información y atención personalizada.  

Los barrios donde se concentra la insatisfacción son:  
    :material/arrow_right: Agualongo (20 %)  
    :material/arrow_right: Atahualpa (13.3 %)  
    :material/arrow_right: Granada  
    :material/arrow_right: El Tejar  
    :material/arrow_right: Carlos Pizarro  
    :material/arrow_right: San Miguel  
    :material/arrow_right: Gualcaloma  
    :material/arrow_right: El Pilar  
    :material/arrow_right: Panamericano  
    :material/arrow_right: María Isabel  
    :material/arrow_right: Santa Mónica    
    :material/arrow_right: El Tejar  
    :material/arrow_right: Carlos Pizarro  
    :material/arrow_right: San Miguel  
    :material/arrow_right: Gualcaloma  
    :material/arrow_right: El Pilar  
    :material/arrow_right: Panamericano  
    :material/arrow_right: Santa Mónica  

Muchos de estos barrios coinciden con los que en otras preguntas reportaron:  
    :material/arrow_right: baja presión,  
    :material/arrow_right: afectaciones por obras,  
    :material/arrow_right: falta de aviso previo,  
    :material/arrow_right: dificultades en continuidad,  
    :material/arrow_right: percepción negativa en mantenimiento.  
Esto confirma que la percepción de gestión está influenciada por la experiencia operativa directa.
""")


col1, col2 = st.columns(2)
with col1:
    st.subheader("¿A través de qué medio se entera de las noticias de EMPOPASTO?")
    pregunta17_17_1 = df2.filter((pl.col("variable") == 'pregunta17') | (pl.col("variable") == 'pregunta17_1'))
    pregunta17_17_1 = pregunta17_17_1.filter(pl.col("value") != "Otro")
    grafico17_17_1 = pregunta17_17_1.group_by(["Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)
    fig = px.bar(grafico17_17_1, y="value", x="count", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col2:
    st.subheader("¿A través de qué medio le gustaría recibir la información de EMPOPASTO?")
    pregunta18_18_1 = df2.filter((pl.col("variable") == 'pregunta18') | (pl.col("variable") == 'pregunta18_1'))
    pregunta18_18_1 = pregunta18_18_1.filter(pl.col("value") != "Otro")
    grafico18_18_1 = pregunta18_18_1.group_by(["Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)

    fig = px.bar(grafico18_18_1, y="value", x="count", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown("""Los usuarios de EMPOPASTO actualmente se informan principalmente a través de redes sociales (49,2%) y radio (31,3%), mientras que los canales tradicionales como la factura (5,6%) y la televisión (3,87%) tienen un uso mucho menor.  
Sin embargo, al analizar cómo los usuarios desean recibir información, se observan cambios importantes:  
:material/arrow_right: Disminuye la preferencia por redes sociales (de 49,2% a 42,7%)  
:material/arrow_right: Cae fuertemente la preferencia por radio (de 31,3% a 19,9%)  
:material/arrow_right: Aumenta la preferencia por recibir información en la factura (de 5,6% a 13,7%)  
:material/arrow_right: El correo electrónico pasa de ser marginal a 10,8%, mostrando un crecimiento notable.  
Estos resultados indican que los usuarios sí están conectados digitalmente, pero quieren canales más directos, personalizados y oficiales para recibir información.""")

st.subheader("¿Conoce los servicios que presta EMPOPASTO en su página Web?")

col1, col2 = st.columns(2)
with col1:
    pregunta19 = df2.filter(pl.col("variable") == "pregunta19")
    pregunta19 = pregunta19.group_by(["Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)

    fig = px.pie(pregunta19, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    st.markdown("""El :blue[73,8 %] de los usuarios afirma haber utilizado la página web de EMPOPASTO, lo que demuestra que el portal institucional es un recurso relevante y activo para la ciudadanía.  
    Esto indica una adopción digital significativa, especialmente en estratos tradicionalmente asociados a menor acceso tecnológico. Los estratos más bajos son quienes más usan la página, lo cual es un buen indicador de inclusión digital y demuestra que la web es un canal accesible para ellos.    
    El :red[26,2 %] restante no ha utilizado la página web, lo cual representa una oportunidad importante para mejorar acceso, información, navegación o promoción de los servicios digitales, este es un grupo con riesgo de quedar excluido de información o servicios, por lo que se deben priorizar acciones de comunicación y educación digital.
    """)
with col2:
    st.subheader("¿Cuál ha utilizado?")
    pregunta19_1 = df2.filter(pl.col("variable") == "pregunta19_1")
    pregunta19_1 = pregunta19_1.group_by(["Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)

    fig = px.bar(pregunta19_1, y="value", x="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    pregunta19_no = pregunta19.filter(pl.col("value") == "NO")
    pregunta19_no = pregunta19_no.group_by(["Desc Subcategoria", "Desc Categoria", "value", "Barrio"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)

    pregunta19_no = pregunta19_no.group_by("Barrio").agg(
        pl.len().alias("count")
    ).sort("count", descending=True)

    pregunta19_no = pregunta19_no.with_columns(
        (
            pl.col("count") / pl.col("count").sum()
        ).cast(pl.Float64).round(2).alias("Porcentaje")
    )
    st.dataframe(pregunta19_no, height=200)

st.markdown("### **¿Qué sugerencias tiene para Empopasto?**")
pregunta22 = df2.filter(pl.col("variable") == "pregunta22")

sugerencias = pregunta22.select(["value"])

for (row,) in sugerencias.iter_rows():
    st.markdown(f":material/arrow_right: {row}")