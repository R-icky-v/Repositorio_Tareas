from database.tarea_queries import guardar_calificacion_db
from tkinter import messagebox

class CalificacionController:
    @staticmethod
    def procesar_calificacion(id_entrega, nota, comentario, estado, nombre_estudiante):
        """
        Gestiona la lógica de negocio para guardar o publicar (T-10.4).
        """
        # 1. Intentar guardar en la Base de Datos (T-10.6)
        exito = guardar_calificacion_db(id_entrega, nota, comentario, estado)
        
        if exito:
            if estado == "publicada":
                # T-10.5: Simulación de notificación al estudiante
                print(f"NOTIFICACIÓN: Enviando alerta a {nombre_estudiante}...")
                messagebox.showinfo("Publicado", 
                    f"La nota de {nota} ha sido publicada. El estudiante ya puede verla.")
            else:
                messagebox.showinfo("Borrador", "Cambios guardados localmente.")
            return True
        else:
            messagebox.showerror("Error", "No se pudo conectar con la base de datos.")
            return False