import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Capacidad de Respuesta", layout="wide")

st.title(":blue[Capacidad de Respuesta]")

df = pl.read_csv("Formatos_Listos/Cuantitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Int64}, ignore_errors=True)
df2 = pl.read_csv("Formatos_Listos/Cualitativas.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.String}, ignore_errors=True)
df3 = pl.read_csv("Formatos_Listos/para_niv_satisfaccion.csv", separator=",", encoding="utf-8", schema_overrides={"value": pl.Float64}, ignore_errors=True)


df = df.filter(pl.col("Categoria") == "Capacidad de respuesta")

st.subheader(" ¿Durante el año pasado, Usted presentó una petición, una queja, reclamo, sugerencia o una denuncia (PQRS)?")
pregunta5 = df2.filter(pl.col("variable") == "pregunta5")

grafico5 = pregunta5.group_by(["Desc Categoria", "value"]).agg(
    pl.len().alias("count")
)
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
with col2:
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""El resultado de 66,13% muestra que la orientación en la atención de PQRS no cumple con las expectativas de los usuarios, y debe considerarse un indicador prioritario para el plan de mejora.  
    Este valor servirá como línea base para medir avances en los próximos años.  
    Acciones como mejorar la trazabilidad del proceso, la claridad de la información y la capacitación del personal ayudarán a incrementar este indicador hacia niveles óptimos.""")
    


col1, col2, col3 = st.columns(3)
with col1:
    fig = px.bar(grafico5, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown("""En la evaluación sobre si los usuarios han presentado una PQRS, el :blue[79,8 %] respondió No, mientras que el :green[20.2 %] indicó que Sí.
    Este resultado refleja que solo una quinta parte de los usuarios ha interactuado con los canales de atención, lo que puede interpretarse como un bajo nivel de reclamos —aunque también podría indicar limitado conocimiento o uso del sistema PQRS, especialmente en los estratos más bajos.  
    Entre quienes sí presentaron PQRS, el :blue[48.4 %] calificó la orientación recibida como satisfactoria o muy satisfactoria, el 28,2 % se mantuvo neutral, y el :red[23.35 %] manifestó insatisfacción.  
    Los estratos con mayor participación fueron los Bajo, Medio-Bajo y Bajo-Bajo, donde los usuarios destacan la buena disposición del personal, pero solicitan mayor claridad en los pasos del proceso y tiempos de respuesta.  
    Respecto a la calidad de la respuesta recibida (Pregunta 5.2), el :blue[41.6 %] mantiene una percepción positiva, el :green[30.5%] se declara neutral y el :red[28%] considera que la respuesta fue insatisfactoria o poco útil.  
    La baja proporción de usuarios que presentan PQRS (20,2 %) sugiere una gestión operativa estable, pero también la necesidad de ampliar el conocimiento ciudadano sobre sus derechos y canales de atención.  
    Los niveles de satisfacción con la orientación (48,4 %) y la respuesta final (41,6 %) están por debajo de la meta institucional del 90 %, mostrando que el proceso de atención requiere mayor seguimiento, empatía y cierre efectivo.  
    La brecha entre orientación y respuesta (≈7 puntos porcentuales) indica que los usuarios perciben buena disposición inicial, pero falta cumplimiento o solución efectiva al final del trámite.
    """)


with col2:
    pregunta5_1 = df.filter((pl.col("variable") == "pregunta5_1") & (pl.col("value") != 0))
    grafico5_1 = pregunta5_1.group_by(["Desc Categoria", "value"]).agg(
    pl.len().alias("count"))
    fig = px.bar(grafico5_1, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

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

    fig = px.bar(grafico5_2, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

    
with col3:
        pregunta5_1_barrio = df.filter((pl.col("variable") == "pregunta5_1") & (pl.col("value") != 0)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
        )
        fig = px.bar(pregunta5_1_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
        st.plotly_chart(fig, theme="streamlit", width="stretch")

        st.markdown("""El resultado de 63,05% deja claro que la calidad de la respuesta a las PQRS es un punto crítico dentro de la experiencia del usuario.  
        Este indicador, junto con la orientación en el trámite (66,13%), evidencia que el proceso PQRS requiere intervenciones urgentes a nivel de:  
        :material/arrow_right: Tiempos de respuesta,  
        :material/arrow_right: Claridad del contenido,  
        :material/arrow_right: Pertinencia técnica,  
        :material/arrow_right: Acompañamiento al usuario.  
        Este valor servirá como la línea base para el mejoramiento continuo en próximos periodos. Implementar mejoras específicas en el proceso permitirá aumentar significativamente este indicador y mejorar la confianza de los usuarios en EMPOPASTO.""")
        

        pregunta5_2_barrio = df.filter((pl.col("variable") == "pregunta5_2") & (pl.col("value") != 0)).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
            pl.len().alias("count")
        )
        fig = px.bar(pregunta5_2_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
        st.plotly_chart(fig, width="stretch")


st.subheader("¿Ha solicitado revisión interna en su inmueble?")
col1, col2 = st.columns(2)
with col1:
    pregunta6 = df2.filter(pl.col("variable") == "pregunta6")
    pregunta6 = pregunta6.group_by(["Desc Categoria", "value"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(pregunta6, x="value", y="count", color="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

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

    fig = px.pie(grafico6_1, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")


with col2:
    pregunta6_barrio = df2.filter((pl.col("variable") == "pregunta6") & (pl.col("value") == "SI")).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(pregunta6_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

    st.markdown("""El indicador de 2025 (71,79%) indica un desempeño moderado, pero por debajo de estándares aceptables para el sector público, donde lo esperado es ≥ 90%.  
    **El patrón refleja:**  
    :material/arrow_right: debilidad en la capacidad de respuesta técnica,  
    :material/arrow_right: falta de oportunidad en la atención en ciertos barrios,  
    :material/arrow_right: percepción de que las revisiones no solucionan el problema de raíz,  
    :material/arrow_right: insuficiente difusión del servicio, especialmente en estratos bajos.  
    El hecho de que 2025 no haya presentado una mejora sustancial confirma que las acciones implementadas no han sido lo suficientemente efectivas o no han abarcado los sectores críticos.
    
    """)

    grafico6_1_barrio = pregunta6_1.filter(pl.col("value") != 0).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )

    fig = px.bar(grafico6_1_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
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


st.title(":blue[Acueductos y alcantarillados]")
st.subheader("¿Cómo califica la oportunidad y organización de los trabajos realizados cuando se presenta un daño de acueducto o alcantarillado?")
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
    fig = px.pie(grafico14, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    
    grafico14_1 = df2.filter(pl.col("variable") == "pregunta14_1")
    grafico14_1 = grafico14_1.group_by(["value", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico14_1, y="value", x="count", barmode="group", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
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
    fig = px.bar(grafico14_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    grafico14_1_barrio = df2.filter(pl.col("variable") == "pregunta14_1").group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico14_1_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")

st.markdown(""" Frente a la oportunidad y organización en los trabajos de reparación de acueducto y alcantarillado, el :blue[67,68 %] de los usuarios se muestra satisfecho, mientras que un :green[26,9 %] mantiene una posición neutra, y un :red[5,4 %] considera que la atención es inadecuada o insatisfactoria.
Este resultado refleja una percepción moderadamente positiva, pero con oportunidades claras de mejora en la agilidad de respuesta y finalización de obras.

Las principales inconformidades se presentan en los barrios residenciales de estratos Bajo, Medio y Medio-Bajo, y en zonas comerciales, donde los usuarios manifiestan que las demoras en las reparaciones afectan la movilidad y el desarrollo del comercio, además de reportar trabajos inconclusos o con acabados deficientes.
En el caso de los usuarios residenciales, la percepción negativa se asocia con la falta de mantenimiento preventivo y los tiempos prolongados de atención a solicitudes.
""")

st.subheader("¿Cómo califica la labor de mantenimiento y limpieza en cámaras y sumideros para evitar taponamientos y reboses?")
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
    fig = px.pie(grafico16, names="value", values="count", color_discrete_sequence=["#006400","#99EE99", "#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
    st.plotly_chart(fig, width="stretch")
    
with col21:
    grafico16_barrio = pregunta16.filter(pl.col("value") < 3).group_by(["Barrio", "Desc Subcategoria", "Desc Categoria"]).agg(
        pl.len().alias("count")
    )
    fig = px.bar(grafico16_barrio, x="Barrio", y="count", color="Desc Subcategoria", barmode="relative", facet_col="Desc Categoria", color_discrete_sequence=["#006400","#99EE99", "#228B22","#FFD700","#FF4444","#CC0000","#8B0000"], height=400)
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


# st.subheader("Recomendaciones")
# st.markdown("""
# 1. Fortalecer la divulgación del servicio de revisión interna, especialmente en estratos 1, 2 y 3, explicando sus beneficios preventivos y cómo solicitarlo.  
# 2. Analizar la relación entre revisiones y zonas con fallas (como La Cruz y Cantarana) para planear acciones correctivas focalizadas.  
# 3. Implementar campañas educativas o de mantenimiento preventivo en los barrios con más revisiones, para reducir reincidencias y solicitudes repetidas.  
# 4. Evaluar incluir en futuras encuestas una pregunta complementaria:  
#     :material/arrow_right: “¿Conoce el procedimiento para solicitar una revisión interna?” Esto permitirá medir el nivel de conocimiento y acceso a este servicio.  
# 5. Fortalecer la capacitación de los técnicos en atención al usuario, empatía y cierre efectivo de casos, para elevar la satisfacción al nivel meta (≥ 90 %).  
# 6. Implementar un sistema de seguimiento a revisiones internas, donde el usuario pueda calificar la atención al finalizar el servicio, retroalimentando el proceso.  
# 7. Ampliar la difusión del servicio de revisión preventiva, especialmente en estratos residenciales bajos, para evitar fallas mayores o reclamos tardíos.  
# 8. Enfocar la mejora en los barrios críticos (La Cruz, San Juan de Dios y Aquine II) mediante un plan piloto de revisiones técnicas proactivas.  
# 9. Fortalecer la trazabilidad de las PQRS, garantizando que los usuarios sean informados de cada etapa (recepción, trámite, cierre).  
# 10. Capacitar al personal de atención en comunicación empática y manejo de reclamos, priorizando claridad en la orientación y cumplimiento de los tiempos de respuesta.  
# 11. Difundir los canales de PQRS (presencial, telefónico, web) en barrios de estratos Bajo y Medio-Bajo, donde hay mayor desconocimiento o insatisfacción.  
# 12. Implementar encuestas postatención (por SMS o correo) para medir satisfacción y retroalimentar en tiempo real la calidad del servicio.


# 22. Fortalecer la gestión de cuadrillas operativas, priorizando los casos según impacto comunitario y nivel de afectación.  
# 23. Establecer un protocolo estandarizado de comunicación con los usuarios y comerciantes cuando se realicen obras, informando plazos y avances.  
# 24. Implementar un sistema de cierre de obras (físico y digital) que asegure que cada intervención quede completamente terminada y con el entorno restablecido.  
# 25. Diseñar un plan de mantenimiento preventivo trimestral, especialmente en sectores residenciales que reportan demoras o falta de atención.

# """)

# st.subheader("La atención que Usted recibe en nuestros puntos, ha sido:")

# st.write(df.select("variable").unique())

