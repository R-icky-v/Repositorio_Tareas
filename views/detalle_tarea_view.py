import tkinter as tk
from tkinter import ttk

class DetalleTareaView(tk.Toplevel):
    def __init__(self, parent, datos, id_estudiante=None): # Añadimos id_estudiante
        super().__init__(parent)
        self.title("Detalle de la Tarea")
        self.geometry("500x550") # Aumenté un poco el alto para el nuevo botón
        self.resizable(False, False)
        
        # Guardamos los datos para usarlos en las funciones
        self.datos = datos
        self.id_estudiante = id_estudiante
        
        # datos[0] = ID, datos[1] = titulo, datos[2] = descripcion, datos[3] = fecha...
        self.crear_iu(datos)

    def crear_iu(self, datos):
        container = ttk.Frame(self, padding="20")
        container.pack(fill="both", expand=True)

        # Título
        ttk.Label(container, text=datos[1], font=('Arial', 14, 'bold'), wraplength=450).pack(pady=(0, 10))
        
        # Info rápida (Curso y Docente)
        info_frame = ttk.Frame(container)
        info_frame.pack(fill="x", pady=5)
        
        ttk.Label(info_frame, text=f"Curso: {datos[5]}", font=('Arial', 10, 'italic')).pack(side="left")
        ttk.Label(info_frame, text=f"Estado: {datos[4].upper()}", foreground="blue").pack(side="right")

        # Descripción
        ttk.Label(container, text="Descripción:", font=('Arial', 11, 'bold')).pack(anchor="w", pady=(15, 5))
        
        text_area = tk.Text(container, height=8, font=('Arial', 10), bg="#f4f4f4", padx=10, pady=10)
        text_area.insert("1.0", datos[2])
        text_area.config(state="disabled")
        text_area.pack(fill="both", expand=True)

        # Fecha límite
        ttk.Label(container, text=f"Fecha de entrega: {datos[3]}", font=('Arial', 10, 'bold')).pack(pady=15)

        # --- BOTONES DE ACCIÓN ---
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x", pady=10)

        # SOLO mostrar botón de entrega si hay un id_estudiante
        if self.id_estudiante:
            # --- INICIO DE LA MODIFICACIÓN (US-02) ---
            from database.tarea_queries import obtener_entrega_estudiante
            
            # Consultamos si ya existe una entrega para cambiar el aspecto del botón
            entrega = obtener_entrega_estudiante(self.datos[0], self.id_estudiante)
            
            if entrega:
                texto_btn = "⚙️ Gestionar Entrega (Editar)"
                color_btn = "#f39c12"  # Naranja
            else:
                texto_btn = "📤 Entregar Tarea"
                color_btn = "#27ae60"  # Verde

            tk.Button(
                btn_frame, 
                text=texto_btn, 
                command=self.ir_a_entregar,
                bg=color_btn, 
                fg='white', 
                font=('Arial', 11, 'bold'),
                width=25, # Aumentado un poco para que quepa el texto
                cursor='hand2'
            ).pack(side="top", pady=5)
            # --- FIN DE LA MODIFICACIÓN ---

        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side="top", pady=5)

    def ir_a_entregar(self):
        """
        Función que decide si abrir la ventana de carga (US-01) 
        o la de edición/anulación (US-02).
        """
        from database.tarea_queries import obtener_entrega_estudiante
        from views.subir_tarea_view import SubirTareaView
        from views.editar_entrega_view import EditarEntregaView

        id_tarea = self.datos[0]
        id_estudiante = self.id_estudiante
        fecha_limite = self.datos[3]

        # 1. Buscamos si el estudiante ya tiene una entrega para esta tarea (T-02.2)
        entrega_existente = obtener_entrega_estudiante(id_tarea, id_estudiante)

        if entrega_existente:
            # 2. Si ya existe, abrimos la interfaz de edición (US-02)
            # Pasamos los datos de la entrega: id, nombre_archivo, ruta, etc.
            EditarEntregaView(self, entrega_existente, id_tarea, id_estudiante, fecha_limite)
        else:
            # 3. Si no hay entrega previa, abrimos la carga normal (US-01)
            SubirTareaView(self, id_tarea, id_estudiante, fecha_limite)