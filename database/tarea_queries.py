# -*- coding: utf-8 -*-

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import get_conexion

def insertar_tarea(titulo, descripcion, fecha_limite, id_curso, id_docente):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, fecha_limite, estado, id_curso, id_docente)
            VALUES (%s, %s, %s, 'borrador', %s, %s)
            RETURNING id
        ''', (titulo, descripcion, fecha_limite, id_curso, id_docente))
        id_nueva = cursor.fetchone()[0]
        conn.commit()
        print(f'✅ Error al insertar con ID: {id_nueva}')
        return id_nueva
    except Exception as e:
        print(f'? Error al insertar: {e}')
    finally:
        cursor.close()
        conn.close()

def actualizar_tarea(id_tarea, titulo, descripcion, fecha_limite):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tareas
            SET titulo = %s, descripcion = %s, fecha_limite = %s
            WHERE id = %s
        ''', (titulo, descripcion, fecha_limite, id_tarea))
        conn.commit()
        print('? Tarea actualizada correctamente')
    except Exception as e:
        print(f'? Error al actualizar: {e}')
    finally:
        cursor.close()
        conn.close()

def cambiar_estado_tarea(id_tarea, nuevo_estado):
    try:
        if nuevo_estado not in ['borrador', 'publicada']:
            print('? Estado no v�lido')
            return
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tareas
            SET estado = %s
            WHERE id = %s
        ''', (nuevo_estado, id_tarea))
        conn.commit()
        print(f'? Estado cambiado a {nuevo_estado}')
    except Exception as e:
        print(f'? Error al cambiar estado: {e}')
    finally:
        cursor.close()
        conn.close()

def eliminar_tarea(id_tarea):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tareas WHERE id = %s', (id_tarea,))
        conn.commit()
        print('? Tarea eliminada correctamente')
    except Exception as e:
        print(f'? Error al eliminar: {e}')
    finally:
        cursor.close()
        conn.close()

def obtener_tareas_docente(id_docente):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.titulo, t.descripcion,
                   t.fecha_limite, t.estado, c.nombre
            FROM tareas t
            JOIN cursos c ON t.id_curso = c.id
            WHERE t.id_docente = %s
            ORDER BY t.created_at DESC
        ''', (id_docente,))
        tareas = cursor.fetchall()
        print(f'? Se encontraron {len(tareas)} tareas')
        return tareas
    except Exception as e:
        print(f'? Error al consultar: {e}')
    finally:
        cursor.close()
        conn.close()
