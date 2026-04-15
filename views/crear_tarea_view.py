import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configuración de rutas para encontrar el controlador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# IMPORTACIONES
from controllers.tarea_controller import TareaController
from views.components.file_picker import FilePicker 

class CrearTareaView(tk.Toplevel):
    def __init__(self, parent, id_curso, id_docente):
        super().__init__(parent)
        self.title("Crear Nueva Tarea - UMSS")
        self.geometry("500x600")
        
        self.id_curso = id_curso
        self.id_docente = id_docente
        self.controlador = TareaController()
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # --- NUEVA BARRA DE NAVEGACIÓN ---
        nav_frame = tk.Frame(self, bg='#f0f0f0')
        nav_frame.pack(fill="x", padx=10, pady=5)

        # Botón Atrás
        tk.Button(nav_frame, text="⬅ Atrás", command=self.destroy, 
                  bg='#bdc3c7', relief='flat', padx=10).pack(side="left")

        # Botón Menú
        def volver_a_perfiles():
            # Si existe un padre (Panel), al destruirlo se destruye todo automáticamente
            if self.master: 
                self.master.destroy() 
            else:
                self.destroy() 
                
            from views.seleccion_perfil import abrir_seleccion_perfil
            abrir_seleccion_perfil()

        # AQUÍ ESTABA EL DUPLICADO (Corregido: solo una vez)
        tk.Button(nav_frame, text="🏠 Menú Perfiles", command=volver_a_perfiles, 
                  bg='#a1c4fd', relief='flat', padx=10).pack(side="right")

        # --- SEPARADOR VISUAL ---
        tk.Frame(self, height=1, bg='#cccccc').pack(fill="x", padx=10)

        # --- CONTENIDO PRINCIPAL ---
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

        # --- Componente FilePicker ---
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

    def enviar_datos(self, publicar):
        titulo = self.ent_titulo.get()
        descripcion = self.txt_desc.get("1.0", "end-1c")
        fecha = self.ent_fecha.get()
        nombre_archivo = self.picker_adjunto.get_file_name()

        exito, mensaje = self.controlador.guardar_nueva_tarea(
            titulo, descripcion, fecha, self.id_curso, self.id_docente, nombre_archivo, publicar_ahora=publicar
        )

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.destroy() 
        else:
            messagebox.showerror("Atención", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    
    # IMPORTANTE: Usar los IDs de la sesión para que coincidan con el estudiante
    from database.sesion import IDS 
    
    ID_CURSO_VALIDO = IDS['curso'] 
    ID_DOCENTE_VALIDO = IDS['docente']
    
    app = CrearTareaView(root, ID_CURSO_VALIDO, ID_DOCENTE_VALIDO)
    root.mainloop()