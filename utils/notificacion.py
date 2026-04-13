from datetime import datetime

# guardo un registro de todo lo que se envio
notificaciones_enviadas = []

def enviar_notificacion(id_estudiante, nota):

    # armo el mensaje que le llega al estudiante
    texto = f"Tu profe publico tu calificacion: {nota}/100"

    registro = {
        "para": id_estudiante,
        "texto": texto,
        "enviado_el": datetime.now()
    }

    notificaciones_enviadas.append(registro)

    # por ahora simulo el envio, despues se conecta al sistema real
    print(f"[NOTIFICACION] estudiante {id_estudiante} -> {texto}")
    return True


def ver_notificaciones_enviadas():
    # sirve para verificar que si se mandaron
    return notificaciones_enviadas