class TareaService:

    def __init__(self):
        # lista temporal,falta conecta la BD
        self.tareas = []

    def guardar_borrador(self, datos):
        datos["estado"] = "borrador"
        self.tareas.append(datos)
        return "Tarea guardada como borrador"

    def publicar(self, datos):
        datos["estado"] = "publicada"
        self.tareas.append(datos)
        return "Tarea publicada correctamente"

    def editar(self, index, nuevos_datos):
        if index >= len(self.tareas):
            return "Error: tarea no existe"

        tarea = self.tareas[index]

        # no deja editar si ya fue publicada
        if tarea["estado"] == "publicada":
            return "No se puede editar una tarea publicada"

        tarea.update(nuevos_datos)
        return "Tarea editada correctamente"

    def eliminar(self, index):
        if index >= len(self.tareas):
            return "Error: tarea no existe"

        tarea = self.tareas[index]

        # tampoco se puede borrar si esta publicada
        if tarea["estado"] == "publicada":
            return "No se puede eliminar una tarea publicada"

        self.tareas.pop(index)
        return "Tarea eliminada"

    def cambiar_estado(self, index):
        if index >= len(self.tareas):
            return "Error: tarea no existe"

        tarea = self.tareas[index]

        # solo paso de borrador a publicada, no al reves
        if tarea["estado"] == "borrador":
            tarea["estado"] = "publicada"
            return "Tarea publicada"

        return "La tarea ya esta publicada"
