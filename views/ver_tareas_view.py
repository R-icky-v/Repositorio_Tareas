import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configuración de rutas para encontrar la base de datos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.tarea_queries import obtener_tareas_docente, obtener_detalle_tarea

class VerTareasView(tk.Toplevel):
    def __init__(self, parent, id_docente):
        super().__init__(parent)
        self.title("Mis Tareas - Repositorio UMSS")
        self.geometry("800x500") # Aumenté un poco el alto para el botón extra
        self.id_docente = id_docente
        
        self.crear_interfaz()
        # Llamamos a la función de carga después de crear la interfaz
        self.cargar_datos()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Listado General de Tareas", font=('Arial', 14, 'bold')).pack(pady=(0, 15))

        # --- Tabla (Treeview) ---
        columnas = ('ID', 'Título', 'Estado', 'Fecha Límite', 'Curso')
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show='headings')
        
        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Título', text='Título')
        self.tabla.heading('Estado', text='Estado')
        self.tabla.heading('Fecha Límite', text='Fecha Límite')
        self.tabla.heading('Curso', text='Curso')

        # Ajuste de columnas
        self.tabla.column('ID', width=100, anchor="center") # Un poco más ancho para el UUID completo
        self.tabla.column('Título', width=200)
        self.tabla.column('Estado', width=100, anchor="center")
        self.tabla.column('Fecha Límite', width=120, anchor="center")
        
        self.tabla.pack(fill="both", expand=True)
        
        # Evento de doble clic
        self.tabla.bind("<Double-1>", self.abrir_detalle_seleccionado)

        # --- Panel de Botones inferior ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=15)

        ttk.Button(btn_frame, text="🔄 Actualizar Lista", command=self.cargar_datos).pack(side="left")
        
        # EL NUEVO BOTÓN (Capa de Controlador/IU)
        ttk.Button(btn_frame, text="🔍 Ver Detalle", command=self.abrir_detalle_seleccionado).pack(side="left", padx=10)
        
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side="right")

    def cargar_datos(self):
        # 1. Limpiar la tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        # 2. Obtener datos
        tareas = obtener_tareas_docente(self.id_docente)
        
        # 3. Insertar con mapeo explícito
        if tareas:
            for t in tareas:
                id_db      = t[0]
                titulo_db  = t[1]
                fecha_db   = t[3]
                estado_db  = t[4] 
                curso_db   = t[5] if t[5] else "General / Sin Curso"

                self.tabla.insert('', 'end', values=(
                    id_db, 
                    titulo_db, 
                    estado_db.upper(), 
                    fecha_db, 
                    curso_db
                ))
            print(f"✅ Interfaz cargada con {len(tareas)} tareas.")
        else:
            print("⚠️ La base de datos no devolvió tareas para este ID de docente.")

    # --- MÉTODO CONTROLADOR (Une la IU con la BD) ---
    def abrir_detalle_seleccionado(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona una tarea de la lista.")
            return

        # 1. Obtenemos el ID de la fila seleccionada
        item = self.tabla.item(seleccion)
        id_tarea = item['values'][0] 

        # 2. Consultamos a la BD usando ese ID (Capa Modelo)
        datos = obtener_detalle_tarea(id_tarea)

        # 3. Lanzamos la ventana de detalle (Capa Vista Detalle)
        if datos:
            from views.detalle_tarea_view import DetalleTareaView
            DetalleTareaView(self, datos)
        else:
            messagebox.showerror("Error", "No se pudo cargar la información completa de la tarea.")