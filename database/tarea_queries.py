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
        print('Tarea insertada con ID: ' + str(id_nueva))
        return id_nueva
    except Exception as e:
        print('Error al insertar: ' + str(e))
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
        print('Tarea actualizada correctamente')
    except Exception as e:
        print('Error al actualizar: ' + str(e))
    finally:
        cursor.close()
        conn.close()


def cambiar_estado_tarea(id_tarea, nuevo_estado):
    try:
        if nuevo_estado not in ['borrador', 'publicada']:
            print('Estado no valido')
            return
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tareas
            SET estado = %s
            WHERE id = %s
        ''', (nuevo_estado, id_tarea))
        conn.commit()
        print('Estado cambiado a: ' + nuevo_estado)
    except Exception as e:
        print('Error al cambiar estado: ' + str(e))
    finally:
        cursor.close()
        conn.close()


def eliminar_tarea(id_tarea):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tareas WHERE id = %s', (id_tarea,))
        conn.commit()
        print('Tarea eliminada correctamente')
    except Exception as e:
        print('Error al eliminar: ' + str(e))
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
            -- CAMBIO AQUÍ: Usamos LEFT JOIN para no perder tareas sin curso válido
            LEFT JOIN cursos c ON t.id_curso = c.id
            WHERE t.id_docente = %s
            ORDER BY t.created_at DESC
        ''', (id_docente,))
        
        tareas = cursor.fetchall()
        print('Se encontraron ' + str(len(tareas)) + ' tareas')
        return tareas
    except Exception as e:
        print('Error al consultar: ' + str(e))
        return [] # Retornamos lista vacía en lugar de None para evitar errores en la UI
    finally:
        cursor.close()
        conn.close()


def obtener_detalle_tarea(id_tarea):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.titulo, t.descripcion,
                   t.fecha_limite, t.estado,
                   c.nombre AS curso,
                   u.nombre || ' ' || u.apellido AS docente -- Concatenamos nombre y apellido
            FROM tareas t
            LEFT JOIN cursos c ON t.id_curso = c.id      -- LEFT JOIN para seguridad
            LEFT JOIN usuarios u ON t.id_docente = u.id   -- LEFT JOIN para seguridad
            WHERE t.id = %s
        ''', (id_tarea,))
        tarea = cursor.fetchone()
        return tarea
    except Exception as e:
        print('Error al obtener detalle: ' + str(e))
        return None
    finally:
        cursor.close()
        conn.close()

def insertar_entrega(id_tarea, id_estudiante, ruta_archivo, nombre_archivo):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO entregas (id_tarea, id_estudiante, ruta_archivo, nombre_archivo)
            VALUES (%s, %s, %s, %s)
            RETURNING id, fecha_entrega
        ''', (id_tarea, id_estudiante, ruta_archivo, nombre_archivo))
        resultado = cursor.fetchone()
        conn.commit()
        print('Entrega registrada con ID: ' + str(resultado[0]))
        print('Fecha de entrega: ' + str(resultado[1]))
        return resultado[0]
    except Exception as e:
        print('Error al insertar entrega: ' + str(e))
    finally:
        cursor.close()
        conn.close()


def obtener_entregas_por_tarea(id_tarea):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT e.id, e.ruta_archivo, e.nombre_archivo,
                   e.fecha_entrega, e.estado,
                   u.nombre, u.apellido
            FROM entregas e
            JOIN usuarios u ON e.id_estudiante = u.id
            WHERE e.id_tarea = %s
            ORDER BY e.fecha_entrega DESC
        ''', (id_tarea,))
        entregas = cursor.fetchall()
        print('Se encontraron ' + str(len(entregas)) + ' entregas')
        return entregas
    except Exception as e:
        print('Error al obtener entregas: ' + str(e))
    finally:
        cursor.close()
        conn.close()


def anular_entrega(id_entrega):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE entregas
            SET estado = 'anulado'
            WHERE id = %s
        ''', (id_entrega,))
        conn.commit()
        print('Entrega anulada correctamente')
    except Exception as e:
        print('Error al anular entrega: ' + str(e))
    finally:
        cursor.close()
        conn.close()