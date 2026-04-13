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
        # 1. Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # 2. OBTENER ENTREGAS (Cambiado a entregas_actuales)
        self.entregas_actuales = obtener_entregas_por_tarea(self.id_tarea)
        
        if self.entregas_actuales:
            for entrega in self.entregas_actuales:
                # Insertamos usando el ID de la base de datos (entrega[0]) como iid
                self.tabla.insert('', 'end', iid=entrega[0], values=(
                    entrega[1], # Estudiante
                    entrega[2], # Fecha
                    entrega[3], # Archivo
                    f"{entrega[4] if entrega[4] else 'Sin nota'}" # Estado/Nota
                ))

    def abrir_calificador(self):
        sel = self.tabla.selection()
        if not sel: return messagebox.showwarning("Atención", "Seleccione una entrega")
        
        # --- LA SOLUCIÓN ESTÁ AQUÍ ---
        # 1. Recuperamos el ID real que guardamos de forma invisible en el 'iid'
        id_entrega_real = str(sel[0]) 
        
        # 2. Recuperamos los valores visibles de la tabla
        valores_visibles = self.tabla.item(sel)['values']
        nombre_estudiante = valores_visibles[0] # Ahora sabemos que el índice 0 es el nombre
        
        # 3. Armamos un paquete con exactamente lo que CalificarEntregaView espera recibir: [ID, Nombre]
        datos_correctos = [id_entrega_real, nombre_estudiante]
        
        from views.calificar_entrega_view import CalificarEntregaView
        CalificarEntregaView(self, datos_correctos, self.cargar_datos) # Pasamos callback para refrescar
    
    def ver_archivo_estudiante(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una entrega.")
            return

        # SOLUCIÓN AL KEYERROR: En Tkinter, el iid es la selección misma
        id_entrega_sel = str(seleccion[0]) 

        ruta_archivo = None
        
        # Buscamos la ruta en la lista que SI llenamos (entregas_actuales)
        for entrega in self.entregas_actuales:
            if str(entrega[0]) == id_entrega_sel:
                ruta_archivo = entrega[6] # El índice 6 es ruta_archivo en tu DB
                break

        if ruta_archivo and str(ruta_archivo).lower() != 'none':
            ruta_limpia = os.path.abspath(ruta_archivo)
            if os.path.exists(ruta_limpia):
                if os.name == 'nt':
                    os.startfile(ruta_limpia)
                else:
                    subprocess.call(['open', ruta_limpia])
            else:
                messagebox.showerror("Error", f"Archivo no encontrado físicamente en:\n{ruta_limpia}")
        else:
            messagebox.showerror("Error", "No se encontró la ruta del archivo (está vacía en la BD).")