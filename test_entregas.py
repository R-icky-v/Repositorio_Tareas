import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.crear_tablas import crear_tabla_entregas
from database.tarea_queries import (
    insertar_entrega,
    obtener_entregas_por_tarea,
    anular_entrega
)
from database.conexion import get_conexion

# ── Crear tabla entregas ──────────────────────────────────────
print('=== CREANDO TABLA ENTREGAS ===')
crear_tabla_entregas()

# ── Obtener IDs existentes de la BD ──────────────────────────
conn = get_conexion()
cursor = conn.cursor()

cursor.execute('SELECT id FROM tareas LIMIT 1')
resultado_tarea = cursor.fetchone()

cursor.execute("SELECT id FROM usuarios WHERE rol = 'estudiante' LIMIT 1")
resultado_estudiante = cursor.fetchone()

# ── Si no hay estudiante lo creamos ──────────────────────────
if not resultado_estudiante:
    cursor.execute('''
        INSERT INTO usuarios (nombre, apellido, email, rol)
        VALUES ('Maria', 'Lopez', 'estudiante@prueba.com', 'estudiante')
        RETURNING id
    ''')
    resultado_estudiante = cursor.fetchone()
    conn.commit()
    print('Estudiante de prueba creado')

# ── Si no hay tarea la creamos ────────────────────────────────
if not resultado_tarea:
    cursor.execute('SELECT id FROM cursos LIMIT 1')
    id_curso = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM usuarios WHERE rol = \'docente\' LIMIT 1')
    id_docente = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO tareas (titulo, descripcion, fecha_limite, id_curso, id_docente)
        VALUES ('Tarea de prueba', 'Descripcion', '2026-05-30 23:59:00', %s, %s)
        RETURNING id
    ''', (id_curso, id_docente))
    resultado_tarea = cursor.fetchone()
    conn.commit()
    print('Tarea de prueba creada')

id_tarea = resultado_tarea[0]
id_estudiante = resultado_estudiante[0]
cursor.close()
conn.close()

print('ID tarea: ' + str(id_tarea))
print('ID estudiante: ' + str(id_estudiante))

# ── Probar consultas ──────────────────────────────────────────
print('\n=== PROBANDO T-01.7 ===\n')

print('-- Insertando entrega --')
id_entrega = insertar_entrega(
    id_tarea,
    id_estudiante,
    'entregas/tarea1/estudiante_maria.pdf',
    'diagrama_flujo.pdf'
)

print('\n-- Consultando entregas de la tarea --')
obtener_entregas_por_tarea(id_tarea)

print('\n-- Anulando entrega --')
anular_entrega(id_entrega)

print('\n=== T-01.7 COMPLETADO ===')
