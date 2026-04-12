import sys
import os

# 1. Aseguramos la ruta (ajusta según donde esté el archivo)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from controllers.tarea_controller import TareaController

def ejecutar_prueba():
    print("🚀 Iniciando prueba de integración...") # <-- Mensaje de inicio
    
    controlador = TareaController()
    
    # 2. Datos de prueba (Usa IDs que existan en tu BD)
    titulo = "Tarea de Sistemas de Info"
    desc = "Prueba integral de las capas 1, 2 y 3"
    fecha = "2026-05-20"
    id_curso = "c3808b8b-dab9-47f1-9809-dcd2848849d4"
    id_docente = "9767c5f3-d0fa-462a-b58e-8fec9362120f"
    archivo = "clase1.pdf"

    print(f"📡 Enviando datos al controlador para: {titulo}...")

    # 3. CAPTURAMOS EL RESULTADO
    # Recuerda que nuestro controlador devuelve (Exito, Mensaje)
    exito, mensaje = controlador.guardar_nueva_tarea(
        titulo, desc, fecha, id_curso, id_docente, archivo, publicar_ahora=False
    )

    # 4. IMPRIMIMOS EL RESULTADO FINAL
    print("--- RESULTADO DE LA OPERACIÓN ---")
    if exito:
        print(f"✅ ÉXITO: {mensaje}")
    else:
        print(f"❌ FALLÓ: {mensaje}")
    print("---------------------------------")

if __name__ == "__main__":
    ejecutar_prueba()