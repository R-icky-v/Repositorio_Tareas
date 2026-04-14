from datetime import datetime
from entrega_service import EntregaService
import os

service = EntregaService()

# formatos que acepto
formatos_ok = {'.pdf', '.doc', '.docx', '.jpeg', '.jpg'}

def buscar_entrega(id_tarea, id_estudiante):
    # busco la entrega del estudiante en esa tarea
    for e in service.lista_entregas:
        if e["id_tarea"] == id_tarea and e["id_estudiante"] == id_estudiante:
            return e
    return None

def plazo_vencido(fecha_limite):
    # verifico si ya paso la fecha
    limite = datetime.strptime(fecha_limite, "%Y-%m-%d").date()
    return datetime.now().date() > limite

def editar_entrega(id_estudiante, id_usuario, id_tarea, nuevo_archivo, fecha_limite):

    if id_estudiante != id_usuario:
        return "No puedes editar la entrega de otro"

    entrega = buscar_entrega(id_tarea, id_estudiante)
    if entrega is None:
        return "No existe entrega previa"

    if plazo_vencido(fecha_limite):
        return "El plazo ya venció"

    # valido el archivo nuevo
    _, ext = os.path.splitext(nuevo_archivo["nombre"])
    if ext.lower() not in formatos_ok:
        return f"Formato no permitido ({ext})"

    if nuevo_archivo["tamano"] > 5 * 1024 * 1024:
        return f"{nuevo_archivo['nombre']} pesa mas de 5MB"

    # reemplazo y actualizo
    entrega["nombre_archivo"] = nuevo_archivo["nombre"]
    entrega["cuando"] = datetime.now()
    entrega["estado"] = "editado"
    return "Entrega actualizada"

def anular_entrega(id_estudiante, id_usuario, id_tarea, fecha_limite):

    if id_estudiante != id_usuario:
        return "No puedes anular la entrega de otro"

    entrega = buscar_entrega(id_tarea, id_estudiante)
    if entrega is None:
        return "No hay entrega para anular"

    if plazo_vencido(fecha_limite):
        return "El plazo ya venció"

    entrega["estado"] = "anulado"
    return "Entrega anulada"