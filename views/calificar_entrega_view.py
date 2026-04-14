import tkinter as tk
from tkinter import messagebox
from database.tarea_queries import guardar_calificacion_db

class CalificarEntregaView(tk.Toplevel):
    def __init__(self, parent, datos_entrega, callback_refresh):
        super().__init__(parent)
        self.title("Calificar Entrega")
        self.geometry("450x550")
        self.id_entrega = datos_entrega[0]
        self.nombre_estudiante = datos_entrega[1]
        self.callback_refresh = callback_refresh
        self._build_ui()

    def _build_ui(self):
        body = tk.Frame(self, padx=20, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=f"Calificando a: {self.nombre_estudiante}", font=("Arial", 11, "bold")).pack(anchor="w")
        
        # Nota (T-10.2 / T-10.3)
        tk.Label(body, text="\nCalificación (0-100):").pack(anchor="w")
        self.ent_nota = tk.Entry(body, font=("Arial", 12))
        self.ent_nota.pack(fill="x", pady=5)

        # Comentarios (T-10.2 / T-10.3)
        tk.Label(body, text=f"\nRetroalimentación (máx. 500 car.):").pack(anchor="w")
        self.txt_comentario = tk.Text(body, height=8, font=("Arial", 10))
        self.txt_comentario.pack(fill="both", expand=True, pady=5)
        
        self.lbl_count = tk.Label(body, text="0 / 500", fg="gray")
        self.lbl_count.pack(anchor="e")
        self.txt_comentario.bind("<KeyRelease>", self._check_limit)

        # Botones (T-10.4)
        btn_frame = tk.Frame(body)
        btn_frame.pack(fill="x", pady=20)

        tk.Button(btn_frame, text="Guardar Borrador", bg="#f39c12", fg="white",
                  command=lambda: self._procesar("borrador")).pack(side="left", expand=True, fill="x", padx=5)
        
        tk.Button(btn_frame, text="Publicar Nota", bg="#27ae60", fg="white",
                  command=lambda: self._procesar("publicada")).pack(side="left", expand=True, fill="x", padx=5)

    def _check_limit(self, event):
        contenido = self.txt_comentario.get("1.0", "end-1c")
        count = len(contenido)
        self.lbl_count.config(text=f"{count} / 500", fg="red" if count > 500 else "gray")

    def _procesar(self, estado):
        nota_str = self.ent_nota.get()
        comentario = self.txt_comentario.get("1.0", "end-1c")

        # 1. Validación de Rango (T-10.3)
        try:
            # Quitamos espacios por si acaso
            nota = float(nota_str.strip())
            if not (0 <= nota <= 100): 
                raise ValueError()
        except ValueError:
            return messagebox.showerror("Error", "La nota debe ser un número entre 0 y 100")

        # 2. Llamada al Controlador
        from controllers.calificacion_controller import CalificacionController
        
        exito = CalificacionController.procesar_calificacion(
            self.id_entrega, nota, comentario, estado, self.nombre_estudiante
        )

        if exito:
            messagebox.showinfo("Éxito", f"Calificación {estado} guardada correctamente.")
            
            # 3. Refresco Automático: Llama a la función de la ventana anterior
            if self.callback_refresh:
                self.callback_refresh()
            
            # 4. Cierre Automático: La ventana se destruye tras guardar
            self.destroy()
    
    def confirmar_guardado(self, nota):
        # ... lógica de guardado exitoso ...
        
        messagebox.showinfo("Éxito", "Calificación guardada correctamente.")
        
        # Refrescamos la tabla de la ventana anterior
        if self.callback_refrescar:
            self.callback_refrescar() 
        
        # Cerramos la ventana de calificación automáticamente
        self.destroy()