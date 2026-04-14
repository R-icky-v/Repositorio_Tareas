import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
#from database.entrega_queries import registrar_entrega
# Dentro de views/subir_tarea_view.py
from database.tarea_queries import registrar_entrega

class SubirTareaView(tk.Toplevel):
    def __init__(self, parent, id_tarea, id_estudiante, fecha_limite_str):
        super().__init__(parent)
        self.title("Entregar Tarea")
        self.geometry("500x400")
        self.id_tarea = id_tarea
        self.id_estudiante = id_estudiante
        self.fecha_limite_str = fecha_limite_str
        
        self.archivo_seleccionado = None
        self.formatos_validos = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png'] # T-01.3
        
        self.crear_interfaz()

    def crear_interfaz(self):
        # --- NUEVA BARRA DE NAVEGACIÓN ---
        nav_frame = tk.Frame(self, bg='#f0f0f0')
        nav_frame.pack(fill="x", padx=10, pady=5)

        # Botón Atrás
        tk.Button(nav_frame, text="⬅ Atrás", command=self.destroy,
                  bg='#bdc3c7', relief='flat', padx=10).pack(side="left")

        # Botón Menú
        # Botón Menú
        def volver_a_perfiles():
            # Si existe un padre (Panel), al destruirlo se destruye todo automáticamente
            if self.master: 
                self.master.destroy() 
            else:
                self.destroy() # Por si acaso se abrió como ventana independiente
                
            from views.seleccion_perfil import abrir_seleccion_perfil
            abrir_seleccion_perfil()

        tk.Button(nav_frame, text="🏠 Menú Perfiles", command=volver_a_perfiles, 
                  bg='#a1c4fd', relief='flat', padx=10).pack(side="right")

        tk.Button(nav_frame, text="🏠 Menú Perfiles", command=volver_a_perfiles,
                  bg='#a1c4fd', relief='flat', padx=10).pack(side="right")

        # --- SEPARADOR VISUAL ---
        tk.Frame(self, height=1, bg='#cccccc').pack(fill="x", padx=10)

        # --- CÓDIGO ORIGINAL (Sin alteraciones) ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Subir Archivo de Entrega", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Área de carga (Simulada con un Label)
        self.frame_archivo = tk.Frame(main_frame, bg='#f9f9f9', bd=2, relief="groove")
        self.frame_archivo.pack(fill="x", pady=20, ipady=20)
        
        self.lbl_archivo = tk.Label(self.frame_archivo, text="No se ha seleccionado archivo", bg='#f9f9f9', fg='#777')
        self.lbl_archivo.pack()

        ttk.Button(main_frame, text="📁 Seleccionar Archivo", command=self.seleccionar_archivo).pack(pady=5)

        # Indicador de progreso (T-01.1)
        self.progreso = ttk.Progressbar(main_frame, mode='determinate', length=300)
        self.progreso.pack(pady=20)

        # Botón de envío (T-01.2)
        self.btn_enviar = tk.Button(
            main_frame, text="🚀 Confirmar Entrega", 
            command=self.procesar_entrega,
            bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
            state='disabled' # Bloqueado hasta que suba algo
        )
        self.btn_enviar.pack(fill="x", pady=10)

    def seleccionar_archivo(self):
        # T-01.4: Lógica de selección
        ruta = filedialog.askopenfilename(
            title="Seleccionar tarea",
            filetypes=[("Documentos", "*.pdf *.doc *.docx"), ("Imágenes", "*.jpg *.jpeg *.png")]
        )
        
        if ruta:
            # Validaciones de Seguridad (T-01.3 y T-01.6)
            ext = os.path.splitext(ruta)[1].lower()
            tamano_mb = os.path.getsize(ruta) / (1024 * 1024)

            if ext not in self.formatos_validos:
                messagebox.showerror("Error", "Formato no permitido (.exe y .bat están bloqueados)")
                return
            
            if tamano_mb > 5: # Máximo 5MB
                messagebox.showerror("Error", "El archivo excede los 5MB permitidos.")
                return

            self.archivo_seleccionado = ruta
            self.lbl_archivo.config(text=os.path.basename(ruta), fg='black')
            self.btn_enviar.config(state='normal')

    def procesar_entrega(self):
        # 1. Validar fecha
        ahora = datetime.now()
        limite = datetime.strptime(str(self.fecha_limite_str)[:16], '%Y-%m-%d %H:%M')

        if ahora > limite:
            messagebox.showerror("Plazo Vencido", "La fecha límite ha pasado.")
            return

        # 2. Animación de progreso (AHORA ESTÁ AISLADA)
        self.progreso['value'] = 0
        for i in range(1, 101, 20):
            self.update_idletasks()
            self.progreso['value'] = i
            self.after(100)

        # 3. Guardado físico (FUERA DEL BUCLE)
        try:
            nombre_original = os.path.basename(self.archivo_seleccionado)
            os.makedirs("uploads", exist_ok=True)
            # Usamos timestamp para que el nombre sea único y no choque
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_final = f"{self.id_estudiante}_{timestamp}_{nombre_original}"
            ruta_destino = os.path.join("uploads", nombre_final)
            
            shutil.copy(self.archivo_seleccionado, ruta_destino)
            
            # 4. Registro en BD (UNA SOLA VEZ)
            exito = registrar_entrega(
                self.id_tarea, 
                self.id_estudiante, 
                nombre_final, 
                ruta_destino
            )

            if exito:
                messagebox.showinfo("¡Éxito!", "Tarea entregada correctamente.")
                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo registrar en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar archivo: {e}")