import tkinter as tk
from tkinter import ttk
from controllers.calificaciones_estudiante_controller import CalificacionesEstudianteController

class VerCalificacionesView(tk.Toplevel):
    def __init__(self, parent, id_estudiante):
        super().__init__(parent)
        self.title("Mis Calificaciones - US-05")
        self.geometry("800x500") # Un poco más ancho para legibilidad
        self.id_estudiante = id_estudiante
        self._build_ui()
        self.cargar_datos()

    def _build_ui(self):
        # Frame superior para el promedio
        self.frame_top = tk.Frame(self, bg="#2c3e50", pady=20)
        self.frame_top.pack(fill="x")
        
        self.lbl_promedio = tk.Label(
            self.frame_top, text="Promedio Actual: --", 
            fg="white", bg="#2c3e50", font=("Arial", 14, "bold")
        )
        self.lbl_promedio.pack()

        # Contenedor principal
        container = tk.Frame(self, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Frame para la tabla y el scrollbar (T-05.1)
        tabla_frame = tk.Frame(container)
        tabla_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_frame)
        scrollbar.pack(side="right", fill="y")

        columnas = ("materia", "tarea", "nota", "comentario")
        self.tabla = ttk.Treeview(
            tabla_frame, 
            columns=columnas, 
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        # Configuración de encabezados
        self.tabla.heading("materia", text="ID Curso")
        self.tabla.heading("tarea", text="Tarea")
        self.tabla.heading("nota", text="Nota")
        self.tabla.heading("comentario", text="Feedback del Docente")

        # Configuración de columnas
        self.tabla.column("materia", width=100, anchor="center")
        self.tabla.column("tarea", width=150)
        self.tabla.column("nota", width=60, anchor="center")
        self.tabla.column("comentario", width=350)

        # Configurar color rojo para reprobados (T-05.1)
        self.tabla.tag_configure("reprobado", foreground="red")
        
        self.tabla.pack(fill="both", expand=True)
        scrollbar.config(command=self.tabla.yview)

    def cargar_datos(self):
        notas, promedio = CalificacionesEstudianteController.obtener_resumen_notas(self.id_estudiante)
        self.lbl_promedio.config(text=f"Promedio Actual: {promedio}")

        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if not notas:
            self.tabla.insert("", "end", values=("---", "Sin calificaciones publicadas", "---", "---"))
            return

        for n in notas:
            # Orden de base de datos: 0:titulo, 1:calificacion, 2:comentario, 3:curso_id
            tarea = n[0]
            calif = n[1]
            feedback = n[2] if n[2] else "Sin comentarios"
            materia = n[3]

            # Tag para reprobados (menor a 51)
            tag_color = "reprobado" if float(calif) < 51 else ""

            self.tabla.insert(
                "", 
                "end", 
                values=(materia, tarea, f"{calif}", feedback), 
                tags=(tag_color,)
            )