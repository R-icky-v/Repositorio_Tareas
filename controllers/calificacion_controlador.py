from datetime import datetime
from notificacion import enviar_notificacion

# aqui guardo las notas mientras el compañero conecta la BD
mis_calificaciones = []

def gestionar_calificacion(id_entrega, id_estudiante, nota, comentario, accion):

    # la nota no puede salirse del rango
    if nota < 0 or nota > 100:
        return "Error: la nota tiene que ser entre 0 y 100"

    # el comentario no es obligatorio pero si lo pone que no se pase
    if comentario and len(comentario) > 500:
        return "Error: el comentario es muy largo, maximo 500 caracteres"

    # reviso si ya existe algo guardado para esta entrega
    calif_anterior = None
    for c in mis_calificaciones:
        if c["id_entrega"] == id_entrega:
            calif_anterior = c
            break

    if accion == "borrador":

        if calif_anterior:
            # ya existia, solo actualizo
            calif_anterior["nota"] = nota
            calif_anterior["comentario"] = comentario
            calif_anterior["estado"] = "borrador"
            return "Borrador actualizado"

        # primera vez que se guarda
        nueva_calif = {
            "id_entrega": id_entrega,
            "id_estudiante": id_estudiante,
            "nota": nota,
            "comentario": comentario,
            "estado": "borrador",
            "guardado_el": datetime.now()
        }
        mis_calificaciones.append(nueva_calif)
        return "Calificacion guardada en borrador"

    elif accion == "publicar":

        # no puedo publicar si no hay borrador primero
        if calif_anterior is None:
            return "Primero guarda un borrador"

        if calif_anterior["estado"] == "publicada":
            return "Esta nota ya estaba publicada"

        calif_anterior["nota"] = nota
        calif_anterior["comentario"] = comentario
        calif_anterior["estado"] = "publicada"
        calif_anterior["guardado_el"] = datetime.now()

        # notifico al estudiante que ya puede ver su nota
        enviar_notificacion(id_estudiante, nota)
        return "Nota publicada, estudiante notificado"

    elif accion == "editar":

        if calif_anterior is None:
            return "No hay nota guardada para editar"

        # no dejo editar si ya fue publicada
        if calif_anterior["estado"] == "publicada":
            return "No puedes editar una nota que ya se publico"

        calif_anterior["nota"] = nota
        calif_anterior["comentario"] = comentario
        calif_anterior["guardado_el"] = datetime.now()
        return "Nota editada correctamente"

    else:
        return "No reconozco esa accion"


def filtrar_entregas(id_estudiante=None, id_tarea=None):

    resultados = mis_calificaciones

    # si me pasan estudiante filtro por ese
    if id_estudiante:
        resultados = [c for c in resultados if c["id_estudiante"] == id_estudiante]

    # si me pasan tarea filtro por esa
    if id_tarea:
        resultados = [c for c in resultados if c.get("id_tarea") == id_tarea]

    if not resultados:
        return "No encontre nada con esos datos"

    return resultados