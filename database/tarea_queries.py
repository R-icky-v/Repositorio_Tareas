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
            JOIN cursos c ON t.id_curso = c.id
            WHERE t.id_docente = %s
            ORDER BY t.created_at DESC
        ''', (id_docente,))
        tareas = cursor.fetchall()
        print('Se encontraron ' + str(len(tareas)) + ' tareas')
        return tareas
    except Exception as e:
        print('Error al consultar: ' + str(e))
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
                   u.nombre AS docente
            FROM tareas t
            JOIN cursos c ON t.id_curso = c.id
            JOIN usuarios u ON t.id_docente = u.id
            WHERE t.id = %s
        ''', (id_tarea,))
        tarea = cursor.fetchone()
        if tarea:
            print('Tarea encontrada: ' + str(tarea))
        else:
            print('No se encontro la tarea')
        return tarea
    except Exception as e:
        print('Error al obtener detalle: ' + str(e))
    finally:
        cursor.close()
        conn.close()