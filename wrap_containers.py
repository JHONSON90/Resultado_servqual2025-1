"""
Script para envolver markdown en contenedores con el formato específico del usuario
"""
import re
import sys

def wrap_markdown_in_columns(file_path):
    """Envuelve st.markdown dentro de columnas con st.container"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Detectar "with col" seguido eventualmente de st.markdown
        if re.match(r'\s*with col\d+:', line):
            col_indent = len(line) - len(line.lstrip())
            
            # Buscar el siguiente st.markdown en este bloque
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # Si encontramos otra columna o salimos del bloque, parar
                if next_indent <= col_indent and next_line.strip():
                    break
                
                # Si encontramos st.markdown y no está ya en un container
                if 'st.markdown(' in next_line and 'with st.container' not in ''.join(lines[max(0,j-5):j]):
                    # Insertar el container antes del markdown
                    markdown_indent = len(next_line) - len(next_line.lstrip())
                    container_lines = [
                        ' ' * markdown_indent + 'with st.container(\n',
                        ' ' * (markdown_indent + 8) + 'height=400,\n',
                        ' ' * (markdown_indent + 8) + 'horizontal_alignment="center",\n',
                        ' ' * (markdown_indent + 8) + 'vertical_alignment="center"\n',
                        ' ' * markdown_indent + '):\n'
                    ]
                    
                    # Agregar líneas hasta el markdown (espacios en blanco)
                    for k in range(i + 1, j):
                        new_lines.append(lines[k])
                    
                    # Agregar el container
                    new_lines.extend(container_lines)
                    
                    # Agregar el markdown con indentación adicional
                    markdown_content = next_line
                    new_markdown = ' ' * 4 + markdown_content
                    new_lines.append(new_markdown)
                    
                    # Continuar con las líneas del markdown multilinea
                    j += 1
                    while j < len(lines):
                        if '"""' in lines[j] and j > i + 1:
                            # Fin del markdown
                            new_lines.append(' ' * 4 + lines[j])
                            i = j
                            break
                        else:
                            new_lines.append(' ' * 4 + lines[j])
                        j += 1
                    break
                
                j += 1
        
        i += 1
    
    # Escribir el archivo
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ Procesado: {file_path}")

# Este script es complejo, mejor hacerlo manualmente
print("Script de referencia - se recomienda aplicar cambios manualmente")
