import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import time

class frmEntregaTarea(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Entrega de tarea")
        self.geometry("520x600")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        self.archivo = None

        # 🎨 Colores (misma línea, pero diferenciados)
        self.C_PRIMARIO = "#7A5AF8"      # morado elegante
        self.C_PRIMARIO_HOV = "#6941C6"
        self.C_FONDO = "#F9FAFB"
        self.C_BORDE = "#D0D5DD"
        self.C_TEXTO = "#101828"
        self.C_HINT = "#98A2B3"
        self.C_EXITO = "#12B76A"
        self.C_ERROR = "#F04438"

        self._build_ui()

    def _build_ui(self):
        # ── Header ─────────────────────────────
        header = tk.Frame(self, bg=self.C_PRIMARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="📤 Entrega de tarea",
                 bg=self.C_PRIMARIO, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=20)

        # ── Body ───────────────────────────────
        body = tk.Frame(self, bg="white", padx=30, pady=20)
        body.pack(fill="both", expand=True)

        tk.Label(body, text="Subir archivo",
                 bg="white", fg=self.C_TEXTO,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")

        tk.Label(body, text="Adjunta tu tarea en formato PDF, DOC o imagen",
                 bg="white", fg=self.C_HINT,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 10))

        # ── Zona de carga ──────────────────────
        drop = tk.Frame(body, bg=self.C_FONDO,
                        highlightbackground=self.C_BORDE,
                        highlightthickness=1)
        drop.pack(fill="x", ipady=25)

        tk.Label(drop, text="⬆",
                 bg=self.C_FONDO, fg=self.C_PRIMARIO,
                 font=("Segoe UI", 22)).pack()

        tk.Label(drop, text="Arrastra o selecciona tu archivo",
                 bg=self.C_FONDO, fg=self.C_TEXTO,
                 font=("Segoe UI", 10, "bold")).pack()

        btn = tk.Label(drop, text="Seleccionar archivo",
                       bg="white", fg=self.C_PRIMARIO,
                       font=("Segoe UI", 9, "bold"),
                       padx=12, pady=6, cursor="hand2",
                       highlightbackground=self.C_PRIMARIO,
                       highlightthickness=1)
        btn.pack(pady=10)

        btn.bind("<Button-1>", lambda e: self._seleccionar())
        btn.bind("<Enter>", lambda e: btn.config(bg=self.C_PRIMARIO, fg="white"))
        btn.bind("<Leave>", lambda e: btn.config(bg="white", fg=self.C_PRIMARIO))

        self.lbl_archivo = tk.Label(body, text="Ningún archivo seleccionado",
                                    bg="white", fg=self.C_HINT,
                                    font=("Segoe UI", 9))
        self.lbl_archivo.pack(anchor="w", pady=(10, 0))

        # ── Barra de progreso ──────────────────
        tk.Label(body, text="Progreso de carga",
                 bg="white", fg=self.C_TEXTO,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))

        self.progress = ttk.Progressbar(body, orient="horizontal",
                                        length=400, mode="determinate")
        self.progress.pack(fill="x")

        self.lbl_progreso = tk.Label(body, text="0%",
                                      bg="white", fg=self.C_HINT,
                                      font=("Segoe UI", 9))
        self.lbl_progreso.pack(anchor="e")

        # ── Estado ─────────────────────────────
        self.lbl_estado = tk.Label(body, text="Esperando archivo...",
                                   bg="white", fg=self.C_HINT,
                                   font=("Segoe UI", 9, "italic"))
        self.lbl_estado.pack(anchor="w", pady=(10, 0))

        # ── Botón enviar ───────────────────────
        enviar = tk.Label(self, text="Enviar tarea",
                          bg=self.C_PRIMARIO, fg="white",
                          font=("Segoe UI", 11, "bold"),
                          padx=20, pady=12, cursor="hand2")
        enviar.pack(side="bottom", fill="x", padx=20, pady=15)

        enviar.bind("<Button-1>", lambda e: self._enviar())
        enviar.bind("<Enter>", lambda e: enviar.config(bg=self.C_PRIMARIO_HOV))
        enviar.bind("<Leave>", lambda e: enviar.config(bg=self.C_PRIMARIO))

    # ── Funciones ─────────────────────────────
    def _seleccionar(self):
        ruta = filedialog.askopenfilename(
            filetypes=[("Archivos", "*.pdf *.docx *.png *.jpg")]
        )
        if ruta:
            self.archivo = ruta
            nombre = os.path.basename(ruta)
            self.lbl_archivo.config(text=f"Archivo: {nombre}", fg=self.C_EXITO)
            self.lbl_estado.config(text="Archivo listo para enviar.", fg=self.C_EXITO)

    def _simular_carga(self):
        self.progress["value"] = 0
        for i in range(101):
            time.sleep(0.02)
            self.progress["value"] = i
            self.lbl_progreso.config(text=f"{i}%")
            self.update_idletasks()

    def _enviar(self):
        if not self.archivo:
            messagebox.showwarning("Aviso", "Selecciona un archivo primero.")
            self.lbl_estado.config(text="Falta archivo.", fg=self.C_ERROR)
            return

        self.lbl_estado.config(text="Subiendo archivo...", fg=self.C_PRIMARIO)

        threading.Thread(target=self._simular_carga).start()

        messagebox.showinfo("Éxito", "Tarea enviada correctamente.")
        self.lbl_estado.config(text="Entrega completada.", fg=self.C_EXITO)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmEntregaTarea(root)
    root.mainloop()