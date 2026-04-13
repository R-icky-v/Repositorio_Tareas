from datetime import datetime
from database.conexion import get_conexion

def reemplazar_entrega(id_entrega, nueva_ruta, nuevo_nombre):
    try:
        conn = get_conexion()
        cursor = conn.cursor()

        # 🔍 1. Verificar que existe la entrega
        cursor.execute('''
            SELECT id FROM entregas WHERE id = %s AND estado = 'entregado'
        ''', (id_entrega,))
        
        entrega = cursor.fetchone()

        if not entrega:
            return {
                "ok": False,
                "error": "Entrega no encontrada o no válida"
            }

        # 🔄 2. Actualizar archivo y fecha
        cursor.execute('''
            UPDATE entregas
            SET ruta_archivo = %s,
                nombre_archivo = %s,
                fecha_entrega = %s
            WHERE id = %s
        ''', (nueva_ruta, nuevo_nombre, datetime.now(), id_entrega))

        conn.commit()

        cursor.close()
        conn.close()

        # ✅ 3. Confirmación
        return {
            "ok": True,
            "mensaje": "Entrega actualizada correctamente"
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }