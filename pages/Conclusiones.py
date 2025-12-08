import polars as pl
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import traceback
import time

st.set_page_config(page_title="Conclusiones", layout="wide")

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

try:
    df4_raw = conn.read(worksheet="Preguntas", ttl=0)
    # Convertir pandas DataFrame a Polars DataFrame
    preguntas = pl.from_pandas(df4_raw)
    placeholder = st.empty()
    placeholder.success(f"✅ Preguntas cargadas ({len(preguntas)} filas)")
    time.sleep(0.5)
    placeholder.empty()
except Exception as e:
    st.error(f"❌ Error al conectar con Google Sheets (Preguntas): {str(e)}")
    st.error(f"Traceback: {traceback.format_exc()}")
    st.stop()

st.subheader(":blue[Aspectos generales del servicio]")
col1, col2 = st.columns(2)
with col1:
    aspectos_grales = df3.filter(
        pl.col("Nueva_Clasificacion") == "Aspectos Generales"
    )
    ag_comparativo = aspectos_grales.group_by("Nueva_Clasificacion").agg(
        pl.when(pl.col("2023") == 0) # Si el valor es 0
        .then(pl.lit(None))           # Reemplázalo con null
        .otherwise(pl.col("2023"))    # Si no es 0, mantén el valor original
        .mean()                       # Calcula el promedio (ignorará los nulls creados)
        .round(2)
        .alias("promedio_2023"),

        pl.when(pl.col("2024") == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("2024"))
        .mean()
        .round(2)
        .alias("promedio_2024"),

        pl.when(pl.col("2025") == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("2025"))
        .mean()
        .round(2)
        .alias("promedio_2025")
        )

    fig = px.bar(ag_comparativo, x="Nueva_Clasificacion", y=["promedio_2023", "promedio_2024", "promedio_2025"], barmode="group", color_discrete_sequence=["#006400","#8B0000", "#FFD700"], title="Comparativo por año", text_auto=True)
    fig.update_layout(
        bargap=0.2,  
        bargroupgap=0.05,
    ) 
    st.plotly_chart(fig)

with col2:
    promedio = aspectos_grales.select("2025").mean().item()

    fig2 = px.bar(aspectos_grales.sort("2025", descending=True), x="variable", y="2025", color="Descripcion Pregunta", color_discrete_sequence=["#006400","#006400", "#99EE99","#99EE99", "#FFD700","#FFD700","#FF4444","#CC0000","#CC0000","#8B0000", "#8B0000"], text_auto=True, title="Nivel de satisfacción por pregunta")
    fig2.add_hline(y=promedio, line_width=2, line_color="black", annotation_text=f"{promedio:.2f}", annotation_position="top right")
    fig2.update_layout(
        showlegend=False,
    # margin=dict(b=100),
    # annotations=[
    #     dict(
    #         x=0.5,             
    #         y=-0.25,            
    #         xref="paper", 
    #         yref="paper",
    #         text= "Descripcion Pregunta",
    #         showarrow=False,
    #         font=dict(size=12, color="gray")
    #     )
    # ]
    )
    st.plotly_chart(fig2)

st.markdown("""En términos generales, los aspectos asociados a la prestación del servicio presentan una valoración satisfactoria por parte de la comunidad. El promedio de satisfacción para este componente en 2025 alcanza un 77,94%, lo que representa, un aumento de 1,23 puntos porcentuales respecto al año 2024, una reducción de 2,02 puntos porcentuales en la brecha existente frente al nivel alcanzado en 2023.  
Esto indica que, a pesar de algunas variaciones en indicadores específicos, la percepción general hacia el servicio presenta una recuperación progresiva y se mantiene dentro del rango de satisfacción establecido por los estándares de medición de la metodología SERVQUAL.  
Sin embargo, al analizar la distribución interna de los resultados, se observa que varias preguntas se encuentran por debajo del promedio global de satisfacción, lo que evidencia que existen áreas que requieren priorización para evitar que continúen afectando la percepción del servicio en general, dentro de las preguntas con desempeño inferior, el componente que muestra mayor rezago es el proceso completo de atención de PQRS, tanto en orientación como en la respuesta final ofrecida al usuario.
""")

st.subheader(":blue[Servicio de acueducto y alcantarillado]")
col1, col2 = st.columns(2)
with col1:
    acueducto_alcantarillado = df3.filter(
        pl.col("Nueva_Clasificacion") == "Servicio de acueducto y alcantarillado"
    )
    aa_comparativo = acueducto_alcantarillado.group_by("Nueva_Clasificacion").agg(
        pl.when(pl.col("2023") == 0) # Si el valor es 0
        .then(pl.lit(None))           # Reemplázalo con null
        .otherwise(pl.col("2023"))    # Si no es 0, mantén el valor original
        .mean()                       # Calcula el promedio (ignorará los nulls creados)
        .round(2)
        .alias("promedio_2023"),

        pl.when(pl.col("2024") == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("2024"))
        .mean()
        .round(2)
        .alias("promedio_2024"),

        pl.when(pl.col("2025") == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("2025"))
        .mean()
        .round(2)
        .alias("promedio_2025")
        )

    fig = px.bar(aa_comparativo, x="Nueva_Clasificacion", y=["promedio_2023", "promedio_2024", "promedio_2025"], barmode="group", color_discrete_sequence=["#FFD700","#8B0000", "#006400"], title="Comparativo por año", text_auto=True)
    fig.update_layout(
        bargap=0.2,  
        bargroupgap=0.05,
    ) 
    st.plotly_chart(fig)

with col2:
    promedio = acueducto_alcantarillado.select("2025").mean().item()

    fig2 = px.bar(acueducto_alcantarillado.sort("2025", descending=True), x="variable", y="2025", color="Descripcion Pregunta", color_discrete_sequence=["#006400","#006400", "#99EE99", "#FFD700","#FF4444","#CC0000","#CC0000","#8B0000", "#8B0000"], text_auto=True, title="Nivel de satisfacción por pregunta")
    fig2.add_hline(y=promedio, line_width=2, line_color="black", annotation_text=f"{promedio:.2f}", annotation_position="top right")
    fig2.update_layout(
        showlegend=False,
    # margin=dict(b=100),
    # annotations=[
    #     dict(
    #         x=0.5,             
    #         y=-0.25,            
    #         xref="paper", 
    #         yref="paper",
    #         text= "Descripcion Pregunta",
    #         showarrow=False,
    #         font=dict(size=12, color="gray")
    #     )
    # ]
    )
    st.plotly_chart(fig2)

st.markdown("""En términos generales, el componente Servicio de Acueducto y Alcantarillado presenta una valoración muy satisfactoria por parte de la comunidad. Para el año 2025, este componente alcanza un promedio de satisfacción del 80,13%, lo que representa un aumento de 3,9 puntos porcentuales respecto al año 2024 y una mejora de 0,11 puntos porcentuales frente al nivel registrado en 2023.  
Estos resultados evidencian una recuperación progresiva del componente, ubicándolo nuevamente dentro del rango de "muy satisfactorio" según los parámetros definidos por la metodología SERVQUAL. La estabilidad y mejora observada indican que los usuarios perciben un servicio técnicamente confiable, con buena calidad del agua, adecuada continuidad y procesos que, en la mayoría de los casos, cumplen con las expectativas ciudadanas.  
A pesar de la valoración general positiva, un examen detallado de las preguntas que integran el componente revela que dos indicadores se encuentran por debajo del promedio global. Esto señala áreas críticas que requieren atención prioritaria debido a su potencial impacto en la satisfacción global del servicio.
:material/arrow_right: Oportunidad y organización de los trabajos de acueducto y alcantarillado
:material/arrow_right: Labor de mantenimiento y limpieza en cámaras y sumideros para evitar taponamientos y reboses
""")

st.subheader(":blue[Medios de Comunicación, Actividades y Gestión]")
col1, col2 = st.columns(2)
with col1:
    mdcag = df3.filter(
        pl.col("Nueva_Clasificacion") == "Medios de comunicación, actividades y gestión"
    )
    mcag_comparativo = mdcag.group_by("Nueva_Clasificacion").agg(
        pl.when(pl.col("2023") == 0) # Si el valor es 0
        .then(pl.lit(None))           # Reemplázalo con null
        .otherwise(pl.col("2023"))    # Si no es 0, mantén el valor original
        .mean()                       # Calcula el promedio (ignorará los nulls creados)
        .round(2)
        .alias("promedio_2023"),

        pl.when(pl.col("2024") == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("2024"))
        .mean()
        .round(2)
        .alias("promedio_2024"),

        pl.when(pl.col("2025") == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("2025"))
        .mean()
        .round(2)
        .alias("promedio_2025")
        )

    fig = px.bar(mcag_comparativo, x="Nueva_Clasificacion", y=["promedio_2023", "promedio_2024", "promedio_2025"], barmode="group", color_discrete_sequence=["#8B0000","#006400","#FFD700"], title="Comparativo por año", text_auto=True)
    fig.update_layout(
        bargap=0.2,  
        bargroupgap=0.05,
    ) 
    st.plotly_chart(fig)

with col2:
    promedio = mdcag.select("2025").mean().item()

    fig2 = px.bar(mdcag.sort("2025", descending=True), x="variable", y="2025", color="Descripcion Pregunta", color_discrete_sequence=["#006400","#006400", "#99EE99", "#FFD700","#FF4444","#CC0000","#CC0000","#8B0000", "#8B0000"], text_auto=True, title="Nivel de satisfacción por pregunta")
    fig2.add_hline(y=promedio, line_width=2, line_color="black", annotation_text=f"{promedio:.2f}", annotation_position="top right")
    fig2.update_layout(
        showlegend=False,
    # margin=dict(b=100),
    # annotations=[
    #     dict(
    #         x=0.5,             
    #         y=-0.25,            
    #         xref="paper", 
    #         yref="paper",
    #         text= "Descripcion Pregunta",
    #         showarrow=False,
    #         font=dict(size=12, color="gray")
    #     )
    # ]
    )
    st.plotly_chart(fig2)

st.markdown("""
En términos generales, el componente Medios de Comunicación, Actividades y Gestión presenta una valoración media-alta por parte de la comunidad, con una tendencia marcada hacia la recuperación en 2025.  
Para este año, el componente alcanza un promedio de satisfacción del 82,52%, lo que representa un incremento de 17,57 puntos porcentuales respecto al año 2024 y un aumento de 4,29 puntos porcentuales frente al nivel registrado en 2023.  
Este crecimiento refleja una mejor percepción de la comunidad en torno a la gestión institucional, especialmente en lo relacionado con:  
:material/arrow_right: La forma en que los usuarios se enteran de las noticias y actividades de EMPOPASTO.  
:material/arrow_right: La valoración de los programas sociales y ambientales.  
:material/arrow_right: La percepción global de la gestión gerencial.  
El desempeño de 2025 ubica este componente dentro del rango de “muy satisfactorio”, según los criterios de la metodología SERVQUAL, evidenciando una recuperación significativa después de un 2024 con resultados más bajos.""")


st.subheader(":blue[Niveles de satisfaccion global]")

ag = ag_comparativo.select("promedio_2025").item()
ac = aa_comparativo.select("promedio_2025").item()
mcag = mcag_comparativo.select("promedio_2025").item()

fig = px.bar(x=["Aspectos Generales", "Acueducto y Alcantarillado", "Medios de Comunicación, Actividades y Gestión"], y=[ag, ac, mcag], color_discrete_sequence=["#006400", "#FFD700", "#8B0000"], title="Niveles de satisfacción global")
st.plotly_chart(fig)

promedio_gral = (ag + ac + mcag) / 3

st.metric("Nivel de satisfacción global", f"{promedio_gral:.2f}%", border=True, delta_color="normal", delta="+0,93%")

st.markdown("""
El nivel de satisfaccion global se encuentra en el rango de "muy satisfactorio" según los parámetros definidos por la metodología SERVQUAL. 


""")

#st.write(df3)



st.markdown("**Conclusiones**")

st.markdown("""Tras analizar los resultados obtenidos a partir de la encuesta aplicada bajo la metodología SERVQUAL, se pueden establecer las siguientes conclusiones:  
1. El nivel global de satisfacción de los usuarios es positivo, pero aún insuficiente  
La percepción general de los usuarios alcanza un 81,93%, lo que indica que EMPOPASTO mantiene una buena receptividad y valoración positiva en la mayoría de sus servicios.  
Sin embargo, todavía existe una brecha importante para alcanzar la meta institucional del 90%, lo que sugiere la necesidad de ajustar procesos clave para continuar mejorando la experiencia ciudadana.  

2. La Capacidad de Respuesta es la dimensión con mayores desafíos  
Con un nivel de aceptación del 57,91%, este componente se posiciona como el principal punto crítico.  
Las preguntas más sensibles son:  
    :material/arrow_right: Respuesta a las PQRS (41,52%)  
    :material/arrow_right: Orientación durante los trámites (48,38%)  
Estas cifras muestran que los usuarios sienten falta de claridad, acompañamiento y oportunidad en los procesos administrativos y de atención.  
Los estratos Bajo, Medio-Bajo y Bajo-Bajo concentran el mayor número de inconformidades, por lo que se requieren acciones focalizadas.  

3. La dimensión de Tangibilidad registra aceptación moderada  
La percepción positiva sobre instalaciones y elementos físicos del servicio alcanza el 71,65%.  
Aunque la mayoría de usuarios consideran que las instalaciones son adecuadas, este componente no cumple con el estándar esperado para entidades públicas (≥90%).  
Se recomienda mejorar señalización, accesibilidad y condiciones físicas de los puntos de atención.  

4. El servicio operativo (calidad del agua, continuidad y presión) mantiene resultados sobresalientes  
Las preguntas relacionadas con calidad del agua, continuidad del servicio y presión presentan niveles de aceptación superiores al 90%, lo que confirma que el componente técnico–operativo es la mayor fortaleza de EMPOPASTO.  
Esto se ve reforzado por:  

    :material/arrow_right: 92,7% de satisfacción con la calidad del agua.  
    :material/arrow_right: 90,5% de percepción positiva frente a continuidad del servicio.  
    :material/arrow_right: 90,7% de aceptación sobre la presión del agua.  
Estas cifras demuestran un servicio estable y confiable, incluso en sectores con condiciones geográficas complejas.  

5. La comunicación institucional requiere ajustes para alinearse con las preferencias de los usuarios  
Aunque el 49,2% de los usuarios se informa principalmente a través de redes sociales, existe una demanda creciente por medios alternos como:  
    :material/arrow_right: Factura (13,7%)  
    :material/arrow_right: Correo electrónico (10,8%)  
Esto muestra una oportunidad para diversificar los canales de comunicación y fortalecer estrategias informativas segmentadas por estrato y tipo de usuario.  

6. La página web es una herramienta relevante, pero con brechas de acceso  
El 73,8% de los usuarios ha utilizado la página web, principalmente en estratos bajos y medio-bajos.  
Sin embargo, el 26,2% que no la usa corresponde a sectores donde puede existir desconocimiento, falta de acceso digital o necesidad de mejorar la usabilidad.  
Esto sugiere la importancia de reforzar campañas de alfabetización digital y optimizar la arquitectura web.  

7. Los trabajos operativos generan afectaciones en ciertos sectores  
Aunque el 74,2% no ha sido afectado por trabajos de obra, el 25,8% restante señala impactos como:  

    :material/arrow_right: Cierre de vías (29%)  
    :material/arrow_right: Suspensión temporal del agua (17,6%)  
    :material/arrow_right: Afectación del comercio (12,2%)  
Los barrios Agualongo, La Cruz y zonas comerciales requieren una gestión más anticipada, mejor comunicación y reducción de tiempos de intervención.  

8. La gestión institucional es valorada positivamente, pero con variaciones por edad y estrato  
La gestión actual de EMPOPASTO obtiene un 72,7% de aceptación.  
Los usuarios más críticos pertenecen a:  

    :material/arrow_right: Estratos Bajo, Comercial y Medio-Bajo  
    :material/arrow_right: Grupos de edad entre 36–45 y 50–60 años  
    :material/arrow_right: Barrios con antecedentes de problemas operativos (Agualongo, Atahualpa, La Cruz, etc.)  
Esto evidencia que la percepción de la gestión está directamente relacionada con la experiencia en servicios operativos y la atención al usuario.  

EMPOPASTO presenta una percepción mayoritariamente positiva en los aspectos operativos del servicio —calidad del agua, continuidad y presión— lo que constituye su mayor fortaleza.  Sin embargo, los procesos administrativos, de atención al usuario y de respuesta a solicitudes requieren mejoras urgentes para cerrar las brechas en Capacidad de Respuesta y Tangibilidad, y así avanzar hacia el objetivo institucional del 90% de satisfacción.  

El análisis permite identificar con claridad los focos de intervención, los grupos de usuarios más sensibles y las zonas donde la gestión debe priorizarse para lograr una mejora integral en la experiencia del servicio.  

""")

st.markdown("**Recomendaciones**")
st.markdown("""Con base en el análisis integral de los resultados obtenidos en la encuesta aplicada bajo la metodología SERVQUAL, se plantean las siguientes recomendaciones estratégicas para mejorar la experiencia del usuario, fortalecer los procesos internos y avanzar hacia el cumplimiento de la meta institucional del 90% de satisfacción:  

**Fortalecer la Comunicación Institucional**  
:material/arrow_right: Diversificar los canales de información, integrando redes sociales, radio comunitaria, mensajería instantánea (WhatsApp/SMS), correo electrónico y secciones informativas en la factura.  
:material/arrow_right: Crear una sección digital “Entienda su Factura” con videos, ejemplos y guías interactivas.  
:material/arrow_right: Diseñar una guía gráfica impresa y digital sobre interpretación de la factura, adaptada por estrato y distribuida en barrios vulnerables.  
:material/arrow_right: Mejorar la oportunidad y claridad en la comunicación sobre cortes programados, trabajos en vía y actividades operativas, priorizando los barrios más afectados (Agualongo, La Cruz, Miraflores, Caicedo Alto, etc.).  
:material/arrow_right: Publicar informes trimestrales de calidad del agua para aumentar la transparencia y confianza ciudadana.  

**Optimizar la Capacidad de Respuesta y Atención al Usuario**

:material/arrow_right: Fortalecer la gestión de PQRS mediante trazabilidad visible para el usuario (recepción, trámite y cierre), reduciendo tiempos y mejorando la calidad de las respuestas.  
:material/arrow_right: Capacitar al personal en comunicación empática, orientación clara y manejo de reclamos.  
:material/arrow_right: Implementar encuestas de satisfacción postatención (presencial, telefónica y web) para retroalimentación continua.  
:material/arrow_right: Difundir ampliamente el servicio de revisión interna, especialmente en estratos 1, 2 y 3, explicando su utilidad preventiva y cómo solicitarlo.  
:material/arrow_right: Realizar planes piloto de revisiones preventivas en barrios con mayores incidencias (La Cruz, Cantarana, San Juan de Dios).

**Mejorar la Gestión de Obras y Afectaciones en Territorio**

:material/arrow_right: Establecer un protocolo estandarizado de comunicación para avisos de obras, con tiempos mínimos de 24 horas y formatos claros.  
:material/arrow_right: Implementar un sistema de cierre de obras físico/digital que garantice entrega completa y entorno restablecido.  
:material/arrow_right: Priorizar horarios de intervención que reduzcan el impacto en movilidad y comercio, con coordinaciones específicas para zonas comerciales.  
:material/arrow_right: Instalar señalización visible durante las obras y evitar cierres totales cuando sea posible.  
:material/arrow_right: Monitorear semanalmente las afectaciones a través de un tablero de control (Power BI) para evaluar mejoras trimestrales.

**Fortalecer el Componente Operativo del Servicio**

:material/arrow_right: Mantener los estándares altos en calidad del agua, continuidad y presión, reforzando el seguimiento georreferenciado en barrios con variaciones reportadas.  
:material/arrow_right: Realizar mediciones de presión en campo en barrios críticos (La Floresta, Chambú, Quintas de San Pedro, La Cruz, Panorámico II Etapa, etc.).  
:material/arrow_right: Implementar un plan de mantenimiento preventivo de válvulas, redes secundarias y estaciones de bombeo en zonas de altitud elevada.  
:material/arrow_right: Comunicar proactivamente las causas y acciones correctivas cuando existan interrupciones del servicio para fortalecer la confianza del usuario.

**Mejoras en Infraestructura y Tangibles**

:material/arrow_right: Ampliar o reorganizar los espacios de atención donde se presentan mayores tiempos de espera.  
:material/arrow_right: Mejorar los elementos tangibles mediante señalización clara, mayor accesibilidad física, rampas, pasamanos y zonas preferenciales.  
:material/arrow_right: Mantener estándares altos de limpieza e higiene en todos los puntos de atención.  
:material/arrow_right: Incluir terminales de autoservicio, pantallas informativas y sistemas tecnológicos que aumenten la percepción de modernización.

**Agilizar la Atención Presencial y Telefónica**

:material/arrow_right: Implementar o mejorar sistemas de turnos y filas para reducir tiempos de espera.  
:material/arrow_right: Mapear trámites más lentos y aplicar mejoras específicas para los cuellos de botella.  
:material/arrow_right: Reducir tiempos de respuesta en la línea telefónica mediante protocolos de atención eficiente y solución en primer contacto.  

**Monitoreo y Evaluación Continua**  

:material/arrow_right: Realizar seguimiento periódico por estrato y barrio para evaluar el impacto de las acciones.  
:material/arrow_right: Incorporar en próximas encuestas preguntas adicionales sobre conocimiento de servicios (revisión interna, PQRS, página web).  
:material/arrow_right: Utilizar herramientas como Power BI para monitorear indicadores en tiempo real y reaccionar más rápido ante variaciones.

La implementación articulada de estas acciones permitirá elevar la satisfacción del usuario, mejorar la percepción en los componentes más críticos (Capacidad de Respuesta y Tangibles) y consolidar la confianza en la gestión de EMPOPASTO, avanzando hacia el cumplimiento de la meta institucional del 90%.
""")