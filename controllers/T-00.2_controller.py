from database.conexion import get_conexion

def formatear_estado(estado):
    if estado == "publicada":
        return "Pendiente"
    elif estado == "borrador":
        return "No disponible"
    return estado

def obtener_tarea_por_id(id_tarea):
    try:
        conn = get_conexion()

        with conn.cursor() as cursor:
            query = """
            SELECT titulo, descripcion, fecha_limite, estado
            FROM tareas
            WHERE id = %s;
            """

            cursor.execute(query, (id_tarea,))
            fila = cursor.fetchone()

        conn.close()

        if fila:
            return {
                "titulo": fila[0],
                "descripcion": fila[1],
                "fecha_limite": fila[2],
                "estado": formatear_estado(fila[3])
            }
        else:
            return None

    except Exception as e:
        print("❌ Error al obtener tarea:", e)
        return None