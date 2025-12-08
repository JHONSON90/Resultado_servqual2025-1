
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

