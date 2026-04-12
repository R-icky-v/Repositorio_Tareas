import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configuración de rutas para encontrar la base de datos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.tarea_queries import obtener_tareas_docente

class VerTareasView(tk.Toplevel):
    def __init__(self, parent, id_docente):
        super().__init__(parent)
        self.title("Mis Tareas - Repositorio UMSS")
        self.geometry("800x450")
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
        self.tabla.column('ID', width=80, anchor="center")
        self.tabla.column('Título', width=200)
        self.tabla.column('Estado', width=100, anchor="center")
        self.tabla.column('Fecha Límite', width=120, anchor="center")
        
        self.tabla.pack(fill="both", expand=True)

        ttk.Button(main_frame, text="Actualizar Lista", command=self.cargar_datos).pack(side="left", pady=10)
        ttk.Button(main_frame, text="Cerrar", command=self.destroy).pack(side="right", pady=10)

    def cargar_datos(self):
        # 1. Limpiar la tabla
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        # 2. Obtener datos
        tareas = obtener_tareas_docente(self.id_docente)
        
        # 3. Insertar con mapeo explícito
        if tareas:
            for t in tareas:
                # Mapeo según tu SELECT (id, titulo, desc, fecha, estado, curso)
                id_db      = t[0]
                titulo_db  = t[1]
                fecha_db   = t[3]
                estado_db  = t[4] # <--- ESTE ES EL ESTADO REAL
                curso_db   = t[5] if t[5] else "General / Sin Curso"

                # Insertar en el orden de las columnas de tu Treeview
                # Verifica que tus columnas sean: ('ID', 'Título', 'Estado', 'Fecha Límite', 'Curso')
                self.tabla.insert('', 'end', values=(
                    str(id_db)[:8], 
                    titulo_db, 
                    estado_db.upper(), # Lo forzamos a mayúsculas para verificar
                    fecha_db, 
                    curso_db
                ))
            print(f"✅ Interfaz cargada con {len(tareas)} tareas.")
        else:
            print("⚠️ La base de datos no devolvió tareas para este ID de docente.")