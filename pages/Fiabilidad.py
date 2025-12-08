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


