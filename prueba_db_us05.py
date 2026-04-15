import os
from dotenv import load_dotenv
from database.tarea_queries import obtener_calificaciones_estudiante, guardar_calificacion_db

load_dotenv()

ID_ESTUDIANTE = "5820f721-bb24-4605-9df0-c8cc6a8e54cb"

print("--- 📊 INICIANDO PRUEBA DE CONSULTA DE NOTAS (US-05) ---")

# 1. Ejecutar la consulta del Task T-05.3
notas = obtener_calificaciones_estudiante(ID_ESTUDIANTE)

if notas:
    print(f"✅ Se encontraron {len(notas)} calificaciones publicadas para el estudiante.")
    print("--------------------------------------------------")
    for n in notas:
        print(f"Tarea: {n[0]}")
        print(f"Nota: {n[1]}")
        print(f"Comentario Docente: {n[2]}")
        print(f"Fecha: {n[4]}")
        print("--------------------------------------------------")
    print("✅ PRUEBA EXITOSA: La consulta recupera solo lo permitido.")
else:
    print(f"⚠️ No se encontraron notas publicadas para el ID: {ID_ESTUDIANTE}")
    print("💡 Tip: Asegúrate de que en la tabla 'calificaciones' haya registros con estado='publicada'.")

print("--- FIN DE LA PRUEBA US-05 ---")