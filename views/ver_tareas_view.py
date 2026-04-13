import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Configuración de rutas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# CORRECCIÓN: Importamos la función que faltaba
from database.tarea_queries import obtener_tareas_docente, obtener_detalle_tarea, obtener_entregas_por_tarea

class VerTareasView(tk.Toplevel):
    def __init__(self, parent, id_docente):
        super().__init__(parent)
        self.title("Mis Tareas - Repositorio UMSS")
        self.geometry("900x500") 
        self.id_docente = id_docente
        
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Gestión de Tareas y Calificaciones", font=('Arial', 14, 'bold')).pack(pady=(0, 15))

        # --- Tabla (Treeview) ---
        columnas = ('ID', 'Título', 'Estado', 'Fecha Límite', 'Curso')
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show='headings')
        
        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Título', text='Título')
        self.tabla.heading('Estado', text='Estado')
        self.tabla.heading('Fecha Límite', text='Fecha Límite')
        self.tabla.heading('Curso', text='Curso')

        self.tabla.column('ID', width=80, anchor="center")
        self.tabla.column('Título', width=250)
        self.tabla.column('Estado', width=100, anchor="center")
        self.tabla.column('Fecha Límite', width=120, anchor="center")
        
        self.tabla.pack(fill="both", expand=True)
        
        self.tabla.bind("<Double-1>", self.abrir_entregas_estudiantes)

        # --- Panel de Botones ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=15)

        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos).pack(side="left")
        
        self.btn_entregas = tk.Button(
            btn_frame, 
            text="📥 Ver Entregas (Calificar)", 
            command=self.abrir_entregas_estudiantes,
            bg='#27ae60', 
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=10
        )
        self.btn_entregas.pack(side="left", padx=10)

        ttk.Button(btn_frame, text="🔍 Ver Detalle Tarea", command=self.abrir_detalle_seleccionado).pack(side="left")
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side="right")

    def cargar_datos(self):
        """Carga la lista de tareas creadas por el docente."""
        # 1. Limpiar la tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # 2. Obtener las tareas usando el ID del DOCENTE (no de la tarea)
        # Cambia la línea que está dando el error por esta:
        self.tareas_lista = obtener_tareas_docente(self.id_docente)
        
        # 3. Llenar la tabla si hay resultados
        if self.tareas_lista:
            for t in self.tareas_lista:
                # Insertamos los datos en las columnas correspondientes
                self.tabla.insert('', 'end', values=(
                    t[0], # ID de la tarea
                    t[1], # Titulo
                    t[4], # Estado
                    t[3], # Fecha Limite
                    t[5]  # Curso
                ))

    def abrir_entregas_estudiantes(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        # Aquí es donde recuperamos el ID de la fila seleccionada
        item = self.tabla.item(seleccion)
        id_tarea_seleccionada = item['values'][0] 
        titulo_tarea = item['values'][1]

        from views.lista_entregas_view import ListaEntregasView
        # Aquí es donde realmente nace el 'id_tarea' para la siguiente ventana
        ListaEntregasView(self, id_tarea_seleccionada, titulo_tarea)

    def abrir_detalle_seleccionado(self, event=None):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, selecciona una tarea.")
            return

        id_tarea = self.tabla.item(seleccion)['values'][0] 
        datos = obtener_detalle_tarea(id_tarea)

        if datos:
            from views.detalle_tarea_view import DetalleTareaView
            DetalleTareaView(self, datos)