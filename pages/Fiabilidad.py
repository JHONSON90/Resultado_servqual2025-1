from turtle import color
import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Fiabilidad", layout="wide")

df = pl.read_csv("Formatos_Listos/Cuantitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Int64}, ignore_errors=True)
df2 = pl.read_csv("Formatos_Listos/Cualitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.String}, ignore_errors=True)
df3 = pl.read_csv("Formatos_Listos/para_niv_satisfaccion.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Float64}, ignore_errors=True)


st.title(":blue[Fiabilidad]")
st.text("Cumplimiento del servicio prometido de manera precisa y confiable.")

df = df.filter(pl.col("Categoria") == "Fiabilidad")

#df2 = df2.filter(pl.col("Categoria") == "Fiabilidad")


st.subheader("¿Usted considera que el tiempo de entrega de su factura, hasta la fecha límite de pago de la misma, es adecuado?")

pregunta1 = df.filter(pl.col("variable") == "pregunta1")

p1_ns = df3.filter(pl.col("variable") == "pregunta1")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#8B0000", "#FFD700"], height=400)
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
    st.text("Total de respuestas")
    graficap1 = pregunta1.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(graficap1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

    st.markdown("""El **:blue[87,2 %]** de los usuarios califica positivamente el tiempo de entrega de la factura, siendo el **:blue[61,5 %]** satisfecho y el **:blue[25,7 %]** muy satisfecho. 
    Solo un **:red[12,8 %]** manifiesta inconformidad, lo que indica que el proceso de distribución de facturas cumple con las expectativas de la mayoría de los usuarios.""")

with col2:    
    st.metric("Meta Sugerida", "≥ 90%", border=True)
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
    st.subheader("Evaluacion de calificaciones bajas por Tipo")
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

st.header("¿Cómo califica la información contenida en la factura de pago en términos de facilidad para comprenderla?")

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
    st.subheader("Valoracion de la pregunta")
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
    st.markdown("""**:blue[Análisis detallado:]**  
    Los usuarios que encuentran la factura difícil de comprender mencionan dos causas principales:  
    :material/arrow_right: 60 % no conoce el significado o detalle de los conceptos facturados.  
    :material/arrow_right: 12,5 % no comprenden la inclusión del servicio de aseo, lo que evidencia una brecha de información sobre la normatividad o convenios interinstitucionales.  
    Estos resultados apuntan a una necesidad de fortalecer la comunicación educativa al usuario sobre la estructura y conceptos de cobro en la factura.""")

with col4:
    st.subheader("Razones de la valoracion negativa")

    pregunta2_baja = pregunta2.filter(pl.col("value") < 4)
    pregunta2_baja = pregunta2_baja.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    ).sort("value", descending=True)

    fig = px.bar(pregunta2_baja, y="count", x="Desc Categoria", color="Desc Subcategoria", hover_name="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

    grafico2_1 = pregunta2_1.group_by("value").agg(
        pl.len().alias("count")
    ).sort("value", descending=True)
    fig = px.bar(grafico2_1, y="value", x="count", color="value", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")

st.subheader("¿Conoce los sitios de pago de su factura?")

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
    fig = px.pie(grafico3, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col16:
    pregunta3_baja = pregunta3.filter(pl.col("value") == "NO")
    grafico3_1 = pregunta3_baja.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico3_1, y="count", x="Desc Categoria", color="Desc Subcategoria", hover_name="Desc Subcategoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown("""La población, además de mostrar un alto nivel de cumplimiento con sus obligaciones hacia Empopasto, también demuestra un conocimiento generalizado de los puntos donde puede realizar el pago de su factura.  
El :blue[94,8 %] de los usuarios conoce los lugares de pago, mientras que existe una brecha del :red[5,17 %] que desconoce los puntos habilitados.  
Este grupo minoritario se concentra principalmente en los usuarios residenciales de estratos Bajo y Medio-Bajo, sectores donde persisten dificultades de acceso a información digital o puntos físicos más alejados por lo que requieren mecanismos más accesibles de información y orientación presencial, especialmente en barrios con baja conectividad o alfabetización digital.
""")



st.subheader("¿Durante el año 2024 le suspendieron el servicio de acueducto?")


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
facet_col="Desc Categoria", color_discrete_sequence=["#8B0000","#006400"], height=400)
st.plotly_chart(fig, width="stretch")

st.subheader("Si la respuesta es SI   y teniendo en cuenta que, por normatividad, EMPOPASTO cuenta con 24 horas hábiles para la reinstalación del servicio ¿Cómo califica usted el tiempo entre la suspensión y la reinstalación?")

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
    fig = px.pie(grafico7_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown("""El **:blue[87,2 %]** de la población cumple oportunamente con sus obligaciones con Empopasto, mientras que el **:red[12,8 %]** presenta incumplimientos que derivan en suspensión del servicio.  
En cuanto al tiempo transcurrido entre la suspensión y la reinstalación, el **:blue[58,5 %]** de los usuarios califica el tiempo como adecuado, el **:blue[24,7 %]** se mantiene neutral, y el **:blue[16,85 %]** considera que el proceso fue inadecuado.  
Estos resultados reflejan que el proceso de reinstalación cumple con las expectativas de la mayoría de los usuarios, aunque no se alcanza la meta sugerida del 90 % de satisfacción.  
Adicionalmente, los barrios con mayor número de inconformidades corresponden principalmente a estratos Bajo-Bajo, Bajo y Medio-Bajo, destacándose Agualongo y La Cruz, donde se concentran los casos de demoras o dificultades en la reconexión.""")

st.subheader("¿Cómo califica la calidad de agua que recibe de EMPOPASTO?")

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
, height=400)
    st.plotly_chart(fig, width="stretch")

with col8:
    grafico10_1 = pregunta10.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    ).sort("count", descending=True)
    fig = px.bar(grafico10_1, x="Desc Subcategoria", y="count", color="value", barmode="relative", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"]
, height=400)
    st.plotly_chart(fig, width="stretch")


st.markdown("""El :blue[92,7 %] de la población se encuentra satisfecha con la calidad del agua que recibe de Empopasto, mientras que el :red[7,3 %] expresa algún nivel de inconformidad.  
Estos resultados reflejan una alta percepción positiva de los usuarios respecto al producto principal que ofrece la empresa **el agua potable** evidenciando que los estándares de tratamiento, potabilidad y continuidad del servicio son reconocidos favorablemente por la comunidad.""")

st.subheader("¿Empopasto le brinda información de manera anticipada sobre las suspensiones del servicio en su sector? ")
pregunta11 = df2.filter(pl.col("variable") == "pregunta11")

col9, col10, col11 = st.columns(3)
with col9:
    grafico11 = pregunta11.group_by("value").agg(
        pl.len().alias("count")
    )
    fig = px.pie(grafico11, names="value", values="count", color_discrete_sequence=["#006400","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
with col10:
    st.text("Estratos mas representativos")
    grafico11_estrato = pregunta11.filter(pl.col("value") == "NO").group_by("Desc Subcategoria").agg(
        pl.len().alias("count")
    )
    st.write(grafico11_estrato)
with col11:
    st.subheader("Barrios que generan inconformidades")
    grafico11_barrio = pregunta11.filter(pl.col("value") == "NO").group_by("Barrio").agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico11_barrio, y="Barrio", x="count", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    
st.subheader("Si la respuesta es Si, califique si la información y el tiempo de aviso previo a la suspensión del servicio de agua son adecuados")



pregunta11_1 = df.filter(pl.col("variable") == "pregunta11_1").filter(pl.col("value") != 0)
p11_1_ns = df3.filter(pl.col("variable") == "pregunta11_1")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(p11_1_ns, x="variable", y=["2023", "2024", "2025"], barmode="group", text_auto=True, title="Nivel de satisfaccion", color_discrete_sequence=["#006400","#FFD700","#8B0000"], height=400)
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
    fig = px.pie(grafico11_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

with col13:
    grafico11_1_estrato = pregunta11_1.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico11_1_estrato, x="Barrio", y="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown("""Se evidencia que el :blue[68.2 %] de la población recibe información previa sobre las suspensiones del servicio, mientras que el :red[31.8 %] manifiesta no ser informada oportunamente.
Este resultado refleja un avance positivo en los canales de comunicación, aunque aún existen brechas de cobertura informativa, especialmente en algunos barrios y estratos socioeconómicos.

Dentro del grupo que no recibe la información (31,8 %), destacan los barrios Atahualpa, Ocho de Marzo, Las Américas y Bellavista, pertenecientes principalmente a los estratos Único, Bajo, Medio-Bajo y Bajo-Bajo.
En cuanto al tiempo de aviso previo, el :blue[90.9 %] de los usuarios considera que este es adecuado, y solo un :red[9.1 %] lo califica como inadecuado.
Las inconformidades provienen principalmente de los barrios Agualongo, San Juan de Dios, Miraflores, Caicedo Alto, Ocho de Marzo, Manantial y Niza II.
""")

st.subheader("Considera Usted, que la continuidad del servicio que presta EMPOPASTO es:")
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
    fig = px.pie(grafico12, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    
with col15:
    grafico12_barrio = pregunta12.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico12_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown("""En cuanto a la continuidad del servicio, el :blue[90,5 %] de la población considera que el suministro de agua es adecuado, superando por 0,5 puntos porcentuales la meta sugerida del 90 %.  
Por otro lado, el :red[9,5 %] manifiesta que el servicio no es continuo o presenta interrupciones ocasionales.  
Las principales inconformidades se concentran en los barrios Agualongo, Panamericano, La Carolina y Caicedo Alto, donde los usuarios reportan cortes esporádicos o disminución temporal del caudal.
    """)

st.subheader("La presión de agua en su inmueble o en su vivienda es?")


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
    fig = px.pie(grafico13, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
with col17:
    grafico13_barrio = pregunta13.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico13_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown("""En relación con la presión del agua, el :blue[90.7 %] de los usuarios manifiesta estar satisfecho con la presión del servicio recibido, lo que representa un resultado positivo y coherente con la percepción favorable sobre la continuidad del servicio (:blue[90,5 %] en la pregunta anterior).
Este desempeño es destacable considerando las condiciones geográficas y topográficas del municipio de Pasto, que naturalmente pueden generar variaciones en la presión en algunos sectores.

No obstante, un :red[9.3 %] de los usuarios considera que la presión es baja o inadecuada, identificándose principalmente los barrios La Floresta, Chambú, Quintas de San Pedro, San Vicente, Panorámico II Etapa y La Cruz.
En estos sectores se reportan cortes esporádicos o disminución temporal del caudal, lo que sugiere relación directa entre interrupciones parciales y presión insuficiente.
""")




# st.subheader("Recomendaciones")
# st.markdown("""1. Mantener la eficiencia en la entrega actual, pero revisar casos donde se presentan demoras.  
# 2. Considerar campañas informativas sobre canales digitales de consulta de factura para mejorar aún más la percepción.  
# 3. Elaborar una guía gráfica impresa y digital explicando cada sección de la factura y los conceptos facturados, con un lenguaje adaptado según estrato.  
# 4. En los barrios de estrato bajo y bajo-bajo, realizar campañas informativas presenciales o a través de las juntas de acción comunal, enfocadas en la interpretación de la factura y la justificación del cobro de aseo.
# 5. Integrar en la página web y redes sociales una sección “Entienda su factura” con ejemplos interactivos y videos explicativos.  
# 6. Monitorear en la próxima encuesta el cambio en la percepción de comprensión por estrato, para medir el impacto de las acciones educativas.  
# 7. Identificar causas específicas de demora en barrios de estratos Bajo-Bajo y Bajo mediante visitas técnicas o revisión de registros de órdenes de trabajo.  
# 8. Optimizar los procesos de validación y reconexión, especialmente en sectores con alta densidad de usuarios, para acercarse al cumplimiento del 90 % de satisfacción.  
# 9. Implementar recordatorios previos de pago (SMS, WhatsApp, correo electrónico) para reducir el número de suspensiones.  
# 10. Mantener los estándares actuales de tratamiento y monitoreo, reforzando la comunicación de resultados de calidad del agua a la ciudadanía.  
# 11. Implementar una estrategia informativa trimestral, publicando en medios y redes sociales los informes de calidad del agua (color, turbiedad, cloro residual, bacteriología), para fortalecer la confianza del usuario.  
# 12. Realizar un seguimiento geográfico a los sectores donde se reportó insatisfacción (7,3 %), verificando posibles afectaciones localizadas o variaciones temporales  
# 13. Ampliar los canales de comunicación, incluyendo:  
#     :material/arrow_right: Publicaciones más frecuentes en emisoras comunitarias y carteleras barriales.  
#     :material/arrow_right: Mensajería instantánea (WhatsApp o SMS) a los usuarios registrados.  
#     :material/arrow_right: Sincronización con líderes comunitarios para avisos presenciales en barrios vulnerables.  
# 14.  Verificar la cobertura digital y radial en barrios con menor nivel de información (Atahualpa, Las Américas, Bellavista, Ocho de Marzo) y ajustar la estrategia de difusión.
# 15. Monitorear los barrios críticos identificados (Agualongo, San Juan de Dios, Miraflores, Caicedo Alto, Manantial, Niza II) para asegurar que los avisos se emitan con antelación mínima de 24 horas hábiles.  
# 16. Mantener la operación actual, reforzando el seguimiento a los sectores que reportan variaciones en la continuidad (Agualongo, Panamericano, La Carolina y Caicedo Alto).  
# 17. Implementar un monitoreo georreferenciado de interrupciones, permitiendo detectar rápidamente zonas con fallas recurrentes.  
# 18. Comunicar proactivamente los motivos de cortes programados a los usuarios de los barrios mencionados, para fortalecer la confianza y percepción de transparencia.  
# 19. Verificar la presión en campo mediante mediciones en los barrios con mayores reportes de baja presión (La Floresta, Chambú, Quintas de San Pedro, San Vicente, Panorámico II Etapa y La Cruz).  
# 20. Implementar un plan de mantenimiento preventivo de válvulas, redes secundarias y estaciones de bombeo en sectores de altitud elevada.  
# 21. Mantener la comunicación activa con los usuarios afectados, informando causas y acciones correctivas para fortalecer la confianza.
# 22. Fortalecer la gestión de cuadrillas operativas, priorizando los casos según impacto comunitario y nivel de afectación.  
# 23. Establecer un protocolo estandarizado de comunicación con los usuarios y comerciantes cuando se realicen obras, informando plazos y avances.  
# 24. Implementar un sistema de cierre de obras (físico y digital) que asegure que cada intervención quede completamente terminada y con el entorno restablecido.  
# 25. Diseñar un plan de mantenimiento preventivo trimestral, especialmente en sectores residenciales que reportan demoras o falta de atención.

# """)


