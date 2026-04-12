import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configuración de rutas para encontrar el controlador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORTACIONES
from controllers.tarea_controller import TareaController
# --- CAMBIO 1: Importamos tu nuevo componente (T-09.2) ---
from views.components.file_picker import FilePicker 

class CrearTareaView(tk.Toplevel):
    def __init__(self, parent, id_curso, id_docente):
        super().__init__(parent)
        self.title("Crear Nueva Tarea - UMSS")
        self.geometry("500x600")
        
        self.id_curso = id_curso
        self.id_docente = id_docente
        self.controlador = TareaController()
        
        # --- CAMBIO 2: Ya no necesitamos self.ruta_archivo_seleccionado aquí ---
        # porque el componente FilePicker se encargará de eso.

        self.crear_interfaz()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # --- Título ---
        ttk.Label(main_frame, text="Título de la Tarea:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(10, 0))
        self.ent_titulo = ttk.Entry(main_frame, width=50)
        self.ent_titulo.pack(fill="x", pady=5)

        # --- Descripción ---
        ttk.Label(main_frame, text="Descripción:", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(10, 0))
        self.txt_desc = tk.Text(main_frame, height=5, width=50)
        self.txt_desc.pack(fill="x", pady=5)

        # --- Fecha Límite ---
        ttk.Label(main_frame, text="Fecha Límite (YYYY-MM-DD):", font=('Arial', 10, 'bold')).pack(anchor="w", pady=(10, 0))
        self.ent_fecha = ttk.Entry(main_frame, width=50)
        self.ent_fecha.insert(0, "2026-06-30") 
        self.ent_fecha.pack(fill="x", pady=5)

        # --- CAMBIO 3: Usamos el componente FilePicker (T-09.2) ---
        # Reemplazamos todo el bloque anterior de file_frame y el botón
        self.picker_adjunto = FilePicker(main_frame, label_text="Material Adjunto:")
        self.picker_adjunto.pack(fill="x", pady=15)

        # --- Botones de Acción ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=30)

        btn_borrador = ttk.Button(btn_frame, text="Guardar Borrador", 
                                 command=lambda: self.enviar_datos(publicar=False))
        btn_borrador.pack(side="left", padx=5, expand=True, fill="x")

        btn_publicar = ttk.Button(btn_frame, text="🚀 Publicar Tarea", 
                                 command=lambda: self.enviar_datos(publicar=True))
        btn_publicar.pack(side="right", padx=5, expand=True, fill="x")

    # --- CAMBIO 4: Borramos el método seleccionar_archivo() ---
    # Ya no es necesario porque está dentro del componente FilePicker.

    def enviar_datos(self, publicar):
        # 1. Recolectar datos de la GUI
        titulo = self.ent_titulo.get()
        descripcion = self.txt_desc.get("1.0", "end-1c")
        fecha = self.ent_fecha.get()
        
        # --- CAMBIO 5: Obtenemos el nombre del archivo desde el componente ---
        nombre_archivo = self.picker_adjunto.get_file_name()

        # 2. Llamar al controlador
        exito, mensaje = self.controlador.guardar_nueva_tarea(
            titulo, descripcion, fecha, self.id_curso, self.id_docente, nombre_archivo, publicar_ahora=publicar
        )

        # 3. Mostrar resultado al usuario
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.destroy() 
        else:
            messagebox.showerror("Atención", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # IDs de prueba
    ID_CURSO_VALIDO = "c3808b8b-dab9-47f1-9809-dcd2848849d4" 
    ID_DOCENTE_VALIDO = "5820f721-bb24-4605-9df0-c8cc6a8e54cb"
    
    app = CrearTareaView(root, ID_CURSO_VALIDO, ID_DOCENTE_VALIDO)
    root.mainloop()