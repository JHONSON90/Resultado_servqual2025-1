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


st.title(":blue[Aspectos Generales]")
st.markdown("### ¿Usted considera que el tiempo de entrega de su factura, hasta la fecha límite de pago de la misma, es adecuado?")
st.badge("Fiabilidad" )

pregunta1 = df.filter(pl.col("variable") == "pregunta1")

p1_ns = df3.filter(pl.col("variable") == "pregunta1")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
    fig.update_layout(
    bargap=0.2,  
    bargroupgap=0.05, 
    legend_title_text='Año'
)
    st.plotly_chart(fig, width="stretch")

with col2:
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""El análisis muestra que el nivel de satisfacción ha tenido variaciones importantes durante los tres años evaluados:  
    :material/arrow_right: En 2023, el indicador se ubicó en un nivel muy alto (91,3%), cumpliendo la meta institucional del 90%.  
    :material/arrow_right: En 2024, el indicador presentó un descenso significativo al 87,9%, lo que representa una caída de 3,4 puntos porcentuales, ubicando el desempeño por debajo del nivel esperado.  
    :material/arrow_right: En 2025, se observa una recuperación importante, alcanzando un 81,93%, con un aumento de 24,23 puntos frente a 2024.""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Calificaciones**")
    graficap1 = pregunta1.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(graficap1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

    st.markdown("""El **:blue[87,2 %]** de los usuarios califica positivamente el tiempo de entrega de la factura, siendo el **:blue[61,5 %]** satisfecho y el **:blue[25,7 %]** muy satisfecho. 
    Solo un **:red[12,8 %]** manifiesta inconformidad, lo que indica que el proceso de distribución de facturas cumple con las expectativas de la mayoría de los usuarios.""")

with col2:    
    #st.metric("Meta Sugerida", "≥ 90%", border=True)
    satisfactorio = pregunta1.filter(
        (pl.col("value") == 4) | (pl.col("value") == 5)
    ).group_by("value").agg(
        pl.len().alias("count")
    )
    satisfactorio = satisfactorio.select("count").sum()
    # st.write(pregunta1)
    # st.write(satisfactorio.item())
    st.metric("Total de respuestas", f"{satisfactorio.item()/600*100:.2f} %", border=True)

    por_estrato = pregunta1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    por_estrato = por_estrato.filter(
        pl.col("value") <= 3
    )
    st.markdown("**Evaluacion de calificaciones bajas por Tipo de servicio**")
    # fig = go.Figure()
    # fig.add_trace(go.Bar(x=por_estrato["Desc Categoria"], y=por_estrato["count"], name="Desc Categoria", text=por_estrato["Desc Subcategoria"], textposition="auto", hovertext=por_estrato["Desc Subcategoria"]))
    # # fig.add_trace(go.Bar(x=por_estrato["Desc Subcategoria"], y=por_estrato["count"], name="Desc Subcategoria"))
    # fig.update_layout(
    #     xaxis_title="Estrato",
    #     yaxis_title="Cantidad",
    #     barmode="group")

    fig = px.bar(por_estrato, x="Desc Categoria", y="count", color="Desc Subcategoria", hover_name="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)

    st.plotly_chart(fig, width="stretch")

pregunta2 = df.filter(pl.col("variable") == "pregunta2").filter(pl.col("value") > 0)
pregunta2_1 = df2.filter(pl.col("variable") == "pregunta2_1")
st.markdown("### ¿Cómo califica la información contenida en la factura de pago en términos de facilidad para comprenderla?")
st.badge("Fiabilidad" )

p2_ns = df3.filter(pl.col("variable") == "pregunta2")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p2_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400", "#FFD700","#8B0000"], height=400)
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
        st.markdown("""La evolución del indicador en la Pregunta 2 evidencia una tendencia decreciente y sostenida durante los tres años analizados:  
    :material/arrow_right: En 2023, el nivel de satisfacción se ubicó en 82,7%, un valor sólido y cercano al umbral del 85%.  
    :material/arrow_right: En 2024, se observa una ligera reducción a 80,9%, con una caída de 1,8 puntos porcentuales.  
    :material/arrow_right: En 2025, la tendencia descendente continúa, alcanzando un 79,33%, disminuyendo 1,57 puntos más.  
    El indicador continúa bajando, aunque la caída es similar en magnitud a la del periodo anterior. Esto muestra que el deterioro no es abrupto, pero sí constante, lo cual evidencia una percepción que se está debilitando con el tiempo.""")


col3, col4 = st.columns(2)

with col3:
    st.markdown("**Respuestas**")
    graficop2 = pregunta2.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(graficop2, names="value", values="count",color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""El ***:blue[80,6 %]*** de los usuarios percibe la información en la factura como clara o muy clara, lo que refleja un nivel aceptable de comprensión del contenido. Sin embargo, un ***:red[19,4 %]*** manifiesta dificultades para entenderla, lo que indica que aún existen aspectos de presentación o redacción que podrían mejorarse.  
    Los grupos que presentan la mayor proporción de dificultades para comprender la factura corresponden a los usuarios residenciales de estrato bajo y bajo-bajo. Esta situación podría obedecer a la falta de conocimiento sobre los conceptos facturados.  Por su parte, los usuarios residenciales de estrato medio y medio-bajo, aunque exhiben una mejor comprensión, aún evidencian dudas respecto a los conceptos incluidos en la factura.
    """)
    

with col4:
    st.markdown("**Estratos donde la calificación fue insatisfecha o muy insatisfecha**")

    pregunta2_baja = pregunta2.filter(pl.col("value") < 4)
    pregunta2_baja = pregunta2_baja.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    ).sort("value", descending=True)

    fig = px.bar(pregunta2_baja, y="count", x="Desc Categoria", color="Desc Subcategoria", hover_name="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

    grafico2_1 = pregunta2_1.group_by("value").agg(
        pl.len().alias("count")
    ).sort("value", descending=True)
    fig = px.bar(grafico2_1, y="value", x="count", color="value", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Razones de calificaciones 1 o 2")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")
st.markdown("""  
    Los usuarios que encuentran la factura difícil de comprender mencionan dos causas principales:  
    :material/arrow_right: 60 % no conoce el significado o detalle de los conceptos facturados.  
    :material/arrow_right: 12,5 % no comprenden la inclusión del servicio de aseo, lo que evidencia una brecha de información sobre la normatividad o convenios interinstitucionales.  
    Estos resultados apuntan a una necesidad de fortalecer la comunicación educativa al usuario sobre la estructura y conceptos de cobro en la factura.""")
st.markdown("### ¿Conoce los sitios de pago de su factura?")
st.badge("Seguridad" )

p3_ns = df3.filter(pl.col("variable") == "pregunta3")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p3_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#FFD700","#8B0000", "#006400"], height=400)
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
        st.markdown("""En esta pregunta muestra un comportamiento altamente positivo, con valores muy elevados en los tres años. A diferencia de otras preguntas que muestran descensos o recuperaciones, esta se destaca porque:  
    :material/arrow_right: Mantiene niveles superiores al 87% en toda la serie.  
    :material/arrow_right: Presenta un incremento significativo en 2025.  
    Esto indica que el aspecto evaluado en esta pregunta es uno de los mejores percibidos por los usuarios y constituye una fortaleza dentro del servicio.""")


col15, col16 = st.columns(2)
with col15:
    pregunta3 = df2.filter((pl.col("variable") == "pregunta3"))
    grafico3 = pregunta3.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico3, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col16:
    pregunta3_baja = pregunta3.filter(pl.col("value") == "NO")
    grafico3_1 = pregunta3_baja.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico3_1, y="count", x="Desc Categoria", color="Desc Subcategoria", hover_name="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Estratos donde la población no tiene claro los puntos de pago")
    st.plotly_chart(fig, width="stretch")

st.markdown("""La población, además de mostrar un alto nivel de cumplimiento con sus obligaciones hacia Empopasto, también demuestra un conocimiento generalizado de los puntos donde puede realizar el pago de su factura.  
El :blue[94,8 %] de los usuarios conoce los lugares de pago, mientras que existe una brecha del :red[5,17 %] que desconoce los puntos habilitados.  
Este grupo minoritario se concentra principalmente en los usuarios residenciales de estratos Bajo y Medio-Bajo, sectores donde persisten dificultades de acceso a información digital o puntos físicos más alejados por lo que requieren mecanismos más accesibles de información y orientación presencial, especialmente en barrios con baja conectividad o alfabetización digital.
""")

st.markdown("### La atención que Usted recibe en nuestros puntos, ha sido:")
st.badge("Empatía")

col1, col2, col3 = st.columns(3)
with col1:
    p4_1_ns = df3.filter(pl.col("variable") == "pregunta4_1")
    fig = px.bar(p4_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion Amabilidad", color_discrete_sequence=["#FFD700","#8B0000","#006400"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
)
    st.plotly_chart(fig, theme="streamlit", width="stretch")
    st.markdown("""El indicador de amabilidad presenta un comportamiento estable entre 2023 y 2024, pero un salto muy significativo en 2025:  
    :material/arrow_right: Estabilidad 2023–2024 prácticamente no hubo variación (–0,2 puntos).  
    :material/arrow_right: Mejora sustancial en 2024–2025 donde se evidencia un incremento de 11,25 puntos, ubicando el indicador en el nivel más alto registrado en los tres años.  
    Este componente se convierte en uno de los indicadores con mayor mejora interanual positiva dentro del eje de Empatía / Atención.""")
with col2:
    p4_2_ns = df3.filter(pl.col("variable") == "pregunta4_2")
    fig = px.bar(p4_2_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion Agilidad", color_discrete_sequence=["#8B0000","#FFD700","#006400"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
)
    st.plotly_chart(fig, theme="streamlit", width="stretch")
    st.markdown("""El indicador refleja una recuperación estructural del servicio:  
    :material/arrow_right: De 71–73% (niveles aceptables pero bajos)  
    :material/arrow_right: A 83,51% (nivel sobresaliente y competitivamente alto)  
    Aunque aún no se alcanza el 90%, la trayectoria indica que, de mantenerse los esfuerzos en procesos de atención y reducción de tiempos, es viable alcanzar la meta institucional en el corto plazo.""")
with col3:
    p4_3_ns = df3.filter(pl.col("variable") == "pregunta4_3")
    fig = px.bar(p4_3_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion Oportunidad", color_discrete_sequence=["#8B0000","#FFD700","#006400"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
)
    st.plotly_chart(fig, theme="streamlit", width="stretch")
    st.markdown("""La oportunidad en la atención estuvo estancada durante dos años, pero presentó un salto significativo en 2025.  
    El incremento del 10% es suficientemente grande para evidenciar cambios reales en la operación y no solo variaciones estadísticas.  
    El indicador se acerca a niveles de excelencia, aunque todavía queda una brecha cercana a 6,5 puntos para alcanzar el estándar del 90%.  
    En conjunto con amabilidad y agilidad, 2025 se consolida como el año con la mejor percepción del componente de empatía.""")

st.markdown("""**Analisis de los componentes en conjunto:**  
Los tres componentes muestran un crecimiento claro y coherente en 2025, lo que indica una mejora integral en la experiencia de atención presencial.  
Esto refuerza la hipótesis de que en 2025 se implementaron acciones concretas de mejora en el modelo de atención, y el usuario lo percibió.""")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Amabilidad")
    pregunta4_1 = df.filter((pl.col("variable") == "pregunta4_1") & (pl.col("value") != 0))
    pregunta4_1 = pregunta4_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.pie(pregunta4_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
with col2:
    fig = px.bar(pregunta4_1, x="value", y="count", color="Desc Categoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")

with col3:
    fig = px.bar(pregunta4_1, x="value", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio y estrato")
    st.plotly_chart(fig, width="stretch")



pregunta4_2 = df.filter((pl.col("variable") == "pregunta4_2") & (pl.col("value") != 0))
pregunta4_2 = pregunta4_2.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Agilidad")
    fig = px.pie(pregunta4_2, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.bar(pregunta4_2, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")

with col3:
    fig = px.bar(pregunta4_2, x="value", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio y estrato")
    st.plotly_chart(fig, width="stretch")

pregunta4_3 = df.filter((pl.col("variable") == "pregunta4_3") & (pl.col("value") != 0))
pregunta4_3 = pregunta4_3.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### Oportunidad")
    fig = px.pie(pregunta4_3, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.bar(pregunta4_3, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")

with col3:
    fig = px.bar(pregunta4_3, x="value", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio y estrato")
    st.plotly_chart(fig, width="stretch")

consolidado = pl.DataFrame({
    "positivos": [92.6, 89, 91.2], 
    "caracteristicas": ["Amable", "Agil", "Oportuna"]
})
col1, col2 = st.columns(2)
with col1:
    fig = px.line_polar(consolidado, r="positivos", theta="caracteristicas", line_close=True, height=400)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, width="stretch")

with col2:
    with st.container(
        height=500, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""  
        Al analizar los tres componentes de la atención en los puntos de servicio, se evidencia una alta aceptación por parte de los usuarios.  
        Dos de las tres dimensiones evaluadas alcanzan niveles superiores al 90 %, específicamente amabilidad :blue[92,6 %] y oportunidad :blue[91,2 %], lo que demuestra un desempeño destacado en el trato al usuario y la disposición oportuna del servicio.  
        En cuanto a la agilidad, aunque el :green[89 %] sigue siendo un resultado positivo, este valor está por debajo del nivel esperado y se ubica ligeramente por debajo de las otras dimensiones del servicio.  
        Esto sugiere que, si bien la atención es amable y oportuna, los tiempos de espera o la rapidez en la gestión pueden estar generando pequeñas fricciones en la experiencia del usuario.  
        La amabilidad es el punto más fuerte del servicio, lo cual es clave en el componente de Empatía de SERVQUAL.  
        La oportunidad supera el :blue[90 %], indicando que los usuarios perciben que la atención se da dentro de tiempos razonables.  
        La agilidad, al ser la más baja :green[89 %], debe ser tratada como un indicador de alerta leve: está bien evaluada, pero no sobresaliente. Puede estar relacionada con:  
            :material/arrow_right: tiempos de espera en fila,  
            :material/arrow_right: lentitud en trámites específicos,  
            :material/arrow_right: falta de personal en horas pico.
        """)

st.markdown("### ¿Durante el año pasado, Usted presentó una petición, una queja, reclamo, sugerencia o una denuncia (PQRS)?")
st.badge("Capacidad de respuesta" )
pregunta5 = df2.filter(pl.col("variable") == "pregunta5")

grafico5 = pregunta5.group_by(["Desc Categoria", "value"]).agg(
    pl.len().alias("count")
)
col1, col2, col3 = st.columns(3)
with col1:
    fig = px.pie(grafico5, names="value", values="count", color="value", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")
with col2:
    fig = px.bar(grafico5, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")
with col3:
    fig = px.bar(grafico5, x="value", y="count", color="value", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio y estrato")
    st.plotly_chart(fig, width="stretch")

st.markdown("**¿La orientación que recibió a su trámite, fue:**")
col1, col2 = st.columns(2)
with col1:
    p5_1_ns = df3.filter(pl.col("variable") == "pregunta5_1")
    fig = px.bar(p5_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
    )
    st.plotly_chart(fig, theme="streamlit", width="stretch")

    pregunta5_1 = df.filter((pl.col("variable") == "pregunta5_1") & (pl.col("value") != 0))
    grafico5_1 = pregunta5_1.group_by(["Desc Categoria", "value"]).agg(
    pl.len().alias("count"))
    fig = px.bar(grafico5_1, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")
with col2:
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""El resultado de 66,13% muestra que la orientación en la atención de PQRS no cumple con las expectativas de los usuarios, y debe considerarse un indicador prioritario para el plan de mejora.  
    Este valor servirá como línea base para medir avances en los próximos años.  
    Acciones como mejorar la trazabilidad del proceso, la claridad de la información y la capacitación del personal ayudarán a incrementar este indicador hacia niveles óptimos.""")
    pregunta5_1_barrio = df.filter((pl.col("variable") == "pregunta5_1") & (pl.col("value") != 0) & (pl.col("value") < 3)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
        )
    fig = px.bar(pregunta5_1_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas de 1 y 2 por barrio, tipo de servicio y estrato")
    st.plotly_chart(fig, theme="streamlit", width="stretch")

st.markdown("**¿Cómo califica la respuesta a su PQRS?**")
col1, col2 = st.columns(2)
with col1:
    p5_2_ns = df3.filter(pl.col("variable") == "pregunta5_2")
    fig = px.bar(p5_2_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
    )
    st.plotly_chart(fig, theme="streamlit", width="stretch")

    pregunta5_2 = df.filter((pl.col("variable") == "pregunta5_2") & (pl.col("value") != 0))
    grafico5_2 = pregunta5_2.group_by(["Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(grafico5_2, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")
    
with col2:
    st.markdown("""El resultado de 63,05% deja claro que la calidad de la respuesta a las PQRS es un punto crítico dentro de la experiencia del usuario.  
        Este indicador, junto con la orientación en el trámite (66,13%), evidencia que el proceso PQRS requiere intervenciones urgentes a nivel de:  
        :material/arrow_right: Tiempos de respuesta,  
        :material/arrow_right: Claridad del contenido,  
        :material/arrow_right: Pertinencia técnica,  
        :material/arrow_right: Acompañamiento al usuario.  
        Este valor servirá como la línea base para el mejoramiento continuo en próximos periodos. Implementar mejoras específicas en el proceso permitirá aumentar significativamente este indicador y mejorar la confianza de los usuarios en EMPOPASTO.""")
        
    pregunta5_2_barrio = df.filter((pl.col("variable") == "pregunta5_2") & (pl.col("value") != 0) & (pl.col("value") < 3)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
        )
    fig = px.bar(pregunta5_2_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas de 1 y 2 por barrio, tipo de servicio y estrato")
    st.plotly_chart(fig, theme="streamlit", width="stretch")


st.markdown("""En la evaluación sobre si los usuarios han presentado una PQRS, el :blue[79,8 %] respondió No, mientras que el :green[20.2 %] indicó que Sí.
    Este resultado refleja que solo una quinta parte de los usuarios ha interactuado con los canales de atención, lo que puede interpretarse como un bajo nivel de reclamos —aunque también podría indicar limitado conocimiento o uso del sistema PQRS, especialmente en los estratos más bajos.  
    Entre quienes sí presentaron PQRS, el :blue[48.4 %] calificó la orientación recibida como satisfactoria o muy satisfactoria, el 28,2 % se mantuvo neutral, y el :red[23.35 %] manifestó insatisfacción.  
    Los estratos con mayor participación fueron los Bajo, Medio-Bajo y Bajo-Bajo, donde los usuarios destacan la buena disposición del personal, pero solicitan mayor claridad en los pasos del proceso y tiempos de respuesta.  
    Respecto a la calidad de la respuesta recibida (Pregunta 5.2), el :blue[41.6 %] mantiene una percepción positiva, el :green[30.5%] se declara neutral y el :red[28%] considera que la respuesta fue insatisfactoria o poco útil.  
    La baja proporción de usuarios que presentan PQRS (20,2 %) sugiere una gestión operativa estable, pero también la necesidad de ampliar el conocimiento ciudadano sobre sus derechos y canales de atención.  
    Los niveles de satisfacción con la orientación (48,4 %) y la respuesta final (41,6 %) están por debajo de la meta institucional del 90 %, mostrando que el proceso de atención requiere mayor seguimiento, empatía y cierre efectivo.  
    La brecha entre orientación y respuesta (≈7 puntos porcentuales) indica que los usuarios perciben buena disposición inicial, pero falta cumplimiento o solución efectiva al final del trámite.
    """)


st.subheader("### ¿Ha solicitado revisión interna en su inmueble?")
st.badge("Seguridad" )
col1, col2 = st.columns(2)
with col1:
    pregunta6 = df2.filter(pl.col("variable") == "pregunta6")
    pregunta6 = pregunta6.group_by(["Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(pregunta6, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por tipo de servicio")
    st.plotly_chart(fig, width="stretch")
    st.markdown("**¿cómo califica la atención recibida?**")
    p6_1_ns = df3.filter(pl.col("variable") == "pregunta6_1")
    fig = px.bar(p6_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
    fig.update_layout(
    # Ajusta el espacio entre los GRUPOS (Pregunta A vs Pregunta B)
    bargap=0.2,  
    # Ajusta el espacio entre las barras DENTRO de un grupo (2023 vs 2024)
    bargroupgap=0.05, 
    # Mueve la leyenda si es necesario
    legend_title_text='Año'
    )
    st.plotly_chart(fig, theme="streamlit", width="stretch")

    
    pregunta6_1 = df.filter((pl.col("variable") == "pregunta6_1") & (pl.col("value") != 0))
    grafico6_1 = pregunta6_1.group_by(["Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )

    fig = px.pie(grafico6_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")


with col2:
    pregunta6_barrio = df2.filter((pl.col("variable") == "pregunta6") & (pl.col("value") == "SI")).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(pregunta6_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas positivas (Si) por barrio, tipo de servicio y estrato")
    st.plotly_chart(fig, width="stretch")

    st.markdown("** **")

    st.markdown("""El indicador de 2025 (71,79%) indica un desempeño moderado, pero por debajo de estándares aceptables para el sector público, donde lo esperado es ≥ 90%.  
    **El patrón refleja:**  
    :material/arrow_right: debilidad en la capacidad de respuesta técnica,  
    :material/arrow_right: falta de oportunidad en la atención en ciertos barrios,  
    :material/arrow_right: percepción de que las revisiones no solucionan el problema de raíz,  
    :material/arrow_right: insuficiente difusión del servicio, especialmente en estratos bajos.  
    El hecho de que 2025 no haya presentado una mejora sustancial confirma que las acciones implementadas no han sido lo suficientemente efectivas o no han abarcado los sectores críticos.
    
    """)

    grafico6_1_barrio = pregunta6_1.filter((pl.col("value") != 0) & (pl.col("value") < 3)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(grafico6_1_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas de 1 - 2 por barrio, tipo de servicio y estrato")
    st.plotly_chart(fig, width="stretch")

st.markdown("""Se observa que el :blue[80.7 %] de los usuarios no ha solicitado revisión interna de su inmueble, mientras que el :green[19.3 %] sí ha requerido este servicio.
De este grupo, el :blue[75,65 %] pertenece al sector residencial y el :green[23 %] al sector comercial, lo que evidencia una mayor demanda de atención técnica en viviendas particulares.  
En el tipo residencial, los barrios con mayor número de solicitudes son La Cruz (5,17 %) y Cantarana (4,31 %); mientras que en el tipo comercial destacan Las Américas, El Tejar, Caracha, Sendoya y Santa Mónica.  
Esta distribución muestra que las solicitudes se concentran en barrios que, en otras preguntas, ya habían reportado dificultades en la presión y continuidad del agua, evidenciando una relación directa entre problemas operativos y necesidad de revisiones internas.  
La baja proporción de usuarios que solicitan revisión (19,3 %) indica que la mayoría no ha tenido necesidad de requerir soporte técnico, lo cual puede interpretarse positivamente en términos de estabilidad del servicio.  
Sin embargo, también puede reflejar desconocimiento del servicio o limitado acceso a los canales de solicitud, especialmente en los estratos residenciales bajos.  
Este bloque de preguntas refleja la capacidad de respuesta operativa y técnica de Empopasto, tanto en disponibilidad del servicio como en la calidad de la atención brindada.  
La satisfacción del :blue[64,7 %] indica que el servicio es funcional pero no sobresaliente, y que aún no se logra consolidar una atención uniforme y eficiente.  
La presencia de neutralidad (:green[13,7 %]) sugiere que hay usuarios que no perciben una diferencia clara entre un buen y mal servicio, lo que puede mejorarse mediante protocolos de atención más visibles y estandarizados.
""")

st.markdown("### ¿Durante el año 2024 le suspendieron el servicio de acueducto?")
st.badge("Capacidad de respuesta")

pregunta7 = df2.filter(
    pl.col("variable") == "pregunta7"
)

pregunta7_1 = df.filter(
    pl.col("variable") == "pregunta7_1"
).filter(
    pl.col("value") != 0
)

pregunta7_1_bajo = df.filter(
    (pl.col("variable") == "pregunta7_1") & (pl.col("value") != 0)
)

pregunta7_1_bajo = pregunta7_1_bajo.filter(
    pl.col("value") < 3
)

graficop7 = pregunta7.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
    )
fig = px.bar(graficop7, x="Desc Subcategoria", y="count", color="value", barmode="group",
facet_col="Desc Categoria", color_discrete_sequence=["#8B0000","#006400"], height=400, title="Respuestas por tipo de servicio y estrato")
st.plotly_chart(fig, width="stretch")

st.markdown("**Si la respuesta es SI   y teniendo en cuenta que, por normatividad, EMPOPASTO cuenta con 24 horas hábiles para la reinstalación del servicio ¿Cómo califica usted el tiempo entre la suspensión y la reinstalación?**")

p7_1_ns = df3.filter(pl.col("variable") == "pregunta7_1")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p7_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#8B0000", "#FFD700"], height=400)
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
        st.markdown("""El indicador presenta una tendencia variable, con una caída significativa en 2024 y una recuperación parcial en 2025, aunque aún sin alcanzar los niveles de 2023.  
    Esto muestra que los usuarios han tenido percepciones fluctuantes en relación con los tiempos de reconexión después de la suspensión del servicio.  
    :material/arrow_right: Se evidencia una recuperación parcial en 2025 (+6.24 puntos porcentuales), lo cual indica una mejora operativa o una mejor comunicación con los usuarios.  
    :material/arrow_right: Aunque la percepción mejora, no logra volver al nivel observado en 2023 (-2.86 puntos porcentuales).""")


col5, col6 = st.columns(2)
with col6:
    graficop7_1_bajo = pregunta7_1_bajo.group_by("Barrio").agg(
        pl.len().alias("count")
    ).sort("count", descending=True)
    fig = px.bar(graficop7_1_bajo, x="Barrio", y="count",  title="Barrios con calificacion baja", color="Barrio", color_discrete_sequence=["#006400","#006400", "#228B22","#228B22","#99EE99", "#99EE99","#FFD700","#FFD700","#FF4444","#FF4444","#CC0000","#CC0000","#8B0000", "#8B0000"], height=400)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")

with col5:
    grafico7_1 = pregunta7_1.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico7_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

st.markdown("""El **:blue[87,2 %]** de la población cumple oportunamente con sus obligaciones con Empopasto, mientras que el **:red[12,8 %]** presenta incumplimientos que derivan en suspensión del servicio.  
En cuanto al tiempo transcurrido entre la suspensión y la reinstalación, el **:blue[58,5 %]** de los usuarios califica el tiempo como adecuado, el **:blue[24,7 %]** se mantiene neutral, y el **:blue[16,85 %]** considera que el proceso fue inadecuado.  
Estos resultados reflejan que el proceso de reinstalación cumple con las expectativas de la mayoría de los usuarios, aunque no se alcanza la meta sugerida del 90 % de satisfacción.  
Adicionalmente, los barrios con mayor número de inconformidades corresponden principalmente a estratos Bajo-Bajo, Bajo y Medio-Bajo, destacándose Agualongo y La Cruz, donde se concentran los casos de demoras o dificultades en la reconexión.""")

st.markdown("### Califique si las Instalaciones de Empopasto S.A. E.S.P. son adecuadas para atender a los usuarios.")
st.badge("Elementos Tangibles")

pregunta8 = df.filter((pl.col("variable") == "pregunta8")&(pl.col("value") != 0))

p8_ns = df3.filter(pl.col("variable") == "pregunta8")
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p8_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#8B0000", "#FFD700"], height=400)
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
        st.markdown("""El indicador de instalaciones físicas, con un **:blue[74,65 %]**, muestra un desempeño aceptable pero no sobresaliente.  
        El usuario reconoce que las instalaciones son funcionales, pero no excelentes ni totalmente alineadas con estándares modernos de servicio al ciudadano.  
        Dado que los tangibles influyen directamente en la percepción final de la calidad del servicio, este componente debe considerarse prioritario para:  
        :material/arrow_right: mejoras estructurales,  
        :material/arrow_right: actualizaciones de señalización,  
        :material/arrow_right: accesibilidad  
        y reorganización de espacios.  
        Este resultado permite establecer acciones claras y medibles para los próximos ciclos de evaluación.""")


col1, col2, col3= st.columns(3)
with col1:
    pregunta8 = pregunta8.group_by(["Barrio",'Desc Categoria','Desc Subcategoria','value']).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)
    fig = px.pie(pregunta8, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.bar(pregunta8, x="value", y="count", color="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por estrato")
    st.plotly_chart(fig, width="stretch")

with col3:
    p8_bajo = pregunta8.filter(pl.col('value') < 3)
    fig = px.bar(p8_bajo, x="Barrio", y="count", color="value",facet_col="Desc Categoria" ,color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas 1 o 2 por barrio y tipo de servicio")
    st.plotly_chart(fig, width="stretch")
st.markdown("""
    Con respecto a la percepción de los usuarios sobre las instalaciones físicas de EMPOPASTO, el :blue considera que estas son adecuadas, calificando su experiencia como satisfecho o muy satisfecho.  
    Sin embargo, este resultado no alcanza la meta recomendada del 90 % para entidades públicas, lo que evidencia una brecha significativa entre la percepción actual y el estándar esperado.  
    La población que más interactúa y califica este aspecto pertenece principalmente al sector residencial, especialmente en los estratos Bajo, Medio-Bajo y Bajo-Bajo, lo que sugiere que la percepción de la infraestructura está fuertemente influenciada por los usuarios con menos acceso a servicios informativos y que dependen más de la atención presencial.""")

st.markdown("### ¿Usted se ha comunicado con EMPOPASTO a través del canal telefónico?")
st.badge("Elementos Tangibles")
col1, col2= st.columns(2)
with col1:
    grafica9 = df2.filter(pl.col("variable") == "pregunta9")
    grafica9 = grafica9.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafica9, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")

with col2:
    pregunta9 = df2.filter(pl.col("variable") == "pregunta9")
    pregunta9 = pregunta9.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(pregunta9, x="value", y="count", color="Desc Categoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por estrato")
    st.plotly_chart(fig, width="stretch")

p9_1_ns = df3.filter(pl.col("variable") == "pregunta9_1")

st.markdown("**¿cómo califica la atención recibida?**")
col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p9_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
        st.markdown("""El resultado de 75,53% constituye una base importante para medir el avance en próximas encuestas. Aunque el servicio tiene buena aceptación, existe una brecha cercana de 14,5 puntos respecto a la meta del 90%.  
    Es fundamental priorizar este canal por su importancia en:  
    :material/arrow_right: Resolución rápida de problemas,  
    :material/arrow_right: Evitar congestión en puntos presenciales,  
    :material/arrow_right: Facilitar el acceso a usuarios de mayor edad o zonas alejadas,  
    :material/arrow_right: Mejorar la percepción general de la empresa sin depender del contacto físico.""")
    
col4, col5 = st.columns(2)
with col4:
    pregunta9_1 = df.filter((pl.col("variable") == "pregunta9_1") & (pl.col("value") != 0))
    pregunta9_1 = pregunta9_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.pie(pregunta9_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas")
    st.plotly_chart(fig, width="stretch")


    pregunta9_1_barrio_bajo = df.filter((pl.col("variable") == "pregunta9_1") & (pl.col("value") < 3) & (pl.col("value") != 0)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(pregunta9_1_barrio_bajo, x="Barrio", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas bajas por barrio y Estrato")
    st.plotly_chart(fig, width="stretch")

with col5:
    
    pregunta9_1_barrio = df.filter((pl.col("variable") == "pregunta9_1") & (pl.col("value") != 0)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(pregunta9_1_barrio, x="Barrio", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas por barrio y Estrato")
    st.plotly_chart(fig, width="stretch")

    fig2 = px.bar(pregunta9_1_barrio_bajo, x="Barrio", y="count", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400, title="Respuestas bajas por barrio y Tipo de servicio")
    st.plotly_chart(fig2, width="stretch")

st.markdown("""En la evaluación sobre el uso de la línea telefónica, el :blue[84.3%] de los usuarios informó que no ha utilizado este medio, mientras que el :green[15.7%] sí lo ha utilizado.  
Esto evidencia que el canal telefónico no es el principal medio de contacto, posiblemente porque los usuarios prefieren la atención presencial, canales digitales o no han tenido necesidad de comunicarse.  
Entre quienes sí han utilizado la línea telefónica, el :blue[75.3%] calificó la atención como satisfactoria o muy satisfactoria, el :green[16.5%] se mantuvo en una postura neutral, y solo el :red[8.23%] expresó insatisfacción.  
Esta distribución muestra que el canal telefónico, aunque poco utilizado, funciona bien para la mayoría, pero aún tiene un grupo minoritario que no percibe una atención adecuada.  
Dentro del grupo que calificó el servicio negativamente (8,23 %), se observa:  
    :material/arrow_right: Sector residencial: 71,4 % de las respuestas insatisfactorias.  
    :material/arrow_right: Sector comercial: 28,6 %.  
**Barrios residenciales con mayor concentración de insatisfacción:**  
    :material/arrow_right: Panorámico Primera Etapa  
    :material/arrow_right: La Colina  
    :material/arrow_right: El Tejar  
    :material/arrow_right: Sendoya  
    :material/arrow_right: Villa Recreo  
Estos barrios se agrupan principalmente en estratos Bajo, Medio y Medio-Bajo, lo que puede indicar:  
barreras de comunicación (tiempos de espera, cortes, poca claridad), dificultades para acceder al servicio telefónico, o necesidad de mayor cercanía en la atención (empatía, claridad, orientación).  
**En el sector comercial, los barrios que reportan insatisfacción son:**  
    :material/arrow_right: Atahualpa  
    :material/arrow_right: Las Américas  
Esto puede estar relacionado con necesidades más urgentes de atención debido a afectación operativa (negocios, atención a clientes, horarios estrictos).  
""")

