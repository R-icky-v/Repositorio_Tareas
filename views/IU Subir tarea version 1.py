import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class frmEntregaTareaBase(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Entrega de tarea")
        self.geometry("560x680")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        self.archivo_seleccionado = ""

        # Colores alineados con tu estilo
        self.C_AZUL      = "#1A6FBF"
        self.C_AZUL_HOV  = "#155A9E"
        self.C_VERDE     = "#0F6E56"
        self.C_VERDE_HOV = "#0A5240"
        self.C_GRIS_BG   = "#F7F8FA"
        self.C_GRIS_BD   = "#D0D5DD"
        self.C_TEXTO     = "#1A1A2E"
        self.C_LABEL     = "#5A6478"
        self.C_HINT      = "#A0A8B8"
        self.C_ERROR     = "#D92D20"

        self._build_ui()

    def _label(self, parent, text, required=False):
        f = tk.Frame(parent, bg="white")
        f.pack(fill="x", pady=(14, 3))
        tk.Label(
            f, text=text, bg="white", fg=self.C_LABEL,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")
        if required:
            tk.Label(
                f, text=" *", bg="white", fg=self.C_ERROR,
                font=("Segoe UI", 9, "bold")
            ).pack(side="left")

    def _btn(self, parent, text, bg, fg, hover, command, width=14):
        btn = tk.Label(
            parent, text=text, bg=bg, fg=fg,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2", padx=18, pady=10,
            relief="flat", bd=0, width=width
        )
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=self.C_AZUL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="  ↑  ", bg="#155A9E", fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=(16, 0))

        tk.Label(
            header, text="Entrega de tarea", bg=self.C_AZUL, fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=10)

        tk.Label(
            header, text="US-10 · Estudiante", bg=self.C_AZUL, fg="#A8C8F0",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=18)

        # Body
        body = tk.Frame(self, bg="white", padx=28, pady=10)
        body.pack(fill="both", expand=True)

        # Tarjeta informativa de tarea
        card_info = tk.Frame(
            body, bg=self.C_GRIS_BG, highlightthickness=1,
            highlightbackground=self.C_GRIS_BD
        )
        card_info.pack(fill="x", pady=(6, 12))

        tk.Label(
            card_info, text="Práctica 1 — Circuitos en serie",
            bg=self.C_GRIS_BG, fg=self.C_TEXTO,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 4))

        tk.Label(
            card_info,
            text="Adjunta tu archivo antes de la fecha límite establecida por el docente.",
            bg=self.C_GRIS_BG, fg=self.C_LABEL,
            font=("Segoe UI", 9), wraplength=470, justify="left"
        ).pack(anchor="w", padx=14)

        tk.Label(
            card_info,
            text="Fecha límite: 11/04/2026 00:15",
            bg=self.C_GRIS_BG, fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=14, pady=(6, 12))

        # Estado general
        self.lbl_estado = tk.Label(
            body,
            text="Formulario listo para entregar.",
            bg="white", fg=self.C_HINT,
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_estado.pack(anchor="w", pady=(0, 8))

        # Área de carga
        self._label(body, "Archivo de entrega", required=True)

        drop = tk.Frame(
            body, bg=self.C_GRIS_BG, bd=0,
            highlightthickness=1, highlightbackground=self.C_GRIS_BD
        )
        drop.pack(fill="x", pady=(4, 0), ipady=14)

        tk.Label(
            drop, text="↑", bg=self.C_GRIS_BG, fg=self.C_AZUL,
            font=("Segoe UI", 22)
        ).pack()

        tk.Label(
            drop, text="Adjuntar archivo de entrega",
            bg=self.C_GRIS_BG, fg=self.C_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack()

        tk.Label(
            drop, text="PDF, DOCX, PNG, JPG — máx. 10 MB",
            bg=self.C_GRIS_BG, fg=self.C_HINT,
            font=("Segoe UI", 8)
        ).pack()

        btn_archivo = tk.Label(
            drop, text="Examinar archivo", bg="white", fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold"), cursor="hand2",
            padx=14, pady=6, relief="flat",
            highlightthickness=1, highlightbackground=self.C_AZUL
        )
        btn_archivo.pack(pady=(10, 0))
        btn_archivo.bind("<Button-1>", lambda e: self._examinar())
        btn_archivo.bind("<Enter>", lambda e: btn_archivo.configure(bg=self.C_AZUL, fg="white"))
        btn_archivo.bind("<Leave>", lambda e: btn_archivo.configure(bg="white", fg=self.C_AZUL))

        self.lbl_archivo = tk.Label(
            body, text="Ningún archivo seleccionado",
            bg="white", fg=self.C_HINT, font=("Segoe UI", 8)
        )
        self.lbl_archivo.pack(anchor="w", pady=(6, 0))

        # Progreso integrado en la pantalla
        self._label(body, "Progreso de carga")

        progress_box = tk.Frame(
            body, bg="white", highlightthickness=1,
            highlightbackground=self.C_GRIS_BD
        )
        progress_box.pack(fill="x", pady=(4, 0))

        inner = tk.Frame(progress_box, bg="white", padx=12, pady=12)
        inner.pack(fill="both", expand=True)

        self.progress = ttk.Progressbar(
            inner, orient="horizontal", mode="determinate", length=460
        )
        self.progress.pack(fill="x")

        self.lbl_progreso = tk.Label(
            inner, text="0%",
            bg="white", fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_progreso.pack(anchor="e", pady=(6, 0))

        # Footer
        sep = tk.Frame(self, bg=self.C_GRIS_BD, height=1)
        sep.pack(fill="x", side="bottom", before=body)

        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self._btn(
            footer, "Cancelar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
            self.destroy, width=10
        ).pack(side="left")

        self._btn(
            footer, "Enviar entrega", self.C_VERDE, "white", self.C_VERDE_HOV,
            self._enviar, width=14
        ).pack(side="right")

    def _examinar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[
                ("PDF", "*.pdf"),
                ("Word", "*.docx"),
                ("Imágenes", "*.png *.jpg *.jpeg"),
                ("Todos", "*.*")
            ]
        )

        if not ruta:
            return

        ext_validas = (".pdf", ".docx", ".png", ".jpg", ".jpeg")
        if not ruta.lower().endswith(ext_validas):
            messagebox.showwarning(
                "Formato no permitido",
                "Solo se permiten archivos PDF, DOCX, PNG o JPG."
            )
            return

        tam = os.path.getsize(ruta)
        if tam > 10 * 1024 * 1024:
            messagebox.showwarning(
                "Archivo muy pesado",
                "El archivo no debe superar los 10 MB."
            )
            return

        self.archivo_seleccionado = ruta
        nombre = os.path.basename(ruta)

        self.lbl_archivo.configure(
            text=f"Archivo seleccionado: {nombre}",
            fg=self.C_VERDE
        )
        self.lbl_estado.configure(
            text="Archivo listo para enviar.",
            fg=self.C_VERDE
        )
        self.progress["value"] = 0
        self.lbl_progreso.configure(text="0%")

    def _animar_progreso(self, valor=0):
        if valor > 100:
            self.lbl_estado.configure(
                text="Archivo enviado correctamente.",
                fg=self.C_VERDE
            )
            messagebox.showinfo(
                "Entrega enviada",
                "La tarea fue enviada correctamente."
            )
            return

        self.progress["value"] = valor
        self.lbl_progreso.configure(text=f"{valor}%")
        self.after(25, lambda: self._animar_progreso(valor + 4))

    def _enviar(self):
        if not self.archivo_seleccionado:
            messagebox.showwarning(
                "Archivo requerido",
                "Debes seleccionar un archivo antes de enviar la entrega."
            )
            self.lbl_estado.configure(
                text="Falta seleccionar un archivo.",
                fg=self.C_ERROR
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar entrega",
            "¿Deseas enviar tu archivo de entrega ahora?"
        )

        if not confirmar:
            self.lbl_estado.configure(
                text="La entrega fue cancelada por el usuario.",
                fg=self.C_HINT
            )
            return

        self.lbl_estado.configure(
            text="Subiendo archivo...",
            fg=self.C_AZUL
        )
        self._animar_progreso(0)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmEntregaTareaBase(root)
    root.mainloop()