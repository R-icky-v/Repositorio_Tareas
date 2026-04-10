import tkinter as tk

class frmDetalleTarea(tk.Toplevel):
    def __init__(self, master=None, tarea=None):
        super().__init__(master)
        self.title("Detalle de tarea")
        self.geometry("560x580")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

       
        self.tarea = tarea or {
            "titulo":      "Práctica 1 — Circuitos en serie",
            "descripcion": (
                "Resolver los ejercicios del capítulo 3 del libro de texto.\n\n"
                "Analizar al menos 5 circuitos en serie aplicando la Ley de Ohm "
                "y las Leyes de Kirchhoff. Presentar cálculos paso a paso con "
                "el diagrama de cada circuito."
            ),
            "fecha_limite": "12/04/2026  23:59",
            "estado":       "Pendiente",   
        }

        
        self.C_AZUL     = "#1A6FBF"
        self.C_VERDE    = "#0F6E56"
        self.C_ROJO     = "#B42318"
        self.C_GRIS_BG  = "#F7F8FA"
        self.C_GRIS_BD  = "#D0D5DD"
        self.C_TEXTO    = "#1A1A2E"
        self.C_LABEL    = "#5A6478"
        self.C_HINT     = "#A0A8B8"

        self._build_ui()

    def _btn(self, parent, text, bg, fg, hover, command, width=12):
        btn = tk.Label(parent, text=text, bg=bg, fg=fg,
                       font=("Segoe UI", 10, "bold"),
                       cursor="hand2", padx=16, pady=10,
                       relief="flat", width=width)
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>",    lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>",    lambda e: btn.configure(bg=bg))
        return btn

    def _build_ui(self):
        t = self.tarea

        
        es_entregada = t["estado"].lower() == "entregada"
        estado_bg  = "#E1F5EE" if es_entregada else "#FEF3F2"
        estado_fg  = self.C_VERDE if es_entregada else self.C_ROJO
        estado_ico = "✔  " if es_entregada else "●  "

        
        header = tk.Frame(self, bg=self.C_AZUL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="  ≡", bg="#155A9E", fg="white",
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=(12,0))
        tk.Label(header, text="  Detalle de tarea", bg=self.C_AZUL, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Label(header, text="T-00.1 · IU ", bg="#155A9E", fg="#A8C8F0",
                 font=("Segoe UI", 8, "bold"),
                 padx=8, pady=4).pack(side="right", padx=14, pady=16)

       
        body = tk.Frame(self, bg="white", padx=28, pady=20)
        body.pack(fill="both", expand=True)

        # — Título —
        tk.Label(body, text="Título", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(body, text=t["titulo"], bg="white", fg=self.C_TEXTO,
                 font=("Segoe UI", 14, "bold"),
                 wraplength=490, justify="left").pack(anchor="w", pady=(2,16))

        tk.Frame(body, bg=self.C_GRIS_BD, height=1).pack(fill="x", pady=(0,16))

       
        tk.Label(body, text="Estado actual", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0,6))

        estado_card = tk.Frame(body, bg=estado_bg,
                               highlightthickness=1,
                               highlightbackground=estado_fg)
        estado_card.pack(fill="x", ipady=10)
        tk.Label(estado_card, text=estado_ico + t["estado"],
                 bg=estado_bg, fg=estado_fg,
                 font=("Segoe UI", 11, "bold"),
                 padx=14).pack(side="left")
        hint = "Aún no enviaste tu entrega." if not es_entregada else "Tu entrega fue registrada."
        tk.Label(estado_card, text=hint, bg=estado_bg, fg=estado_fg,
                 font=("Segoe UI", 9),
                 padx=4).pack(side="left")

       
        tk.Label(body, text="Fecha límite", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(18,6))

        fecha_card = tk.Frame(body, bg=self.C_GRIS_BG,
                              highlightthickness=1,
                              highlightbackground=self.C_GRIS_BD)
        fecha_card.pack(fill="x", ipady=10)
        tk.Label(fecha_card, text="  🗓", bg=self.C_GRIS_BG, fg=self.C_AZUL,
                 font=("Segoe UI", 12)).pack(side="left", padx=(10,6))
        tk.Label(fecha_card, text=t["fecha_limite"], bg=self.C_GRIS_BG,
                 fg=self.C_TEXTO, font=("Segoe UI", 11, "bold")).pack(side="left")

       
        tk.Label(body, text="Descripción", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(18,6))

        desc_box = tk.Frame(body, bg=self.C_GRIS_BG,
                            highlightthickness=1,
                            highlightbackground=self.C_GRIS_BD)
        desc_box.pack(fill="x")
        tk.Label(desc_box, text=t["descripcion"], bg=self.C_GRIS_BG,
                 fg=self.C_TEXTO, font=("Segoe UI", 10),
                 wraplength=480, justify="left",
                 padx=14, pady=12).pack(anchor="w")

       
        tk.Frame(self, bg=self.C_GRIS_BD, height=1).pack(fill="x", side="bottom")
        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self._btn(footer, "Cerrar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
                  self.destroy, width=10).pack(side="left")

        if not es_entregada:
            self._btn(footer, "Entregar tarea", self.C_VERDE, "white", "#0A5240",
                      lambda: print("→ Abrir frmSubirTarea (US-01)"),
                      width=14).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmDetalleTarea(root)
    root.mainloop()