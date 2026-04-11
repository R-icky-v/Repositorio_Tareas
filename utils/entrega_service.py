from datetime import datetime
from seguridad_entrega import revisar_archivo

class EntregaService:

    def __init__(self):
        # aquí van las entregas, mi compañero conecta la BD después
        self.lista_entregas = []

    def subir_archivos(self, archivos, id_estudiante, id_usuario, id_tarea):

        # no dejo pasar mas de 5 archivos
        if len(archivos) > 5:
            return "Error: solo se permiten hasta 5 archivos"

        archivos_guardados = []

        for archivo in archivos:

            # reviso seguridad antes de guardar cualquier cosa
            es_valido, mensaje = revisar_archivo(
                archivo["nombre"],
                id_estudiante,
                id_usuario
            )
            if not es_valido:
                return mensaje

            # el archivo no puede pesar mas de 5MB
            if archivo["tamano"] > 5 * 1024 * 1024:
                return f"Error: {archivo['nombre']} pesa mas de 5MB"

            # guardo la entrega con fecha y hora exacta
            nueva_entrega = {
                "id_tarea": id_tarea,
                "id_estudiante": id_estudiante,
                "nombre_archivo": archivo["nombre"],
                "cuando": datetime.now(),
                "estado": "entregado"
            }

            self.lista_entregas.append(nueva_entrega)
            archivos_guardados.append(nueva_entrega)

        return "Archivos entregados correctamente"

    # el docente usa esto para ver las entregas
    def ver_entregas(self):
        return self.lista_entregas