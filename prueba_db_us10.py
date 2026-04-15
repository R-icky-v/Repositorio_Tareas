import os
from dotenv import load_dotenv
from database.tarea_queries import guardar_calificacion_db, obtener_entregas_por_tarea

load_dotenv()

# --- CONFIGURACIÓN DE PRUEBA ---
ID_TAREA_PRUEBA = "548f091f-be09-4851-aaf0-509355a3a4dc" # Asegúrate de tener esto en tu .env o cámbialo manualmente
ID_ENTREGA_REAL = "f9484372-22c2-46da-9854-117cd44faa32" 

print("--- 📝 INICIANDO PRUEBA DE CALIFICACIONES (US-10) ---")

# 1. Simular calificación (T-10.6: Inserción)
print(f"Subiendo nota para entrega: {ID_ENTREGA_REAL}...")
exito_ins = guardar_calificacion_db(
    id_entrega=ID_ENTREGA_REAL, 
    nota=85.5, 
    comentario="Buen trabajo, pero faltó mejorar la documentación técnica.",
    estado='publicada'
)

if exito_ins:
    print("✅ Inserción/Actualización exitosa en la tabla 'calificaciones'.")
    
    # 2. Verificar consulta (T-10.6: Consulta por entrega)
    # Usamos la función que ya tienes para ver si la nota aparece vinculada
    entregas = obtener_entregas_por_tarea(ID_TAREA_PRUEBA)
    
    for e in entregas:
        if str(e[0]) == ID_ENTREGA_REAL:
            print("\n--- DATOS RECUPERADOS DE LA BD ---")
            print(f"Estudiante: {e[1]}")
            print(f"Nota: {e[4]}")
            print(f"Estado Nota: {e[5]}")
            print("----------------------------------")
            break
else:
    print("❌ Error al procesar la calificación en la BD.")

print("--- FIN DE LA PRUEBA US-10 ---")