import os
import subprocess
import platform
import tkinter as tk
from tkinter import ttk, messagebox
from database.tarea_queries import obtener_entregas_por_tarea

class ListaEntregasView(tk.Toplevel):
    def __init__(self, parent, id_tarea, titulo_tarea):
        super().__init__(parent)
        self.id_tarea = id_tarea
        self.titulo_tarea = titulo_tarea
        self.entregas_actuales = [] # <-- Inicializar vacía
        self._build_ui()
        self.cargar_datos()

    def _build_ui(self):
        # Encabezado simple
        header = tk.Frame(self, bg="#1A6FBF", height=50)
        header.pack(fill="x")
        tk.Label(header, text=f"Entregas: {self.titulo_tarea}", fg="white", bg="#1A6FBF", font=("Arial", 12, "bold")).pack(pady=10)

        # Tabla (Treeview)
        container = tk.Frame(self, padx=20, pady=20)
        container.pack(fill="both", expand=True)

        columnas = ("id", "estudiante", "fecha", "archivo", "estado")
        self.tabla = ttk.Treeview(container, columns=columnas, show="headings")
        
        self.tabla.heading("estudiante", text="Estudiante")
        self.tabla.heading("fecha", text="Fecha de Entrega")
        self.tabla.heading("archivo", text="Archivo")
        self.tabla.heading("estado", text="Calificación")
        
        # Ocultar columna ID
        self.tabla.column("id", width=0, stretch=False)
        self.tabla.pack(fill="both", expand=True)

        # --- NUEVO: Contenedor de botones (para evitar el AttributeError) ---
        self.frame_acciones = tk.Frame(self)
        self.frame_acciones.pack(pady=20)

        # Botón Ver Archivo
        self.btn_ver_archivo = tk.Button(
            self.frame_acciones, 
            text="📂 Ver Tarea Enviada", 
            command=self.ver_archivo_estudiante,
            bg="#3498db", 
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        )
        self.btn_ver_archivo.pack(side="left", padx=10)

        # Botón Calificar
        self.btn_calificar = tk.Button(
            self.frame_acciones, 
            text="⭐ Calificar Seleccionado", 
            bg="#27ae60", 
            fg="white", 
            command=self.abrir_calificador, 
            font=("Arial", 10, "bold"), 
            padx=10,
            pady=5
        )
        self.btn_calificar.pack(side="left", padx=10)

    def cargar_datos(self):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Obtener entregas
        self.entregas_raw = obtener_entregas_por_tarea(self.id_tarea)
        
        for entrega in self.entregas_raw:
            # Insertamos en la tabla solo lo visible
            # Pero guardamos el ID como iid para buscar la ruta después
            self.tabla.insert('', 'end', iid=entrega[0], values=(entrega[1], entrega[2], entrega[3], entrega[4]))

    def abrir_calificador(self):
        sel = self.tabla.selection()
        if not sel: return messagebox.showwarning("Atención", "Seleccione una entrega")
        
        # Pasamos los datos necesarios al panel de calificación (US-10)
        datos = self.tabla.item(sel)['values']
        from views.calificar_entrega_view import CalificarEntregaView
        CalificarEntregaView(self, datos, self.cargar_datos) # Pasamos callback para refrescar
    
    def ver_archivo_estudiante(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una entrega.")
            return

        # EL PROBLEMA ESTABA AQUÍ:
        # Estás usando valores_fila[0], pero en tu tabla la columna 0 es "Estudiante"
        # El ID real de la entrega lo guardamos internamente en el 'iid'
        id_entrega_sel = self.tabla.item(seleccion)['iid'] 

        print(f"DEBUG CORRECTO: Buscando ID real {id_entrega_sel}")
        
        ruta_archivo = None
        for entrega in self.entregas_actuales:
            if str(entrega[0]) == str(id_entrega_sel):
                ruta_archivo = entrega[6]
                break
        
        # Buscamos la ruta en la lista que SI tiene datos
        for entrega in self.entregas_actuales:
            if str(entrega[0]) == id_entrega_sel:
                ruta_archivo = entrega[6] # El índice 6 es ruta_archivo según tu query
                break

        if ruta_archivo and str(ruta_archivo).lower() != 'none':
            ruta_limpia = os.path.abspath(ruta_archivo)
            if os.path.exists(ruta_limpia):
                if os.name == 'nt':
                    os.startfile(ruta_limpia)
                else:
                    subprocess.call(['open', ruta_limpia])
            else:
                messagebox.showerror("Error", f"El archivo no existe en la ruta:\n{ruta_limpia}")
        else:
            messagebox.showerror("Error", "La ruta en la base de datos está vacía (None).")
        # ... (tu código actual)
        print(f"DEBUG: Buscando ID {id_entrega_sel}") 
        print(f"DEBUG: Contenido de entregas_actuales: {self.entregas_actuales}")