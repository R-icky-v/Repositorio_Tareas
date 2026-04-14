import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
from database.tarea_queries import actualizar_entrega_db, eliminar_entrega_db

class EditarEntregaView(tk.Toplevel):
    def __init__(self, parent, datos_entrega, id_tarea, id_estudiante, fecha_limite_str):
        super().__init__(parent)
        self.title("Editar Entrega")
        self.geometry("450x450")
        
        # Datos iniciales
        self.id_entrega = datos_entrega[0]
        self.archivo_actual = datos_entrega[1]
        self.ruta_actual = datos_entrega[2]
        self.id_tarea = id_tarea
        self.id_estudiante = id_estudiante
        self.fecha_limite = datetime.strptime(str(fecha_limite_str)[:16], '%Y-%m-%d %H:%M')
        
        self.nuevo_archivo = None
        self.crear_iu()

    def crear_iu(self):
        container = ttk.Frame(self, padding="20")
        container.pack(fill="both", expand=True)

        # Verificar si el plazo venció (T-02.1)
        vencido = datetime.now() > self.fecha_limite

        ttk.Label(container, text="Tu entrega actual:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.lbl_archivo = tk.Label(container, text=self.archivo_actual, bg="#fff3cd", fg="#856404", pady=10, width=40)
        self.lbl_archivo.pack(pady=10)

        if vencido:
            lbl_error = ttk.Label(container, text="⚠️ Plazo vencido. No se permiten cambios.", foreground="red")
            lbl_error.pack(pady=10)
            estado_btn = "disabled"
        else:
            estado_btn = "normal"

        ttk.Button(container, text="🔄 Reemplazar Archivo", state=estado_btn, command=self.seleccionar_nuevo).pack(fill="x", pady=5)
        
        btn_anular = tk.Button(container, text="🗑️ Anular Entrega", bg="#f8d7da", fg="#721c24", state=estado_btn, command=self.anular)
        btn_anular.pack(fill="x", pady=20)

        self.btn_guardar = tk.Button(container, text="💾 Guardar Cambios", bg="#28a745", fg="white", state="disabled", command=self.guardar)
        self.btn_guardar.pack(fill="x", pady=10)

    def seleccionar_nuevo(self):
        ruta = filedialog.askopenfilename()
        if not ruta: return
        
        # Aquí aplicaríamos las mismas validaciones de la US-01 (T-02.2)
        tamano = os.path.getsize(ruta) / (1024 * 1024)
        if tamano > 5:
            messagebox.showerror("Error", "El archivo supera los 5MB")
            return

        self.nuevo_archivo = ruta
        self.lbl_archivo.config(text=f"NUEVO: {os.path.basename(ruta)}", bg="#d4edda", fg="#155724")
        self.btn_guardar.config(state="normal")

    def guardar(self):
        nombre_base = os.path.basename(self.nuevo_archivo)
        ruta_final = os.path.join("uploads", f"ID_{self.id_estudiante}_{nombre_base}")
        
        # Copiar archivo físico
        shutil.copy(self.nuevo_archivo, ruta_final)
        
        if actualizar_entrega_db(self.id_entrega, nombre_base, ruta_final):
            messagebox.showinfo("Éxito", "Entrega actualizada correctamente.")
            self.destroy()
        # Dentro de la función guardar, antes de shutil.copy:
        if os.path.exists(self.ruta_actual):
            os.remove(self.ruta_actual) # Borramos el archivo viejo del disco

    def anular(self):
        pregunta = messagebox.askyesno("Confirmar", "¿Estás seguro de anular la entrega? Se borrará el archivo enviado.")
        if pregunta:
            if eliminar_entrega_db(self.id_entrega):
                messagebox.showinfo("Anulado", "La entrega ha sido eliminada.")
                self.destroy()