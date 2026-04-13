# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import get_conexion
#from database.tarea_queries import registrar_entrega


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

def obtener_tareas_estudiante(id_estudiante):
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        # Modificamos la consulta para hacer un LEFT JOIN con entregas
        # Si e.id no es nulo, significa que ya hay una entrega
        cursor.execute('''
            SELECT 
                t.id, 
                t.titulo, 
                t.fecha_limite, 
                COALESCE(e.estado, t.estado) as estado_actual, 
                c.nombre as curso,
                CASE WHEN e.id IS NOT NULL THEN 'entregado' ELSE 'pendiente' END as tracking
            FROM tareas t
            INNER JOIN cursos c ON t.id_curso = c.id
            INNER JOIN inscripciones i ON i.id_curso = c.id
            LEFT JOIN entregas e ON e.id_tarea = t.id AND e.id_estudiante = %s
            WHERE i.id_estudiante = %s
            ORDER BY t.fecha_limite ASC
        ''', (id_estudiante, id_estudiante))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error en BD al obtener tareas con tracking: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def registrar_entrega(id_tarea, id_estudiante, nombre_archivo, ruta_archivo):
    """Registra la entrega en la base de datos (T-01.5 y T-01.7)."""
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO entregas (id_tarea, id_estudiante, nombre_archivo, ruta_archivo, estado)
            VALUES (%s, %s, %s, %s, 'entregado')
            RETURNING id;
        """
        cursor.execute(query, (id_tarea, id_estudiante, nombre_archivo, ruta_archivo))
        id_entrega = cursor.fetchone()[0]
        
        conn.commit()
        return id_entrega
    except Exception as e:
        print(f"❌ Error al registrar entrega: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def obtener_entrega_estudiante(id_tarea, id_estudiante):
    """Obtiene los datos de una entrega específica (T-02.2)."""
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, nombre_archivo, ruta_archivo, fecha_entrega 
            FROM entregas 
            WHERE id_tarea = %s AND id_estudiante = %s
        ''', (id_tarea, id_estudiante))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def actualizar_entrega_db(id_entrega, nombre_archivo, ruta_archivo):
    """Reemplaza el archivo anterior por el nuevo (T-02.4)."""
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE entregas 
            SET nombre_archivo = %s, ruta_archivo = %s, fecha_entrega = CURRENT_TIMESTAMP
            WHERE id = %s
        ''', (nombre_archivo, ruta_archivo, id_entrega))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar entrega: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def eliminar_entrega_db(id_entrega):
    """Elimina el registro de la entrega (Anular entrega - T-02.1)."""
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM entregas WHERE id = %s', (id_entrega,))
        conn.commit()
        return True
    finally:
        cursor.close()
        conn.close()