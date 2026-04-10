import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.tarea_queries import (
    insertar_tarea,
    actualizar_tarea,
    cambiar_estado_tarea,
    eliminar_tarea,
    obtener_tareas_docente,
    obtener_detalle_tarea 
    
)
from database.conexion import get_conexion

conn = get_conexion()
cursor = conn.cursor()

# -- Limpieza previa -------------------------------------------
cursor.execute('DELETE FROM tareas')
cursor.execute('DELETE FROM usuarios')
cursor.execute('DELETE FROM cursos')
conn.commit()
print('? Datos anteriores limpiados')

# -- Datos de prueba -------------------------------------------
cursor.execute('''
    INSERT INTO cursos (nombre)
    VALUES ('Sistemas de Informacion II')
    RETURNING id
''')
id_curso = cursor.fetchone()[0]

cursor.execute('''
    INSERT INTO usuarios (nombre, apellido, email, rol)
    VALUES ('Juan', 'Perez', 'docente@prueba.com', 'docente')
    RETURNING id
''')
id_docente = cursor.fetchone()[0]
conn.commit()
cursor.close()
conn.close()

print(f'? Curso creado con ID: {id_curso}')
print(f'? Docente creado con ID: {id_docente}')

print('\n=== PROBANDO T-09.7 ===\n')

print('-- Insertando tarea --')
id_tarea = insertar_tarea(
    'Tarea 1 - Diagrama de flujo',
    'Realizar un diagrama de flujo del sistema',
    '2026-05-30 23:59:00',
    id_curso,
    id_docente
)

print('\n-- Actualizando tarea --')
actualizar_tarea(
    id_tarea,
    'Tarea 1 - Actualizada',
    'Descripcion actualizada',
    '2026-06-15 23:59:00'
)

print('\n-- Publicando tarea --')
cambiar_estado_tarea(id_tarea, 'publicada')

print('\n-- Consultando tareas del docente --')
obtener_tareas_docente(id_docente)

print('\n-- Obteniendo detalle de tarea --')
obtener_detalle_tarea(id_tarea)

print('\n-- Eliminando tarea --')
eliminar_tarea(id_tarea)


print('\n=== T-09.7 COMPLETADO ===')
