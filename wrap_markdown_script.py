"""
Script para envolver markdown en contenedores con altura fija
"""
import re

def wrap_markdown_in_container(file_path, height=400):
    """Envuelve st.markdown en st.container con altura fija"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para encontrar markdown dentro de with col1/col2/col3
    # que NO esté ya dentro de un container
    
    # Buscar patrones como:
    # with col2:
    #     st.markdown("""...""")
    
    # Reemplazar por:
    # with col2:
    #     with st.container(height=400):
    #         st.markdown("""
    #         <div style="display: flex; align-items: center; height: 100%; text-align: justify;">
    #         <div>
    #         ...
    #         </div>
    #         </div>
    #         """, unsafe_allow_html=True)
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Detectar "with col" seguido de st.markdown
        if 'with col' in line and ':' in line:
            # Verificar si la siguiente línea (sin espacios) es st.markdown
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                new_lines.append(lines[j])
                j += 1
            
            if j < len(lines) and 'st.markdown(' in lines[j] and 'with st.container' not in lines[j-1]:
                # Obtener indentación
                indent = len(lines[j]) - len(lines[j].lstrip())
                
                # Agregar container
                new_lines.append(' ' * indent + f'with st.container(height={height}):')
                
                # Modificar el markdown
                markdown_line = lines[j]
                # Extraer el contenido del markdown
                if '"""' in markdown_line:
                    # Es un markdown multilinea
                    markdown_indent = ' ' * (indent + 4)
                    new_lines.append(markdown_indent + 'st.markdown("""')
                    new_lines.append(markdown_indent + '<div style="display: flex; align-items: center; height: 100%; text-align: justify;">')
                    new_lines.append(markdown_indent + '<div>')
                    
                    # Copiar contenido hasta encontrar el cierre
                    j += 1
                    while j < len(lines):
                        if '"""' in lines[j] and lines[j].strip() != '"""':
                            # Línea con cierre
                            content_line = lines[j].replace('""")', '').strip()
                            if content_line:
                                # Reemplazar :material/arrow_right: con <br>:material/arrow_right:
                                content_line = content_line.replace(':material/arrow_right:', '<br>:material/arrow_right:')
                                new_lines.append(markdown_indent + content_line)
                            new_lines.append(markdown_indent + '</div>')
                            new_lines.append(markdown_indent + '</div>')
                            new_lines.append(markdown_indent + '""", unsafe_allow_html=True)')
                            i = j
                            break
                        elif '"""' in lines[j]:
                            # Cierre en línea separada
                            new_lines.append(markdown_indent + '</div>')
                            new_lines.append(markdown_indent + '</div>')
                            new_lines.append(markdown_indent + '""", unsafe_allow_html=True)')
                            i = j
                            break
                        else:
                            # Contenido normal
                            content_line = lines[j].strip()
                            # Reemplazar :material/arrow_right: con <br>:material/arrow_right:
                            if ':material/arrow_right:' in content_line and not content_line.startswith('<br>'):
                                content_line = '<br>' + content_line
                            new_lines.append(markdown_indent + content_line)
                        j += 1
                    
        i += 1
    
    # Escribir el archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✓ Procesado: {file_path}")

# Nota: Este script es complejo y puede necesitar ajustes manuales
# Es mejor hacerlo manualmente para mayor precisión
print("Este script es de referencia. Se recomienda hacer los cambios manualmente.")
print("Consulta GUIA_ALINEACION.md para ver ejemplos completos.")
