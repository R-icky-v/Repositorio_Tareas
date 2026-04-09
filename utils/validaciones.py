from datetime import datetime

def validar_tarea(titulo, fecha_limite, archivo_nombre):
    errores = []

    # 1. Título obligatorio
    if not titulo or titulo.strip() == "":
        errores.append("El título es obligatorio")

    # 2. Fecha válida
    try:
        fecha = datetime.strptime(fecha_limite, "%Y-%m-%d")
        hoy = datetime.now()

        if fecha < hoy:
            errores.append("La fecha límite no puede ser anterior a hoy")
    except:
        errores.append("Formato de fecha inválido")

    # 3. Validar archivo
    extensiones_permitidas = [".pdf", ".docx", ".png", ".jpg"]

    if archivo_nombre:
        if not any(archivo_nombre.endswith(ext) for ext in extensiones_permitidas):
            errores.append("Formato de archivo no permitido")

    return errores