import tkinter as tk
from tkinter import messagebox, filedialog
import os

class frmEditarEntrega(tk.Toplevel):
    def __init__(self, master=None, entrega=None):
        super().__init__(master)
        self.title("Editar entrega")
        self.geometry("560x580")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        # Datos de ejemplo — vendrán del Controlador T-02.3
        self.entrega = entrega or {
            "tarea":        "Práctica 1 — Circuitos en serie",
            "archivo":      "practica1_franz.pdf",
            "fecha_envio":  "08/04/2026  14:32",
            "fecha_limite": "12/04/2026  23:59",
            "plazo_vencido": False,   # Cambiá a True para ver la UI bloqueada
        }

        # Paleta
        self.C_AZUL    = "#1A6FBF"
        self.C_VERDE   = "#0F6E56"
        self.C_ROJO    = "#B42318"
        self.C_AMBAR   = "#B54708"
        self.C_GRIS_BG = "#F7F8FA"
        self.C_GRIS_BD = "#D0D5DD"
        self.C_TEXTO   = "#1A1A2E"
        self.C_LABEL   = "#5A6478"
        self.C_HINT    = "#A0A8B8"

        self.nuevo_archivo = ""
        self._build_ui()

    def _btn(self, parent, text, bg, fg, hover, command, width=12, disabled=False):
        color_bg = "#E2E5EA" if disabled else bg
        color_fg = self.C_HINT if disabled else fg
        btn = tk.Label(parent, text=text, bg=color_bg, fg=color_fg,
                       font=("Segoe UI", 10, "bold"),
                       cursor="arrow" if disabled else "hand2",
                       padx=16, pady=10, relief="flat", width=width)
        if not disabled:
            btn.bind("<Button-1>", lambda e: command())
            btn.bind("<Enter>",    lambda e: btn.configure(bg=hover))
            btn.bind("<Leave>",    lambda e: btn.configure(bg=bg))
        return btn

    def _build_ui(self):
        e = self.entrega
        vencido = e["plazo_vencido"]

        # ── Header ──────────────────────────────────────────────
        header = tk.Frame(self, bg=self.C_AZUL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="  ✎", bg="#155A9E", fg="white",
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=(12,0))
        tk.Label(header, text="  Editar entrega", bg=self.C_AZUL, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Label(header, text="T-02.1 · IU ", bg="#155A9E", fg="#A8C8F0",
                 font=("Segoe UI", 8, "bold"),
                 padx=8, pady=4).pack(side="right", padx=14, pady=16)

        # ── Aviso si plazo vencido ───────────────────────────────
        if vencido:
            aviso = tk.Frame(self, bg="#FEF3F2",
                             highlightthickness=1,
                             highlightbackground=self.C_ROJO)
            aviso.pack(fill="x", padx=24, pady=(14,0))
            tk.Label(aviso, text="✖  El plazo de entrega ha vencido — no se puede editar ni anular.",
                     bg="#FEF3F2", fg=self.C_ROJO,
                     font=("Segoe UI", 9, "bold"),
                     padx=14, pady=10).pack(anchor="w")

        # ── Cuerpo ───────────────────────────────────────────────
        body = tk.Frame(self, bg="white", padx=28, pady=16)
        body.pack(fill="both", expand=True)

        # — Tarea —
        tk.Label(body, text="Tarea", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(body, text=e["tarea"], bg="white", fg=self.C_TEXTO,
                 font=("Segoe UI", 13, "bold"),
                 wraplength=490, justify="left").pack(anchor="w", pady=(2,14))

        tk.Frame(body, bg=self.C_GRIS_BD, height=1).pack(fill="x", pady=(0,14))

        # — Archivo actual —
        tk.Label(body, text="Archivo entregado actualmente", bg="white",
                 fg=self.C_LABEL, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0,6))

        arch_card = tk.Frame(body, bg="#E6F1FB",
                             highlightthickness=1,
                             highlightbackground="#B5D4F4")
        arch_card.pack(fill="x", ipady=10)
        tk.Label(arch_card, text="  📄", bg="#E6F1FB", fg=self.C_AZUL,
                 font=("Segoe UI", 12)).pack(side="left", padx=(10,4))
        tk.Label(arch_card, text=e["archivo"], bg="#E6F1FB", fg=self.C_AZUL,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(arch_card, text=f"Enviado: {e['fecha_envio']}", bg="#E6F1FB",
                 fg=self.C_LABEL, font=("Segoe UI", 8)).pack(side="right", padx=14)

        # — Fecha límite —
        tk.Label(body, text="Fecha límite", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(14,6))

        fecha_card = tk.Frame(body, bg="#FEF3F2" if vencido else self.C_GRIS_BG,
                              highlightthickness=1,
                              highlightbackground=self.C_ROJO if vencido else self.C_GRIS_BD)
        fecha_card.pack(fill="x", ipady=8)
        ico = "✖" if vencido else "🗓"
        col = self.C_ROJO if vencido else self.C_TEXTO
        tk.Label(fecha_card, text=f"  {ico}  {e['fecha_limite']}",
                 bg="#FEF3F2" if vencido else self.C_GRIS_BG,
                 fg=col, font=("Segoe UI", 10, "bold"),
                 padx=10).pack(side="left")
        if vencido:
            tk.Label(fecha_card, text="Plazo vencido",
                     bg="#FEF3F2", fg=self.C_ROJO,
                     font=("Segoe UI", 8, "bold"),
                     padx=10).pack(side="right", padx=8)

        # — Reemplazar archivo —
        tk.Label(body, text="Reemplazar archivo", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(14,6))

        drop = tk.Frame(body, bg="#E2E5EA" if vencido else self.C_GRIS_BG,
                        highlightthickness=1,
                        highlightbackground=self.C_GRIS_BD)
        drop.pack(fill="x", ipady=10)
        tk.Label(drop, text="↑", bg="#E2E5EA" if vencido else self.C_GRIS_BG,
                 fg=self.C_HINT if vencido else self.C_AZUL,
                 font=("Segoe UI", 16)).pack()
        tk.Label(drop, text="Seleccioná el nuevo archivo",
                 bg="#E2E5EA" if vencido else self.C_GRIS_BG,
                 fg=self.C_HINT, font=("Segoe UI", 9)).pack()

        btn_exam = tk.Label(drop, text="Examinar archivo",
                            bg="#E2E5EA" if vencido else "white",
                            fg=self.C_HINT if vencido else self.C_AZUL,
                            font=("Segoe UI", 9, "bold"),
                            cursor="arrow" if vencido else "hand2",
                            padx=14, pady=6, relief="flat",
                            highlightthickness=1,
                            highlightbackground=self.C_GRIS_BD)
        btn_exam.pack(pady=(8,0))
        if not vencido:
            btn_exam.bind("<Button-1>", lambda e: self._examinar())
            btn_exam.bind("<Enter>", lambda e: btn_exam.configure(bg=self.C_AZUL, fg="white"))
            btn_exam.bind("<Leave>", lambda e: btn_exam.configure(bg="white", fg=self.C_AZUL))

        self.lbl_nuevo = tk.Label(body, text="Ningún archivo seleccionado",
                                  bg="white", fg=self.C_HINT, font=("Segoe UI", 8))
        self.lbl_nuevo.pack(anchor="w", pady=(4,0))

       
        tk.Frame(self, bg=self.C_GRIS_BD, height=1).pack(fill="x", side="bottom")
        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self._btn(footer, "Cerrar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
                  self.destroy, width=10).pack(side="left")

        self._btn(footer, "Anular entrega", "#FEF3F2", self.C_ROJO, "#FCDCDC",
                  self._anular, width=13,
                  disabled=vencido).pack(side="right", padx=(10,0))

        self._btn(footer, "Guardar cambios", self.C_VERDE, "white", "#0A5240",
                  self._guardar, width=14,
                  disabled=vencido).pack(side="right")

    
    def _examinar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar nuevo archivo",
            filetypes=[("PDF","*.pdf"),("Word","*.docx"),
                       ("Imágenes","*.png *.jpg"),("Todos","*.*")]
        )
        if ruta:
            self.nuevo_archivo = ruta
            nombre = os.path.basename(ruta)
            self.lbl_nuevo.configure(text=f"Nuevo archivo: {nombre}", fg=self.C_VERDE)

    def _guardar(self):
        if not self.nuevo_archivo:
            messagebox.showwarning("Sin archivo", "Seleccioná un nuevo archivo primero.")
            return
        messagebox.showinfo("Entrega actualizada", "Tu entrega fue reemplazada correctamente.")
        self.destroy()

    def _anular(self):
        confirmar = messagebox.askyesno("Anular entrega",
                                        "¿Estás seguro que querés anular tu entrega?\nEsta acción no se puede deshacer.")
        if confirmar:
            messagebox.showinfo("Entrega anulada", "Tu entrega fue anulada correctamente.")
            self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # Cambiá "plazo_vencido" a True para ver la UI bloqueada
    app = frmEditarEntrega(root)
    root.mainloop()