import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Configuración de rutas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.tarea_queries import obtener_tareas_estudiante, obtener_detalle_tarea

class TareasEstudianteView(tk.Toplevel):
    def __init__(self, parent, id_estudiante):
        super().__init__(parent)
        self.title("Mis Tareas Pendientes")
        self.geometry("900x550")
        self.id_estudiante = id_estudiante
        
        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        # --- Cabecera y Filtros ---
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(header_frame, text="Panel de Tareas Pendientes", font=('Arial', 14, 'bold')).pack(side="left")
        
        # Filtro por Materia
        ttk.Label(header_frame, text=" Filtrar materia:").pack(side="left", padx=(20, 5))
        self.filtro_var = tk.StringVar()
        self.filtro_var.trace_add("write", lambda *args: self.aplicar_filtro())
        ttk.Entry(header_frame, textvariable=self.filtro_var).pack(side="left")

        # --- Tabla de Tareas ---
        columnas = ('ID', 'Materia', 'Tarea', 'Fecha Límite', 'Tiempo Restante', 'Estado')
        self.tabla = ttk.Treeview(main_frame, columns=columnas, show='headings')
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=120, anchor="center")
        
        self.tabla.column('Tarea', width=200) # Más espacio para el título
        self.tabla.pack(fill="both", expand=True)

        # --- AQUÍ VAN LOS COLORES (TAGS) ---
        self.tabla.tag_configure('urgente', background='#ffcccc')    # Rojo claro
        self.tabla.tag_configure('pendiente', background='#e1f5fe')   # Azul claro
        self.tabla.tag_configure('completado', background='#c8e6c9')  # VERDE suave (Nuevo)

        # Configuración de colores (Tags)
        self.tabla.tag_configure('urgente', background='#ffcccc') # Rojo claro para < 24h
        self.tabla.tag_configure('pendiente', background='#e1f5fe') # Azul claro normal

        # Vincular Doble Clic para ver detalle
        self.tabla.bind("<Double-1>", lambda e: self.abrir_detalle())

        # --- Botones ---
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=15)

        ttk.Button(btn_frame, text="🔄 Actualizar", command=self.cargar_datos).pack(side="left")
        ttk.Button(btn_frame, text="🔍 Ver Detalle / Entregar", command=self.abrir_detalle).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cerrar", command=self.destroy).pack(side="right")

    def calcular_tiempo_restante(self, fecha_limite_str):
        """Calcula cuánto falta y retorna el texto y la urgencia."""
        try:
            limite_limpio = str(fecha_limite_str)[:16]
            fecha_limite = datetime.strptime(limite_limpio, '%Y-%m-%d %H:%M')
            ahora = datetime.now()
            diferencia = fecha_limite - ahora

            if diferencia.total_seconds() <= 0:
                return "Plazo vencido", True
            
            dias = diferencia.days
            horas = diferencia.seconds // 3600
            
            if dias > 0:
                texto = f"{dias}d {horas}h restantes"
            else:
                texto = f"{horas}h restantes"

            es_urgente = (diferencia.total_seconds() < 86400) # Menos de 24 horas
            
            return texto, es_urgente
        except Exception as e:
            return "Fecha no válida", False

    def cargar_datos(self):
        self.todas_las_tareas = obtener_tareas_estudiante(self.id_estudiante)
        self.aplicar_filtro()

    def aplicar_filtro(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        
        busqueda = self.filtro_var.get().lower()

        for t in self.todas_las_tareas:
        # Ahora recibimos 6 valores de la nueva consulta
            id_db, titulo, fecha, estado, curso, tracking = t
        
            if busqueda in curso.lower() or busqueda in titulo.lower():
                tiempo_txt, urgente = self.calcular_tiempo_restante(fecha)
            
            # Lógica de colores priorizando la entrega
                if tracking == 'entregado':
                    tag = 'completado'
                    tiempo_txt = "✅ Enviado"
                    estado_mostrar = "ENTREGADO"
                else:
                    tag = 'urgente' if urgente else 'pendiente'
                    estado_mostrar = estado.upper()

                self.tabla.insert('', 'end', values=(
                    id_db, curso, titulo, fecha, tiempo_txt, estado_mostrar
                ), tags=(tag,))

    def abrir_detalle(self):
        """Aquí es donde ocurre la magia de conectar con el detalle."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una tarea de la lista.")
            return

        id_tarea = self.tabla.item(seleccion)['values'][0]
        datos = obtener_detalle_tarea(id_tarea)

        if datos:
            from views.detalle_tarea_view import DetalleTareaView
            # EL CAMBIO ESTÁ AQUÍ ABAJO: 
            # Agregamos self.id_estudiante al final para que la ventana de detalle 
            # sepa quién es el usuario y muestre el botón de entregar.
            DetalleTareaView(self, datos, self.id_estudiante) 
        else:
            messagebox.showerror("Error", "No se pudo cargar la información de la tarea.")