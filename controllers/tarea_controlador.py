from servicio_tarea import TareaService
from datetime import datetime

service = TareaService()

def procesar_tarea(datos):
    titulo = datos.get("titulo")
    descripcion = datos.get("descripcion")
    fecha_limite = datos.get("fecha_limite")
    archivo = datos.get("archivo")
    estado = datos.get("estado")

    # el titulo no puede ir vacio
    if not titulo or titulo.strip() == "":
        return "Error: El título es obligatorio"

    # verifico que la fecha no sea del pasado
    if fecha_limite:
        hoy = datetime.now().date()
        fecha = datetime.strptime(fecha_limite, "%Y-%m-%d").date()
        if fecha < hoy:
            return "Error: Fecha límite no válida"

    # solo acepto estos formatos de archivo
    if archivo:
        if not archivo.endswith((".pdf", ".doc", ".docx")):
            return "Error: Formato de archivo no permitido"

    # depende del estado llamo a publicar o guardar
    if estado == "publicada":
        return service.publicar(datos)
    else:
        return service.guardar_borrador(datos)
