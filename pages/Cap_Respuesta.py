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



st.title(":blue[Acueductos y alcantarillados]")


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

