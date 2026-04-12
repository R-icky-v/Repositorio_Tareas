import os
from tkinter import ttk, filedialog

class FilePicker(ttk.Frame):
    def __init__(self, parent, label_text="Adjuntar archivo:"):
        super().__init__(parent)
        
        self.ruta_archivo = ""
        
        # Etiqueta descriptiva
        self.lbl_instruccion = ttk.Label(self, text=label_text, font=('Arial', 9, 'bold'))
        self.lbl_instruccion.pack(side="top", anchor="w", pady=(5, 0))

        # Contenedor horizontal para el botón y el nombre del archivo
        self.contenedor = ttk.Frame(self)
        self.contenedor.pack(fill="x", pady=5)

        self.btn_seleccionar = ttk.Button(
            self.contenedor, 
            text="📁 Seleccionar", 
            command=self._abrir_explorador
        )
        self.btn_seleccionar.pack(side="left")

        self.lbl_nombre_archivo = ttk.Label(
            self.contenedor, 
            text="Ninguno seleccionado", 
            foreground="gray",
            wraplength=200
        )
        self.lbl_nombre_archivo.pack(side="left", padx=10)

    def _abrir_explorador(self):
        tipos = [
            ("Documentos PDF", "*.pdf"),
            ("Documentos Word", "*.docx"),
            ("Imágenes", "*.jpg *.png"),
            ("Todos los archivos", "*.*")
        ]
        
        ruta = filedialog.askopenfilename(title="Seleccionar material adjunto", filetypes=tipos)
        
        if ruta:
            self.ruta_archivo = ruta
            nombre = os.path.basename(ruta)
            self.lbl_nombre_archivo.config(text=nombre, foreground="blue")

    def get_file_name(self):
        """Retorna solo el nombre del archivo para la base de datos"""
        return os.path.basename(self.ruta_archivo) if self.ruta_archivo else ""

    def get_full_path(self):
        """Retorna la ruta completa por si necesitan mover el archivo después"""
        return self.ruta_archivo