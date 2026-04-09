from database.tarea_queries import (
    insertar_tarea,
    actualizar_tarea,
    cambiar_estado_tarea,
    eliminar_tarea,
    obtener_tareas_docente
)

# Pega aquí los IDs de tus datos de prueba
ID_CURSO   = "uuid-del-curso"
ID_DOCENTE = "uuid-del-docente"

print("=== PROBANDO T-09.7 ===\n")

id_tarea = insertar_tarea(
    "Tarea 1 - Diagrama de flujo",
    "Realizar un diagrama de flujo",
    "2026-05-30 23:59:00",
    ID_CURSO,
    ID_DOCENTE
)

actualizar_tarea(id_tarea, "Tarea 1 - Actualizada", "Nueva descripción", "2026-06-15 23:59:00")

cambiar_estado_tarea(id_tarea, "publicada")

obtener_tareas_docente(ID_DOCENTE)

eliminar_tarea(id_tarea)

print("\n=== PRUEBAS FINALIZADAS ===")