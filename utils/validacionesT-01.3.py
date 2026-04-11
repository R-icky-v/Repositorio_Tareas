import os

FORMATOS_PERMITIDOS = [".pdf", ".doc", ".jpeg", ".jpg"]
EXTENSIONES_BLOQUEADAS = [".exe", ".bat"]
TAM_MAX = 5 * 1024 * 1024  # 5MB
MAX_ARCHIVOS = 5

def validar_archivos(archivos):
    errores = []

    if len(archivos) > MAX_ARCHIVOS:
        errores.append("Máximo 5 archivos permitidos")

    for archivo in archivos:
        nombre = archivo["nombre"]
        tamaño = archivo["tamaño"]

        ext = os.path.splitext(nombre)[1].lower()

        if ext in EXTENSIONES_BLOQUEADAS:
            errores.append(f"Archivo bloqueado: {nombre}")

        if ext not in FORMATOS_PERMITIDOS:
            errores.append(f"Formato no permitido: {nombre}")

        if tamaño > TAM_MAX:
            errores.append(f"Archivo supera 5MB: {nombre}")

    return errores