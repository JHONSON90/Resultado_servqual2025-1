"""
Script para agregar alturas consistentes a todas las gráficas de Plotly
para mejorar la alineación en columnas de Streamlit
"""
import re
import os

def add_height_to_charts(file_path):
    """Agrega parámetro height a las gráficas de plotly y use_container_width a st.plotly_chart"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Patrón para encontrar px.bar, px.pie, px.histogram, etc. sin height
    # Buscar líneas que terminan con ) pero no tienen height=
    patterns = [
        # Para gráficas que ya tienen parámetros y terminan con )
        (r'(fig = px\.(bar|pie|histogram|scatter_map|line_polar)\([^)]+)(\))', r'\1, height=500\3'),
    ]
    
    for pattern, replacement in patterns:
        # Solo reemplazar si no tiene ya height=
        matches = re.finditer(pattern, content)
        for match in matches:
            if 'height=' not in match.group(0):
                content = content.replace(match.group(0), re.sub(pattern, replacement, match.group(0)))
    
    # Actualizar st.plotly_chart para usar use_container_width=True
    # Patrón 1: st.plotly_chart(fig)
    content = re.sub(
        r'st\.plotly_chart\(fig\)(?!\s*,)',
        'st.plotly_chart(fig, use_container_width=True)',
        content
    )
    
    # Patrón 2: st.plotly_chart(fig, theme="streamlit")
    content = re.sub(
        r'st\.plotly_chart\(fig,\s*theme="streamlit"\)',
        'st.plotly_chart(fig, theme="streamlit", use_container_width=True)',
        content
    )
    
    # Patrón 3: st.plotly_chart(fig2), st.plotly_chart(fig3), etc.
    for i in range(2, 10):
        content = re.sub(
            rf'st\.plotly_chart\(fig{i}\)(?!\s*,)',
            rf'st.plotly_chart(fig{i}, use_container_width=True)',
            content
        )
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Actualizado: {file_path}")
        return True
    else:
        print(f"- Sin cambios: {file_path}")
        return False

# Archivos a procesar
files_to_process = [
    r"f:\EDISON\computador\VARIOS EDISON\PROHIBIDO NO TOCAR\CursoPrepHenry\Encuestas_Empopasto\Arreglo_Encuesta\pages\Tangibles.py",
    r"f:\EDISON\computador\VARIOS EDISON\PROHIBIDO NO TOCAR\CursoPrepHenry\Encuestas_Empopasto\Arreglo_Encuesta\pages\Fiabilidad.py",
    r"f:\EDISON\computador\VARIOS EDISON\PROHIBIDO NO TOCAR\CursoPrepHenry\Encuestas_Empopasto\Arreglo_Encuesta\pages\Empatia.py",
    r"f:\EDISON\computador\VARIOS EDISON\PROHIBIDO NO TOCAR\CursoPrepHenry\Encuestas_Empopasto\Arreglo_Encuesta\pages\Cap_Respuesta.py",
]

print("Procesando archivos...")
print("=" * 60)

for file_path in files_to_process:
    if os.path.exists(file_path):
        add_height_to_charts(file_path)
    else:
        print(f"✗ No encontrado: {file_path}")

print("=" * 60)
print("Proceso completado!")
