from database.conexion import get_conexion

def obtener_calificaciones_estudiante(id_estudiante, id_usuario_actual):
    try:
        #  1. Validar acceso (solo el propio estudiante)
        if id_estudiante != id_usuario_actual:
            return {
                "ok": False,
                "error": "Acceso no autorizado"
            }

        conn = get_conexion()
        cursor = conn.cursor()

        #  2. Obtener calificaciones (cuando exista la tabla)
        query = '''
            SELECT c.calificacion, c.estado
            FROM calificaciones c
            JOIN entregas e ON c.id_entrega = e.id
            WHERE e.id_estudiante = %s
        '''

        cursor.execute(query, (id_estudiante,))
        filas = cursor.fetchall()

        cursor.close()
        conn.close()

        # 🧹 3. Filtrar solo calificaciones publicadas
        calificaciones = [
            fila[0] for fila in filas if fila[1] == 'publicada'
        ]

        #  4. Calcular promedio
        if len(calificaciones) > 0:
            promedio = sum(calificaciones) / len(calificaciones)
        else:
            promedio = 0

        return {
            "ok": True,
            "calificaciones": calificaciones,
            "promedio": round(promedio, 2)
        }

    except Exception as e:
        # ⚠️ Manejo de error (por si aún no existe la tabla)
        return {
            "ok": False,
            "error": str(e)
        }