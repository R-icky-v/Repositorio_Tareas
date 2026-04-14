import os

# estos si los acepto
formatos_ok = {'.pdf', '.doc', '.docx', '.jpeg', '.jpg'}

# estos jamas los dejo pasar
formatos_peligrosos = {'.exe', '.bat', '.msi'}

def revisar_archivo(nombre_archivo, id_estudiante, id_usuario):

    # verifico que sea el mismo estudiante el que entrega
    if id_estudiante != id_usuario:
        return False, "No puedes entregar por otro estudiante"

    # saco solo la extension del archivo, ej: .pdf
    _, ext = os.path.splitext(nombre_archivo)
    ext = ext.lower()

    # si es ejecutable lo bloqueo de una
    if ext in formatos_peligrosos:
        return False, f"Este tipo de archivo no está permitido ({ext})"

    # si no está en la lista de permitidos tampoco pasa
    if ext not in formatos_ok:
        return False, f"Formato no aceptado ({ext})"

    return True, "Archivo valido"