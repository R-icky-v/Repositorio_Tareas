import tkinter as tk

class frmCalificaciones(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Mis calificaciones")
        self.geometry("600x620")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

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

        # Datos de ejemplo — vendrán del Controlador T-05.2
        self.calificaciones = [
            {"tarea": "Práctica 1 — Circuitos en serie",  "nota": 85, "comentario": "Buen trabajo, mejorar presentación.", "estado": "Calificada"},
            {"tarea": "Práctica 2 — Ley de Ohm",          "nota": 42, "comentario": "Faltan varios ejercicios resueltos.", "estado": "Calificada"},
            {"tarea": "Práctica 3 — Circuitos paralelos", "nota": 91, "comentario": "Excelente análisis.",                 "estado": "Calificada"},
            {"tarea": "Práctica 4 — Kirchhoff",           "nota": 0,  "comentario": "",                                   "estado": "Pendiente"},
            {"tarea": "Práctica 5 — Thevenin",            "nota": 58, "comentario": "Revisar el teorema de Thevenin.",    "estado": "Calificada"},
        ]

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
        # ── Header ──────────────────────────────────────────────
        header = tk.Frame(self, bg=self.C_AZUL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="  ★", bg="#155A9E", fg="white",
                 font=("Segoe UI", 15, "bold")).pack(side="left", padx=(12,0))
        tk.Label(header, text="  Mis calificaciones", bg=self.C_AZUL, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        tk.Label(header, text="T-05.1 · IU ", bg="#155A9E", fg="#A8C8F0",
                 font=("Segoe UI", 8, "bold"),
                 padx=8, pady=4).pack(side="right", padx=14, pady=16)

        # ── Tarjeta de promedio ──────────────────────────────────
        notas = [c["nota"] for c in self.calificaciones if c["estado"] == "Calificada"]
        promedio = round(sum(notas) / len(notas), 1) if notas else 0
        aprobado = promedio >= 51

        prom_frame = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        prom_frame.pack(fill="x")

        # Card promedio
        prom_card = tk.Frame(prom_frame, bg="#E6F1FB" if aprobado else "#FEF3F2",
                             highlightthickness=1,
                             highlightbackground=self.C_AZUL if aprobado else self.C_ROJO)
        prom_card.pack(side="left", ipadx=20, ipady=10, padx=(0,12))
        tk.Label(prom_card, text="Promedio actual",
                 bg="#E6F1FB" if aprobado else "#FEF3F2",
                 fg=self.C_LABEL, font=("Segoe UI", 9)).pack()
        tk.Label(prom_card, text=f"{promedio}/100",
                 bg="#E6F1FB" if aprobado else "#FEF3F2",
                 fg=self.C_AZUL if aprobado else self.C_ROJO,
                 font=("Segoe UI", 20, "bold")).pack()
        tk.Label(prom_card, text="Aprobado" if aprobado else "Reprobado",
                 bg="#E6F1FB" if aprobado else "#FEF3F2",
                 fg=self.C_VERDE if aprobado else self.C_ROJO,
                 font=("Segoe UI", 9, "bold")).pack()

        # Cards resumen
        resumen = tk.Frame(prom_frame, bg=self.C_GRIS_BG)
        resumen.pack(side="left", fill="x", expand=True)

        calificadas = sum(1 for c in self.calificaciones if c["estado"] == "Calificada")
        pendientes  = sum(1 for c in self.calificaciones if c["estado"] == "Pendiente")
        reprobadas  = sum(1 for c in self.calificaciones if c["nota"] < 51 and c["estado"] == "Calificada")

        for label, val, color in [
            ("Calificadas", calificadas, self.C_VERDE),
            ("Pendientes",  pendientes,  self.C_AMBAR),
            ("Por debajo\nde 51", reprobadas, self.C_ROJO),
        ]:
            card = tk.Frame(resumen, bg="white",
                            highlightthickness=1,
                            highlightbackground=self.C_GRIS_BD)
            card.pack(side="left", fill="x", expand=True,
                      padx=(0,8), ipady=8, ipadx=10)
            tk.Label(card, text=str(val), bg="white", fg=color,
                     font=("Segoe UI", 18, "bold")).pack()
            tk.Label(card, text=label, bg="white", fg=self.C_LABEL,
                     font=("Segoe UI", 8), justify="center").pack()

        # ── Separador ────────────────────────────────────────────
        tk.Frame(self, bg=self.C_GRIS_BD, height=1).pack(fill="x")

        # ── Lista de calificaciones ──────────────────────────────
        tk.Label(self, text="  Detalle de tareas", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold"), anchor="w").pack(fill="x", padx=24, pady=(12,6))

        lista = tk.Frame(self, bg="white", padx=24)
        lista.pack(fill="both", expand=True)

        for c in self.calificaciones:
            es_pendiente  = c["estado"] == "Pendiente"
            es_reprobada  = not es_pendiente and c["nota"] < 51
            es_aprobada   = not es_pendiente and c["nota"] >= 51

            if es_pendiente:
                card_bg  = self.C_GRIS_BG
                nota_col = self.C_HINT
                bd_col   = self.C_GRIS_BD
                nota_txt = "—"
                estado_bg  = "#FEF3F2"
                estado_fg  = self.C_AMBAR
                estado_txt = "● Pendiente"
            elif es_reprobada:
                card_bg  = "#FEF3F2"
                nota_col = self.C_ROJO
                bd_col   = self.C_ROJO
                nota_txt = str(c["nota"])
                estado_bg  = "#FEF3F2"
                estado_fg  = self.C_ROJO
                estado_txt = "✖ Reprobado"
            else:
                card_bg  = "white"
                nota_col = self.C_VERDE
                bd_col   = self.C_GRIS_BD
                nota_txt = str(c["nota"])
                estado_bg  = "#E1F5EE"
                estado_fg  = self.C_VERDE
                estado_txt = "✔ Aprobado"

            row = tk.Frame(lista, bg=card_bg,
                           highlightthickness=1,
                           highlightbackground=bd_col)
            row.pack(fill="x", pady=4, ipady=8)

            # Nota (izquierda)
            nota_box = tk.Frame(row, bg=card_bg, width=56)
            nota_box.pack(side="left", padx=12, fill="y")
            nota_box.pack_propagate(False)
            tk.Label(nota_box, text=nota_txt, bg=card_bg, fg=nota_col,
                     font=("Segoe UI", 18, "bold")).pack(expand=True)

            # Info (centro)
            info = tk.Frame(row, bg=card_bg)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=c["tarea"], bg=card_bg, fg=self.C_TEXTO,
                     font=("Segoe UI", 10, "bold"), anchor="w").pack(anchor="w")
            if c["comentario"]:
                tk.Label(info, text=f'"{c["comentario"]}"', bg=card_bg,
                         fg=self.C_LABEL, font=("Segoe UI", 9, "italic"),
                         wraplength=340, justify="left", anchor="w").pack(anchor="w", pady=(2,0))

            # Badge estado (derecha)
            tk.Label(row, text=estado_txt, bg=estado_bg, fg=estado_fg,
                     font=("Segoe UI", 8, "bold"),
                     padx=10, pady=4).pack(side="right", padx=12)

        # ── Footer ───────────────────────────────────────────────
        tk.Frame(self, bg=self.C_GRIS_BD, height=1).pack(fill="x", side="bottom")
        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")
        self._btn(footer, "Cerrar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
                  self.destroy, width=10).pack(side="left")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmCalificaciones(root)
    root.mainloop()