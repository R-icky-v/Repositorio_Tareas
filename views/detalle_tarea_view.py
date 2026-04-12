import tkinter as tk
from tkinter import ttk

class DetalleTareaView(tk.Toplevel):
    def __init__(self, parent, datos):
        super().__init__(parent)
        self.title("Detalle de la Tarea")
        self.geometry("500x450")
        self.resizable(False, False)
        
        # datos[1] = titulo, datos[2] = descripcion, etc.
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
        
        text_area = tk.Text(container, height=10, font=('Arial', 10), bg="#f4f4f4", padx=10, pady=10)
        text_area.insert("1.0", datos[2])
        text_area.config(state="disabled") # Para que no lo editen aquí
        text_area.pack(fill="both", expand=True)

        # Fecha límite
        ttk.Label(container, text=f"Fecha de entrega: {datos[3]}", font=('Arial', 10, 'bold')).pack(pady=15)

        ttk.Button(container, text="Cerrar", command=self.destroy).pack()