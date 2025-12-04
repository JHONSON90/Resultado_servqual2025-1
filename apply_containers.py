"""
Script para envolver markdown en contenedores con el formato del usuario
Aplica el patrón:
    with st.container(
        height=400, 
        horizontal_alignment="center",
        vertical_alignment="center"
    ):
        st.markdown(...)
"""
import re
import sys

def process_file(filepath):
    """Procesa un archivo para envolver markdown en contenedores"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para encontrar st.markdown dentro de columnas
    # Buscar: with colX:\n    st.markdown("""...""")
    # Reemplazar con el contenedor
    
    pattern = r'(with col\d+:)\n((?:    .*\n)*?)(    st\.markdown\(""")'
    
    def replacer(match):
        col_line = match.group(1)
        intermediate_lines = match.group(2)
        markdown_start = match.group(3)
        
        # Contar la indentación del markdown
        indent = '    '
        
        # Crear el contenedor
        container = f'''{col_line}
{intermediate_lines}{indent}with st.container(
{indent}    height=400, 
{indent}    horizontal_alignment="center",
{indent}    vertical_alignment="center"
{indent}):
{indent}    st.markdown("""'''
        
        return container
    
    # Aplicar el reemplazo
    new_content = re.sub(pattern, replacer, content)
    
    # Ajustar la indentación del contenido del markdown
    # Buscar el contenido entre """ y """ y agregar 4 espacios
    def indent_markdown_content(match):
        opening = match.group(1)
        content = match.group(2)
        closing = match.group(3)
        
        # Agregar 4 espacios a cada línea del contenido
        lines = content.split('\n')
        indented_lines = [('    ' + line if line.strip() else line) for line in lines]
        indented_content = '\n'.join(indented_lines)
        
        return opening + indented_content + closing
    
    # Este patrón es más complejo, mejor hacerlo manualmente
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ Procesado: {filepath}")

# Archivos a procesar
files = [
    "pages/Tangibles.py",
    "pages/Fiabilidad.py",
    "pages/Empatia.py",
    "pages/Cap_Respuesta.py"
]

if __name__ == "__main__":
    import os
    os.chdir(r"f:\EDISON\computador\VARIOS EDISON\PROHIBIDO NO TOCAR\CursoPrepHenry\Encuestas_Empopasto\Arreglo_Encuesta")
    
    for file in files:
        try:
            process_file(file)
        except Exception as e:
            print(f"✗ Error en {file}: {e}")
