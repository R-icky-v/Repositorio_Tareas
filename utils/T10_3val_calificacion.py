def validar_calificacion(nota, comentario):
    errores = []

    # Validar nota
    if nota is None:
        errores.append("La calificación es obligatoria")
    else:
        if not isinstance(nota, (int, float)):
            errores.append("La calificación debe ser numérica")
        elif nota < 0 or nota > 100:
            errores.append("La calificación debe estar entre 0 y 100")

    # Validar comentario
    if comentario:
        if len(comentario) > 500:
            errores.append("El comentario no puede superar los 500 caracteres")

    return errores