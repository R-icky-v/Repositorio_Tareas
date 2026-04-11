from datetime import datetime
from utils.validaciones_archivos import validar_archivos
from database.conexion import get_conexion

def procesar_entrega(id_tarea, id_estudiante, archivos):
    try:
        # 1. Validar archivos
        errores = validar_archivos(archivos)
        if errores:
            return {"ok": False, "errores": errores}

        # 2. Verificar fecha límite
        conn = get_conexion()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT fecha_limite FROM tareas WHERE id = %s;",
            (id_tarea,)
        )
        fila = cursor.fetchone()

        if not fila:
            return {"ok": False, "errores": ["Tarea no encontrada"]}

        fecha_limite = fila[0]

        if datetime.now() > fecha_limite:
            return {"ok": False, "errores": ["La fecha límite ha expirado"]}

        # 3. Guardar entrega (simulado)
        for archivo in archivos:
            print(f"Guardando archivo: {archivo['nombre']}")

        cursor.close()
        conn.close()

        return {"ok": True, "mensaje": "Entrega realizada correctamente"}

    except Exception as e:
        return {"ok": False, "errores": [str(e)]}