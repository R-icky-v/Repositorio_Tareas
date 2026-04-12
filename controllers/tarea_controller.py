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
        """
        Método que llama la vista (Tkinter). 
        Retorna (True/False, "Mensaje de éxito o error")
        """
        
        # --- PASO 1: VALIDACIÓN (Tarea 09.3) ---
        errores = validar_tarea(titulo, fecha_limite, archivo_nombre)
        if errores:
            # Si hay errores en la lista, los unimos en un solo string
            return False, "\n".join(errores)

        # --- PASO 2: GUARDADO EN BASE DE DATOS (Tarea 09.7) ---
        # En tarea_controller.py
        try:
            # 1. Intentamos insertar la tarea
            id_tarea = insertar_tarea(titulo, descripcion, fecha_limite, id_curso, id_docente)
            
            if not id_tarea:
                return False, "La base de datos devolvió un ID vacío. Revisa la consola de VS Code."

            # --- AQUÍ VA EL CÓDIGO QUE DEBES AUMENTAR ---
            
            # 2. Si la inserción fue exitosa y el usuario marcó 'publicar'
            if publicar_ahora:
                # Llamamos a la función que ya tienen en tareas_queries.py
                cambiar_estado_tarea(id_tarea, 'publicada')
                return True, "¡Tarea creada y publicada exitosamente!"
            
            # --------------------------------------------

            # Si no se marcó publicar, simplemente termina como borrador
            return True, "Tarea guardada como borrador correctamente."

        except Exception as e:
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