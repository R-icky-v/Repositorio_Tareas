import os
from dotenv import load_dotenv
from database.tarea_queries import actualizar_entrega_db, obtener_entrega_estudiante

# 1. Cargar variables del .env
load_dotenv()

ID_ESTUDIANTE = os.getenv("ID_ESTUDIANTE")
# Nota: Necesitamos un ID_TAREA real que esté vinculado a ese estudiante en la tabla entregas
# Por ahora usaré el ID_CURSO como referencia, pero asegúrate de que sea un ID de la tabla 'tareas'
ID_TAREA = "7890bf97-a376-40be-a603-4980705f324a" 

print("--- 🧪 INICIANDO PRUEBA DE BASE DE DATOS (US-02) ---")

# 2. Intentar buscar la entrega actual
entrega = obtener_entrega_estudiante(ID_TAREA, ID_ESTUDIANTE)

if entrega:
    id_entrega_real = entrega[0]
    nombre_viejo = entrega[1]
    
    print(f"✅ Entrega encontrada (ID: {id_entrega_real})")
    print(f"📄 Archivo actual: {nombre_viejo}")
    print("--------------------------------------------------")
    
    # 3. Ejecutar la actualización (Simulando T-02.4)
    nuevo_nombre = "entrega_modificada_v2.pdf"
    nueva_ruta = f"C:/uploads/{nuevo_nombre}"
    
    print(f"🔄 Actualizando a: {nuevo_nombre}...")
    exito = actualizar_entrega_db(id_entrega_real, nuevo_nombre, nueva_ruta)
    
    if exito:
        # 4. Verificar el cambio final
        entrega_final = obtener_entrega_estudiante(ID_TAREA, ID_ESTUDIANTE)
        print(f"✨ RESULTADO FINAL: {entrega_final[1]}")
        print(f"⏰ TIMESTAMP ACTUALIZADO: {entrega_final[3]}")
        print("\n✅ PRUEBA EXITOSA: La BD procesó el UUID y el CURRENT_TIMESTAMP correctamente.")
    else:
        print("❌ Error al ejecutar el UPDATE en la base de datos.")
else:
    print(f"⚠️ No se encontró una entrega para el Estudiante {ID_ESTUDIANTE} en la Tarea {ID_TAREA}.")
    print("💡 Tip: Ve a Supabase, busca la tabla 'entregas' y copia un 'id_tarea' que ya tenga registro.")

print("--- FIN DE LA PRUEBA ---")