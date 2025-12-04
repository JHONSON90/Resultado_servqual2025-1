
import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Empatía", layout="wide")

st.title(":blue[Empatía]")

df = pl.read_csv("Formatos_Listos/Cuantitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Int64}, ignore_errors=True)
df2 = pl.read_csv("Formatos_Listos/Cualitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.String}, ignore_errors=True)
df3 = pl.read_csv("Formatos_Listos/para_niv_satisfaccion.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Float64}, ignore_errors=True)

df = df.filter(pl.col("Categoria") == "Empatía")

st.subheader("La atención que Usted recibe en nuestros puntos, ha sido:")

col1, col2, col3 = st.columns(3)
with col1:
    p4_1_ns = df3.filter(pl.col("variable") == "pregunta4_1")
    fig = px.bar(p4_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
    fig = px.bar(p4_2_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
    fig = px.bar(p4_3_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
    pregunta4_1 = df.filter((pl.col("variable") == "pregunta4_1") & (pl.col("value") != 0))
    pregunta4_1 = pregunta4_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.pie(pregunta4_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
with col2:
    fig = px.bar(pregunta4_1, x="value", y="count", color="Desc Categoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col3:
    fig = px.bar(pregunta4_1, x="value", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")



pregunta4_2 = df.filter((pl.col("variable") == "pregunta4_2") & (pl.col("value") != 0))
pregunta4_2 = pregunta4_2.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
)

col1, col2, col3 = st.columns(3)
with col1:
    fig = px.pie(pregunta4_2, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.bar(pregunta4_2, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col3:
    fig = px.bar(pregunta4_2, x="value", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

pregunta4_3 = df.filter((pl.col("variable") == "pregunta4_3") & (pl.col("value") != 0))
pregunta4_3 = pregunta4_3.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
)

col1, col2, col3 = st.columns(3)
with col1:
    fig = px.pie(pregunta4_3, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.bar(pregunta4_3, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col3:
    fig = px.bar(pregunta4_3, x="value", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
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
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""Al analizar los tres componentes de la atención en los puntos de servicio, se evidencia una alta aceptación por parte de los usuarios.  
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

st.subheader("¿Usted se ha comunicado con EMPOPASTO a través del canal telefónico?")
col1, col2, col3 = st.columns(3)
with col1:
    grafica9 = df2.filter(pl.col("variable") == "pregunta9")
    grafica9 = grafica9.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafica9, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col2:
    pregunta9 = df2.filter(pl.col("variable") == "pregunta9")
    pregunta9 = pregunta9.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(pregunta9, x="value", y="count", color="Desc Categoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

p9_1_ns = df3.filter(pl.col("variable") == "pregunta9_1")

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


with col3:
    pregunta9_1 = df.filter((pl.col("variable") == "pregunta9_1") & (pl.col("value") != 0))
    pregunta9_1 = pregunta9_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(pregunta9_1, x="value", y="count", color="value", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
col4, col5, col6 = st.columns(3)
with col4:
    pregunta9_1 = df.filter((pl.col("variable") == "pregunta9_1") & (pl.col("value") != 0))
    pregunta9_1 = pregunta9_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.pie(pregunta9_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col5:
    pregunta9_1_barrio = df.filter((pl.col("variable") == "pregunta9_1") & (pl.col("value") < 3) & (pl.col("value") != 0)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(pregunta9_1_barrio, x="Barrio", y="count", color="value", facet_col="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col6:
    fig2 = px.bar(pregunta9_1_barrio, x="Barrio", y="count", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
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

st.subheader("Se ha visto afectado por los trabajos adelantados por EMPOPASTO?")
pregunta15 = df2.filter(pl.col("variable") == "pregunta15")
pregunta15 = pregunta15.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
    pl.len().alias("count")
)
col1, col2 =st.columns(2)
with col1:
    fig = px.pie(pregunta15, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400)
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

    fig = px.bar(pregunta15_1_confg, y="Pregunta", x="Contestacion", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
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


# st.subheader("Recomendaciones")
# st.markdown("""
# 1. Fortalecer procesos internos que impacten la agilidad, especialmente en horas de alta demanda.  
# 2. Implementar un sistema de filas y turnos más eficiente, si no existe, o mejorar el actual.  
# 3. Realizar microcapacitaciones al personal para optimizar actividades repetitivas y reducir tiempos muertos.  
# 4. Analizar en detalle qué trámites son más lentos y aplicar mejoras puntuales.  
# 5. Fortalecer la empatía en la atención telefónica, enfocando la capacitación del personal en claridad, tono, escucha activa y solución al primer contacto.  
# 6. Reducir tiempos de espera, ya que este es uno de los factores más comunes detrás de la insatisfacción en líneas de atención.  
# 7. Implementar un sistema de calificación inmediata post-llamada (“¿Cómo calificas tu atención?”) para obtener retroalimentación en tiempo real.  
# 8. Mantener la eficiencia en la entrega actual, pero revisar casos donde se presentan demoras. 
# 9. Mejorar la comunicación anticipada mediante mensajes en la factura, perifoneo y redes sociales sobre intervenciones programadas.  
# 10. Implementar señalización clara durante obras, evitando cierres totales cuando sea posible, y coordinando con la Secretaría de Movilidad.  
# 11. Planificar trabajos en horarios de menor tránsito o en fases alternadas para reducir el impacto en la movilidad.  
# 12. Protocolos especiales para zonas comerciales, coordinando horarios que no afecten horarios pico de ventas.  
# 13. Monitorear semanalmente las afectaciones reportadas a través de un módulo en Power BI para medir mejora trimestral.  
# 14. Realizar estudios de impacto urbano en los barrios donde se repiten los cierres más prolongados.  

# """)




# st.write(df.select("variable").unique())

