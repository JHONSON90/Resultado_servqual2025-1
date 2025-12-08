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

# Agregar logos y menú en la sidebar
st.sidebar.image("../assets/empopasto_logo.jpg", width="stretch")
st.sidebar.markdown("---")

# Menú de navegación con iconos profesionales
st.sidebar.page_link("app.py", label="📊 Generalidades")
st.sidebar.page_link("pages/aspectos_generales.py", label="📋 Aspectos Generales")
st.sidebar.page_link("pages/acueducto_alcantarillado.py", label="💧 Acueducto y Alcantarillado")
st.sidebar.page_link("pages/gestion_comunicacion.py", label="📢 Gestión y Comunicación")
st.sidebar.page_link("pages/Conclusiones.py", label="✅ Conclusiones")

st.sidebar.markdown("---")
st.sidebar.image("../assets/one_logo.jpg", width=80)

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


st.title(":blue[Acueducto y Alcantarillado]")

st.markdown("### ¿Cómo califica la calidad de agua que recibe de EMPOPASTO?")
st.badge("Fiabilidad")

pregunta10 = df.filter((pl.col("variable") == "pregunta10") & (pl.col("value") != 0))
p10_ns = df3.filter(pl.col("variable") == "pregunta10")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p10_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
        st.markdown("""La percepción sobre la calidad del agua ha mostrado una variación moderada durante los tres años analizados. Aunque el indicador sigue siendo alto y positivo, se evidencia una caída en 2024 respecto al 2023 y una recuperación leve en 2025, sin llegar al nivel óptimo alcanzado en 2023.  
    Este comportamiento sugiere que los usuarios mantienen una percepción favorable del servicio, pero existen aspectos puntuales que han afectado ligeramente la confianza.  
    En 2025 se observa una recuperación leve (+1,23 puntos porcentuales), lo que indica que los esfuerzos en operación, mantenimiento o comunicación lograron mejorar la percepción, pero no en la magnitud requerida para volver a niveles de excelencia.

""")


col7, col8 = st.columns(2)
with col7:
    grafico10 = pregunta10.group_by("value").agg(
        pl.len().alias("count")
    ).sort("count", descending=True)
    fig = px.pie(grafico10, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"]
, height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col8:
    grafico10_1 = pregunta10.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)
    fig = px.bar(grafico10_1, x="Desc Subcategoria", y="count", color="value", barmode="relative", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"]
, height=400, title='Respuestas por Estrato')
    st.plotly_chart(fig, width="stretch")


st.markdown("""El :blue[92,7 %] de la población se encuentra satisfecha con la calidad del agua que recibe de Empopasto, mientras que el :red[7,3 %] expresa algún nivel de inconformidad.  
Estos resultados reflejan una alta percepción positiva de los usuarios respecto al producto principal que ofrece la empresa **el agua potable** evidenciando que los estándares de tratamiento, potabilidad y continuidad del servicio son reconocidos favorablemente por la comunidad.""")


st.markdown("### ¿Empopasto le brinda información de manera anticipada sobre las suspensiones del servicio en su sector? ")
st.badge("Capacidad de respuesta")
pregunta11 = df2.filter(pl.col("variable") == "pregunta11")

col9, col10, col11 = st.columns(3)
with col9:
    grafico11 = pregunta11.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico11, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
with col10:
    st.text("Estratos mas representativos")
    grafico11_estrato = pregunta11.filter(pl.col("value") == "NO").group_by("Desc Subcategoria").agg(
        pl.len().alias("count")
    )
    st.write(grafico11_estrato)
with col11:
    grafico11_barrio = pregunta11.filter(pl.col("value") == "NO").group_by("Barrio").agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico11_barrio, y="Barrio", x="count", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Barrios que generan inconformidades")
    st.plotly_chart(fig, width="stretch")
    
st.markdown("**Si la respuesta es Si, califique si la información y el tiempo de aviso previo a la suspensión del servicio de agua son adecuados**")

pregunta11_1 = df.filter(pl.col("variable") == "pregunta11_1").filter(pl.col("value") != 0)
p11_1_ns = df3.filter(pl.col("variable") == "pregunta11_1")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p11_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#FFD700","#8B0000","#006400"], height=400)
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
        st.markdown("""La satisfacción con el aviso previo a la suspensión del servicio presenta una evolución altamente positiva en 2025, alcanzando 80,89%, lo que representa una recuperación importante después de un desempeño moderado en 2023 y 2024.  
    El incremento de 7,49 puntos entre 2024 y 2025 indica que las mejoras en los canales de información (redes, perifoneo, avisos por factura, coordinación con cuadrillas) tuvieron un efecto directo en la percepción del usuario.  
    Aunque la tendencia es favorable, aún existen oportunidades para reforzar la información en barrios vulnerables o de difícil acceso para llevar este indicador a niveles superiores al 85–90%.""")


col12, col13 = st.columns(2)
with col12:
    grafico11_1 = pregunta11_1.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico11_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col13:
    grafico11_1_estrato = pregunta11_1.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico11_1_estrato, x="Barrio", y="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas bajaspor Estrato y barrios")
    st.plotly_chart(fig, width="stretch")

st.markdown("""Se evidencia que el :blue[68.2 %] de la población recibe información previa sobre las suspensiones del servicio, mientras que el :red[31.8 %] manifiesta no ser informada oportunamente.
Este resultado refleja un avance positivo en los canales de comunicación, aunque aún existen brechas de cobertura informativa, especialmente en algunos barrios y estratos socioeconómicos.

Dentro del grupo que no recibe la información (31,8 %), destacan los barrios Atahualpa, Ocho de Marzo, Las Américas y Bellavista, pertenecientes principalmente a los estratos Único, Bajo, Medio-Bajo y Bajo-Bajo.
En cuanto al tiempo de aviso previo, el :blue[90.9 %] de los usuarios considera que este es adecuado, y solo un :red[9.1 %] lo califica como inadecuado.
Las inconformidades provienen principalmente de los barrios Agualongo, San Juan de Dios, Miraflores, Caicedo Alto, Ocho de Marzo, Manantial y Niza II.
""")

st.markdown("### Considera Usted, que la continuidad del servicio que presta EMPOPASTO es:")
st.badge("Fiabilidad")
pregunta12 = df.filter(pl.col("variable") == "pregunta12")

p12_ns = df3.filter(pl.col("variable") == "pregunta12")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p12_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
        st.markdown("""La continuidad del servicio es uno de los indicadores más sensibles para los usuarios porque afecta directamente su vida diaria.  
    El análisis muestra que, aunque los niveles de satisfacción siguen siendo altos, el indicador evidencia una tendencia descendente constante durante los tres años evaluados.
    Continúa la tendencia negativa (-1.67 puntos porcentuales), aunque con una caída menos pronunciada que en el año anterior (-2.9 puntos porcentuales).
    Esto indica que, a pesar de acciones o mantenimientos realizados, el usuario continúa experimentando interrupciones o disminuciones temporales de servicio.
    """)

col14, col15 = st.columns(2)
with col14:
    grafico12 = pregunta12.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico12, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
    
with col15:
    grafico12_barrio = pregunta12.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico12_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas bajas por Estrato y barrios")
    st.plotly_chart(fig, width="stretch")

st.markdown("""En cuanto a la continuidad del servicio, el :blue[90,5 %] de la población considera que el suministro de agua es adecuado, superando por 0,5 puntos porcentuales la meta sugerida del 90 %.  
Por otro lado, el :red[9,5 %] manifiesta que el servicio no es continuo o presenta interrupciones ocasionales.  
Las principales inconformidades se concentran en los barrios Agualongo, Panamericano, La Carolina y Caicedo Alto, donde los usuarios reportan cortes esporádicos o disminución temporal del caudal.
    """)

st.markdown("### La presión de agua en su inmueble o en su vivienda es?")
st.badge("Fiabilidad")
pregunta13 = df.filter((pl.col("variable") == "pregunta13") & (pl.col("value") != 0))
p13_ns = df3.filter(pl.col("variable") == "pregunta13")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p13_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
        st.markdown("""La satisfacción con el aviso previo a la suspensión del servicio presenta una evolución altamente positiva en 2025, alcanzando 80,89%, lo que representa una recuperación importante después de un desempeño moderado en 2023 y 2024.  
    El incremento de 7,49 puntos entre 2024 y 2025 indica que las mejoras en los canales de información (redes, perifoneo, avisos por factura, coordinación con cuadrillas) tuvieron un efecto directo en la percepción del usuario.  
    Aunque la tendencia es favorable, aún existen oportunidades para reforzar la información en barrios vulnerables o de difícil acceso para llevar este indicador a niveles superiores al 85–90%.""")


col16, col17 = st.columns(2)
with col16:
    grafico13 = pregunta13.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico13, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400,title="Respuestas")
    st.plotly_chart(fig, width="stretch")
with col17:
    grafico13_barrio = pregunta13.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico13_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400,title="Respuestas bajas por Estrato y barrios")
    st.plotly_chart(fig, width="stretch")

st.markdown("""En relación con la presión del agua, el :blue[90.7 %] de los usuarios manifiesta estar satisfecho con la presión del servicio recibido, lo que representa un resultado positivo y coherente con la percepción favorable sobre la continuidad del servicio (:blue[90,5 %] en la pregunta anterior).
Este desempeño es destacable considerando las condiciones geográficas y topográficas del municipio de Pasto, que naturalmente pueden generar variaciones en la presión en algunos sectores.

No obstante, un :red[9.3 %] de los usuarios considera que la presión es baja o inadecuada, identificándose principalmente los barrios La Floresta, Chambú, Quintas de San Pedro, San Vicente, Panorámico II Etapa y La Cruz.
En estos sectores se reportan cortes esporádicos o disminución temporal del caudal, lo que sugiere relación directa entre interrupciones parciales y presión insuficiente.
""")

st.markdown("### ¿Cómo califica la oportunidad y organización de los trabajos realizados cuando se presenta un daño de acueducto o alcantarillado?")
st.badge("Capacidad de respuesta")
pregunta14 = df.filter((pl.col("variable") == "pregunta14") & (pl.col("value") != 0))

col18, col19 = st.columns(2)
with col18:
    p14_ns = df3.filter(pl.col("variable") == "pregunta14")
    fig = px.bar(p14_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
    )
    st.plotly_chart(fig, theme="streamlit", width="stretch")


    grafico14 = pregunta14.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico14, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
    
    grafico14_1 = df2.filter(pl.col("variable") == "pregunta14_1")
    grafico14_1 = grafico14_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico14_1, y="value", x="count", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Razones por calificación baja")
    st.plotly_chart(fig, width="stretch")
    

with col19:
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""El indicador presenta una tendencia descendente leve y sostenida, con una reducción más marcada entre 2023 y 2024, y una estabilidad prácticamente plana entre 2024 y 2025.  
        La caída total 2023 - 2025 es de 2,48 puntos.  
        El nivel de satisfacción permanece críticamente bajo frente a la meta institucional (≥ 90%).  
        Refleja que los usuarios continúan percibiendo deficiencias en la planeación, comunicación y ejecución de obras.""")

    grafico14_barrio = pregunta14.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico14_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por barrio, estrato y tipo de servicio")
    st.plotly_chart(fig, width="stretch")
    grafico14_1_barrio = df2.filter(pl.col("variable") == "pregunta14_1").group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico14_1_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Barrios con calificación baja por estrato y tipo de servicio")
    st.plotly_chart(fig, width="stretch")

st.markdown(""" Frente a la oportunidad y organización en los trabajos de reparación de acueducto y alcantarillado, el :blue[67,68 %] de los usuarios se muestra satisfecho, mientras que un :green[26,9 %] mantiene una posición neutra, y un :red[5,4 %] considera que la atención es inadecuada o insatisfactoria.
Este resultado refleja una percepción moderadamente positiva, pero con oportunidades claras de mejora en la agilidad de respuesta y finalización de obras.

Las principales inconformidades se presentan en los barrios residenciales de estratos Bajo, Medio y Medio-Bajo, y en zonas comerciales, donde los usuarios manifiestan que las demoras en las reparaciones afectan la movilidad y el desarrollo del comercio, además de reportar trabajos inconclusos o con acabados deficientes.
En el caso de los usuarios residenciales, la percepción negativa se asocia con la falta de mantenimiento preventivo y los tiempos prolongados de atención a solicitudes.
""")

st.markdown("### ¿Cómo califica la labor de mantenimiento y limpieza en cámaras y sumideros para evitar taponamientos y reboses?")
st.badge("Capacidad de respuesta")
pregunta16 = df.filter((pl.col("variable") == "pregunta16") & (pl.col("value") != 0))
p16_ns = df3.filter(pl.col("variable") == "pregunta16")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p16_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
        st.markdown("""Este indicador muestra que en el año 2024 representó el punto más bajo del período analizado, evidenciando vulnerabilidades internas o factores externos que afectaron de manera significativa el desempeño del servicio. No obstante, el 2025 refleja una notable recuperación operativa, lo que demuestra la resiliencia y capacidad de respuesta del equipo. A pesar de estos avances, persiste una brecha aproximada de 17 puntos respecto al objetivo del 90 %, lo que invita a mantener una vigilancia constante. Dado que el indicador es especialmente sensible a la frecuencia y calidad del mantenimiento preventivo, su sostenibilidad dependerá de un compromiso continuo con controles rigurosos y proactivos.

""")

col20, col21 = st.columns(2)
with col20:
    grafico16 = pregunta16.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico16, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
    
with col21:
    grafico16_barrio = pregunta16.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico16_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Barrios con calificación baja por estrato y tipo de servicio")
    st.plotly_chart(fig, width="stretch")

pregunta16_1 = df2.filter(pl.col("variable") == "pregunta16_1")
#st.write(pregunta16_1)

st.markdown("""Respecto a las labores operativas y de mantenimiento del sistema de acueducto y alcantarillado, se evidencia una percepción moderadamente positiva entre los usuarios.
En la oportunidad y organización de los trabajos correctivos (Pregunta 14), el :blue[67,68%] de los usuarios se declara satisfecho, mientras que el :green[26,9%] mantiene una opinión neutra y el :red[5,4%] considera que la atención es inadecuada.
En la labor de mantenimiento preventivo y limpieza de cámaras y sumideros (Pregunta 16), el :blue[67,83%] se muestra conforme, el :green[23%] mantiene una postura neutra y el :red[9.18%] expresa insatisfacción.  
Ambas preguntas revelan que, aunque más de dos tercios de los usuarios valoran positivamente el trabajo realizado, existe un margen importante de mejora (alrededor del 30 % de usuarios neutros o insatisfechos) que perciben falta de consistencia, lentitud o trabajos inconclusos.  
Las principales inconformidades se concentran en barrios residenciales de estratos Medio-Bajo, Bajo y Bajo-Bajo (72,2 %), y en zonas comerciales (27,8 %), donde los comerciantes mencionan que los retrasos o mantenimientos prolongados dificultan la movilidad y las ventas.  
El barrio Las Américas se destaca con el 13,6 % de menciones negativas, asociado a deficiencias en limpieza y mantenimiento de sumideros.
""")




st.subheader("Se ha visto afectado por los trabajos adelantados por EMPOPASTO?")
pregunta15 = df2.filter(pl.col("variable") == "pregunta15")
pregunta15 = pregunta15.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
)
col1, col2 =st.columns(2)
with col1:
    fig = px.pie(pregunta15, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

pregunta15_1_confg = pl.DataFrame({
    "Pregunta": ['Dejan muchos escombros','Afectacion al comercio','Oportunidad en la informacion','Cierre de vias','Incentivar la inseguridad,','Falta de planificacion','Trabajos demorados','Suspencion del servicio de agua','Cobro adicional en la factura','Daños en las propiedades','Malos Olores','No cumplen su objetivo','Baja la presion en el agua','Cambio de tuberia','Horarios no adecuados','Malos Tratos por parte del personal','En el hogar','Por las inundaciones','Afecta la seguridad'], 
    "Contestacion": [15,16,1,38,1,5,9,23,1,7,2,5,1,2,1,1,1,1,1]
})

with col2:
    pregunta15_1 = df2.filter(pl.col("variable") == "pregunta15_1")
    pregunta15_1 = pregunta15_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(pregunta15_1_confg, y="Pregunta", x="Contestacion", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Razones de afectacion")
    st.plotly_chart(fig, width="stretch")



st.markdown("""Con base en los datos, el :blue[74.2%] de los usuarios indicó que no ha sido afectado por los trabajos realizados por EMPOPASTO, lo que refleja una percepción mayoritariamente positiva sobre la planeación y gestión operativa de las intervenciones.  
Sin embargo, el :red[25.8%] sí reportó haber sido afectado, lo que representa una cuarta parte de la población, por lo que este aspecto no puede ser considerado menor o excepcional.  
Entre las afectaciones reportadas, el cierre de vías (29 %) es la causa más frecuente, seguida por la suspensión temporal del servicio de agua (17.6 %) y la afectación del comercio (12.2 %).  
Esto indica que las intervenciones de infraestructura, aunque necesarias, impactan directamente la movilidad, la disponibilidad del servicio y el desarrollo económico, especialmente en zonas comerciales.  
El 25.8 % afectado es una cifra importante y sugiere que persisten espacios de mejora, especialmente en:  
    :material/arrow_right: Comunicación previa de cierres y suspensiones.  
    :material/arrow_right: Coordinación con autoridades de tránsito.  
    :material/arrow_right: Ejecución nocturna o por fases.  
    :material/arrow_right: Tiempos de cierre más cortos para zonas comerciales.  
El cierre de vías como principal afectación indica que los usuarios perciben más impacto en su movilidad que en la disponibilidad del servicio.  
La afectación del comercio (12.2 %) evidencia impactos económicos que requieren un enfoque especial en la relación con el sector comercial.
""")

