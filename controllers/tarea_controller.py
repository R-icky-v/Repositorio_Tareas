import sys
import os

# Esto permite que el controlador encuentre las carpetas database y utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Importamos la validación del compañero (Capa 2)
from utils.validaciones import validar_tarea

# 2. Importamos las consultas del compañero (Capa 1)
# Usamos el nombre exacto que definieron: tareas_queries.py
from database.tarea_queries import (
    insertar_tarea,
    cambiar_estado_tarea,
    obtener_detalle_tarea,
    eliminar_tarea
)

class TareaController:
    """
    Controlador para la US-09: Gestiona el flujo entre la UI y la persistencia.
    """

    def guardar_nueva_tarea(self, titulo, descripcion, fecha_limite, id_curso, id_docente, archivo_nombre, publicar_ahora=False):
        # --- PASO 1: VALIDACIÓN ---
        errores = validar_tarea(titulo, fecha_limite, archivo_nombre)
        if errores:
            return False, "\n".join(errores)

        # --- PASO 2: GUARDADO ---
        try:
            # Determinamos el estado inicial antes de insertar
            estado_inicial = 'publicada' if publicar_ahora else 'borrador'
            
            # 💡 IMPORTANTE: Modificamos la llamada para que inserte con el estado correcto de una vez
            # Nota: Asegúrate de que tu insertar_tarea en tareas_queries acepte el estado como parámetro
            # Si no lo acepta, usa el parche de abajo.
            
            id_tarea = insertar_tarea(titulo, descripcion, fecha_limite, id_curso, id_docente)
            
            if not id_tarea:
                return False, "Error: No se pudo generar el ID de la tarea."

            # Si el usuario pidió publicar, aseguramos el estado ahora mismo
            if publicar_ahora:
                cambiar_estado_tarea(id_tarea, 'publicada')
                return True, "¡Tarea creada y publicada exitosamente!"
            
            return True, "Tarea guardada como borrador correctamente."

        except Exception as e:
            print(f"DEBUG ERROR: {e}") # Esto lo verás en la consola de VS Code
            return False, f"Error técnico: {str(e)}"

    def borrar_tarea_si_es_posible(self, id_tarea):
        """
        Regla de negocio: Solo borrar si no está publicada.
        """
        tarea = obtener_detalle_tarea(id_tarea)
        if not tarea:
            return False, "La tarea no existe."

        # Según su SELECT en tareas_queries.py, el estado es el índice 4
        if tarea[4] == 'publicada':
            return False, "No está permitido eliminar tareas ya publicadas."

        try:
            eliminar_tarea(id_tarea)
            return True, "Tarea eliminada exitosamente."
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"