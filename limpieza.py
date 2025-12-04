import polars as pl

# Cargar el archivo
df = pl.scan_csv("Data/Encuestas_ONE - Limpia.csv")



print(df.collect().columns)

# ['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'pregunta1', 'pregunta2', 'pregunta2_1', 'pregunta3', 'pregunta4_1', 'pregunta4_2', 'pregunta4_3', 'pregunta5', 'pregunta5_1', 'pregunta5_2', 'pregunta6', 'pregunta6_1', 'pregunta7', 'pregunta7_1', 'pregunta8', 'pregunta9', 'pregunta9_1', 'pregunta10', 'pregunta11', 'pregunta11_1', 'pregunta12', 'pregunta13', 'pregunta14', 'pregunta14_1', 'pregunta15', 'pregunta15_1', 'pregunta16', 'pregunta16_1', 'pregunta17', 'pregunta17_1', 'pregunta18', 'pregunta18_1', 'pregunta19', 'pregunta19_1', 'pregunta20', 'pregunta21', 'pregunta22', 'pregunta23']

# ,       ,  ,              , ,

fiabilidad = ['pregunta1', 'pregunta2', 'pregunta2_1','pregunta3','pregunta7', 'pregunta7_1', 'pregunta10', 'pregunta11', 'pregunta11_1', 'pregunta12', 'pregunta13']
cap_respuesta = ['pregunta5','pregunta5_1', 'pregunta5_2', 'pregunta6','pregunta6_1', 'pregunta14', 'pregunta14_1', 'pregunta16', 'pregunta16_1']
empatia = ['pregunta4_1','pregunta4_2', 'pregunta4_3','pregunta9', 'pregunta9_1', 'pregunta15', 'pregunta15_1',]
elementos_tangibles = ['pregunta8']
otros = ['pregunta17', 'pregunta17_1', 'pregunta18', 'pregunta18_1','pregunta19', 'pregunta19_1', 'pregunta20', 'pregunta21','pregunta22']

cuantitativas = df.select(['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'Desc Categoria', 'Subcategoria', 'Desc Subcategoria','pregunta1', 'pregunta2','pregunta4_1', 'pregunta4_2', 'pregunta4_3','pregunta5_1', 'pregunta5_2', 'pregunta6_1', 'pregunta7_1', 'pregunta8', 'pregunta9_1', 'pregunta10','pregunta11_1', 'pregunta12', 'pregunta13', 'pregunta14', 'pregunta16', 'pregunta20', 'pregunta21']).unpivot(index=['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', "Desc Categoria", "Subcategoria", "Desc Subcategoria"], on=['pregunta1', 'pregunta2','pregunta4_1', 'pregunta4_2', 'pregunta4_3','pregunta5_1', 'pregunta5_2', 'pregunta6_1', 'pregunta7_1', 'pregunta8', 'pregunta9_1', 'pregunta10','pregunta11_1', 'pregunta12', 'pregunta13', 'pregunta14', 'pregunta16', 'pregunta20', 'pregunta21'])

cuantitativas = cuantitativas.with_columns(
    pl.when(pl.col("variable").is_in(fiabilidad)).then(pl.lit("Fiabilidad"))
    .when(pl.col("variable").is_in(cap_respuesta)).then(pl.lit("Capacidad de respuesta"))
    .when(pl.col("variable").is_in(empatia)).then(pl.lit("Empatía"))
    .when(pl.col("variable").is_in(elementos_tangibles)).then(pl.lit("Elementos tangibles"))
    .when(pl.col("variable").is_in(otros)).then(pl.lit("Otros"))
    .otherwise(pl.lit("Otros"))
    .alias("Categoria")
)

cualitativas = df.select(['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'Desc Categoria', 'Subcategoria', 'Desc Subcategoria', 'pregunta2_1', 'pregunta3', 'pregunta5', 'pregunta6', 'pregunta7', 'pregunta9', 'pregunta11', 'pregunta14_1', 'pregunta15', 'pregunta15_1', 'pregunta19', 'pregunta22']).unpivot(index=['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', "Desc Categoria", "Subcategoria", "Desc Subcategoria"], on=['pregunta2_1', 'pregunta3', 'pregunta5', 'pregunta6', 'pregunta7', 'pregunta9', 'pregunta11', 'pregunta14_1', 'pregunta15', 'pregunta15_1','pregunta19','pregunta22'])

cualitativas_lista = df.select(['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'Desc Categoria', 'Subcategoria', 'Desc Subcategoria', 'pregunta17', 'pregunta17_1', 'pregunta18', 'pregunta18_1',  'pregunta19_1']).unpivot(index=['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'Desc Categoria', 'Subcategoria', 'Desc Subcategoria'], on=['pregunta17', 'pregunta17_1', 'pregunta18', 'pregunta18_1',  'pregunta19_1'])

cualitativas_lista = cualitativas_lista.with_columns(
    pl.col("value").str.replace_all(r"[\[\]\"]", "").alias("Sin_lista")
)
#print(cualitativas_lista.collect().tail(10))

cualitativas_lista = cualitativas_lista.with_columns(
    pl.col("Sin_lista")
    .str.strip_chars()
    .alias("Lista_Opciones")
).select(['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'Desc Categoria', 'Subcategoria', 'Desc Subcategoria','variable', 'Lista_Opciones'])
#print(cualitativas_lista.collect().tail(10))

cualitativas_lista = cualitativas_lista.with_columns(
    pl.col("Lista_Opciones").str.split(",").alias("Value")
).explode("Value").with_columns(
    pl.col("Value").str.strip_chars().alias("value2")
).with_columns(
    pl.col("value2").str.replace_all("'", "")
).select(['Nombre', 'Telefono', 'Direccion', 'Barrio', 'Estrato', 'Fecha', 'Codigo', 'Tipo', 'Edad', 'Desc Categoria', 'Subcategoria', 'Desc Subcategoria','variable', 'value2']).filter(
    ~(pl.col("value2").is_null() | (pl.col("value2") == pl.lit("")))
).rename({"value2": "value"})


total_cualitativas = pl.concat([cualitativas, cualitativas_lista]).filter(
    ~(pl.col("value").is_null() | (pl.col("value") == pl.lit("")))
).with_columns(
    pl.when(pl.col("variable").is_in(fiabilidad)).then(pl.lit("Fiabilidad"))
    .when(pl.col("variable").is_in(cap_respuesta)).then(pl.lit("Capacidad de respuesta"))
    .when(pl.col("variable").is_in(otros)).then(pl.lit("Otros"))
    .when(pl.col("variable").is_in(empatia)).then(pl.lit("Empatía"))
    .when(pl.col("variable").is_in(elementos_tangibles)).then(pl.lit("Elementos tangibles"))
    .otherwise(pl.lit("Otro"))
    .alias("Categoria")
)

mayores_a_3 = cuantitativas.filter(pl.col("value") > 0).group_by("variable").agg(
    pl.mean("value").alias("promedio")
)

mayores_a_3 = mayores_a_3.with_columns(
    (pl.col("promedio") / 5 * 100).round(2).alias("2025")
)

mayores_a_3 = mayores_a_3.select(['variable','2025'])

siyno_calificables = total_cualitativas.filter(
    (pl.col("variable")== "pregunta3") #| (pl.col("variable") == "pregunta19")
).with_columns(
    pl.when(pl.col("value") == "SI")
    .then(5)
    .otherwise(1)
    .alias("puntaje")
).group_by("variable").agg(
    pl.mean("puntaje").alias("promedio")
).with_columns(
    (pl.col("promedio") / 5 * 100).round(2).alias("2025")
)

siyno_calificables = siyno_calificables.select(['variable','2025'])

para_niv_satisfaccion = pl.concat([mayores_a_3, siyno_calificables])

cargar_preguntas = pl.read_excel("Data/preguntas.xlsx")

para_niv_satisfaccion = cargar_preguntas.join(para_niv_satisfaccion.collect(), on="variable", how="left")

para_niv_satisfaccion = para_niv_satisfaccion.select(['variable','Descripcion Pregunta','Nueva_Clasificacion', '2023', '2024', '2025'])

para_niv_satisfaccion.write_csv("Formatos_Listos/para_niv_satisfaccion.csv")
total_cualitativas.collect().write_csv("Formatos_Listos/Cualitativas.csv")
cuantitativas.collect().write_csv("Formatos_Listos/Cuantitativas.csv")
print("-" * 50, "Listos!!!!!", "-" * 50)

