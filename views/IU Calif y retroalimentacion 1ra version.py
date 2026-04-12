import tkinter as tk
from tkinter import ttk

class frmListaEntregasDocente(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lista de entregas")
        self.geometry("900x690")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        # Colores
        self.C_AZUL      = "#1A6FBF"
        self.C_AZUL_HOV  = "#155A9E"
        self.C_VERDE     = "#0F6E56"
        self.C_VERDE_TXT = "#067647"
        self.C_NARANJA   = "#F59E0B"
        self.C_NARANJA_TXT = "#B54708"
        self.C_ROJO      = "#D92D20"
        self.C_ROJO_TXT  = "#B42318"
        self.C_GRIS_BG   = "#F7F8FA"
        self.C_GRIS_BD   = "#D0D5DD"
        self.C_TEXTO     = "#1A1A2E"
        self.C_LABEL     = "#5A6478"
        self.C_HINT      = "#A0A8B8"
        self.C_BLANCO    = "#FFFFFF"

        self.datos_entregas = [
            ("Juan Pérez", "10/04/2026 22:15", "Entregado"),
            ("María López", "—", "Pendiente"),
            ("Carlos Rojas", "12/04/2026 01:10", "Atrasado"),
            ("Ana Torres", "10/04/2026 19:40", "Entregado"),
            ("Luis Fernández", "—", "Pendiente"),
            ("Camila Vargas", "09/04/2026 18:20", "Entregado"),
            ("Diego Romero", "11/04/2026 02:05", "Atrasado"),
        ]

        self._configurar_estilos()
        self._build_ui()
        self._cargar_datos()

    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground=self.C_TEXTO,
            fieldbackground="white",
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#F9FAFB",
            foreground=self.C_TEXTO,
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10, "bold"),
            padding=(8, 10)
        )

        style.map(
            "Treeview",
            background=[("selected", "#E6F1FB")],
            foreground=[("selected", self.C_TEXTO)]
        )

    def _label_chip(self, parent, titulo, valor, bg, fg):
        card = tk.Frame(parent, bg=bg, bd=0, highlightthickness=1, highlightbackground=bg)
        card.pack(side="left", padx=(0, 10), ipadx=8, ipady=4)

        tk.Label(
            card, text=titulo,
            bg=bg, fg=fg,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=10, pady=(6, 0))

        tk.Label(
            card, text=str(valor),
            bg=bg, fg=fg,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=10, pady=(0, 6))

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=self.C_AZUL, height=58)
        header.pack(fill="x")
        header.pack_propagate(False)

        icono = tk.Label(
            header,
            text="📋",
            bg="#155A9E",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            width=3
        )
        icono.pack(side="left", padx=(16, 0), pady=8)

        tk.Label(
            header,
            text="Lista de entregas",
            bg=self.C_AZUL,
            fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=12)

        tk.Label(
            header,
            text="US-10 · Docente",
            bg=self.C_AZUL,
            fg="#A8C8F0",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=18)

        # Body
        body = tk.Frame(self, bg="white", padx=20, pady=18)
        body.pack(fill="both", expand=True)

        # Tarjeta principal
        card_info = tk.Frame(
            body, bg=self.C_GRIS_BG,
            highlightthickness=1, highlightbackground=self.C_GRIS_BD
        )
        card_info.pack(fill="x", pady=(0, 14))

        tk.Label(
            card_info,
            text="Práctica 1 — Circuitos en serie",
            bg=self.C_GRIS_BG,
            fg=self.C_TEXTO,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=16, pady=(14, 4))

        tk.Label(
            card_info,
            text="Listado general de entregas registradas por los estudiantes para esta tarea.",
            bg=self.C_GRIS_BG,
            fg=self.C_LABEL,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16)

        tk.Label(
            card_info,
            text="Selecciona una fila para revisar o calificar la entrega.",
            bg=self.C_GRIS_BG,
            fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(6, 14))

        # Resumen
        resumen = tk.Frame(body, bg="white")
        resumen.pack(fill="x", pady=(0, 14))

        total = len(self.datos_entregas)
        entregados = sum(1 for x in self.datos_entregas if x[2] == "Entregado")
        pendientes = sum(1 for x in self.datos_entregas if x[2] == "Pendiente")
        atrasados = sum(1 for x in self.datos_entregas if x[2] == "Atrasado")

        self._label_chip(resumen, "Total", total, "#EEF4FF", "#3538CD")
        self._label_chip(resumen, "Entregados", entregados, "#ECFDF3", self.C_VERDE_TXT)
        self._label_chip(resumen, "Pendientes", pendientes, "#FFFAEB", self.C_NARANJA_TXT)
        self._label_chip(resumen, "Atrasados", atrasados, "#FEF3F2", self.C_ROJO_TXT)

        # Barra superior de tabla
        barra_tabla = tk.Frame(body, bg="white")
        barra_tabla.pack(fill="x", pady=(0, 8))

        tk.Label(
            barra_tabla,
            text="Entregas registradas",
            bg="white",
            fg=self.C_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(side="left")

        buscador_wrap = tk.Frame(
            barra_tabla,
            bg=self.C_GRIS_BD,
            bd=0
        )
        buscador_wrap.pack(side="right")

        buscador_inner = tk.Frame(buscador_wrap, bg="white")
        buscador_inner.pack(padx=1, pady=1)

        tk.Label(
            buscador_inner,
            text="🔎",
            bg="white",
            fg=self.C_HINT,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(8, 4))

        self.txt_buscar = tk.Entry(
            buscador_inner,
            bd=0,
            relief="flat",
            font=("Segoe UI", 9),
            fg=self.C_HINT,
            width=24
        )
        self.txt_buscar.pack(side="left", padx=(0, 8), pady=7)
        self.txt_buscar.insert(0, "Buscar estudiante...")
        self.txt_buscar.bind("<FocusIn>", self._focus_busqueda_in)
        self.txt_buscar.bind("<FocusOut>", self._focus_busqueda_out)
        self.txt_buscar.bind("<KeyRelease>", self._filtrar_tabla)

        # Contenedor tabla
        frame_tabla = tk.Frame(
            body, bg="white",
            highlightthickness=1,
            highlightbackground=self.C_GRIS_BD
        )
        frame_tabla.pack(fill="both", expand=True)

        tabla_inner = tk.Frame(frame_tabla, bg="white")
        tabla_inner.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("estudiante", "fecha", "estado")

        self.tree = ttk.Treeview(
            tabla_inner,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("estudiante", text="Estudiante")
        self.tree.heading("fecha", text="Fecha de entrega")
        self.tree.heading("estado", text="Estado de entrega")

        self.tree.column("estudiante", width=320, anchor="w")
        self.tree.column("fecha", width=220, anchor="center")
        self.tree.column("estado", width=180, anchor="center")

        scroll = ttk.Scrollbar(tabla_inner, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Footer
        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self.lbl_footer = tk.Label(
            footer,
            text="Selecciona un estudiante para continuar con la revisión de su entrega.",
            bg=self.C_GRIS_BG,
            fg=self.C_HINT,
            font=("Segoe UI", 9)
        )
        self.lbl_footer.pack(anchor="w")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _focus_busqueda_in(self, event=None):
        if self.txt_buscar.get() == "Buscar estudiante...":
            self.txt_buscar.delete(0, "end")
            self.txt_buscar.config(fg=self.C_TEXTO)

    def _focus_busqueda_out(self, event=None):
        if not self.txt_buscar.get().strip():
            self.txt_buscar.insert(0, "Buscar estudiante...")
            self.txt_buscar.config(fg=self.C_HINT)

    def _estado_tag(self, estado):
        if estado == "Entregado":
            return "ok"
        if estado == "Pendiente":
            return "pend"
        return "late"

    def _cargar_datos(self, filtro=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        filtro = filtro.strip().lower()

        for fila in self.datos_entregas:
            estudiante, fecha, estado = fila
            if filtro and filtro not in estudiante.lower():
                continue

            iid = self.tree.insert("", "end", values=fila, tags=(self._estado_tag(estado),))

            if estado == "Entregado":
                self.tree.item(iid, tags=("ok",))
            elif estado == "Pendiente":
                self.tree.item(iid, tags=("pend",))
            else:
                self.tree.item(iid, tags=("late",))

        self.tree.tag_configure("ok", foreground=self.C_VERDE_TXT)
        self.tree.tag_configure("pend", foreground=self.C_NARANJA_TXT)
        self.tree.tag_configure("late", foreground=self.C_ROJO_TXT)

    def _filtrar_tabla(self, event=None):
        texto = self.txt_buscar.get().strip()
        if texto == "Buscar estudiante...":
            texto = ""
        self._cargar_datos(texto)

    def _on_select(self, event=None):
        seleccionado = self.tree.selection()
        if not seleccionado:
            return

        valores = self.tree.item(seleccionado[0], "values")
        estudiante = valores[0]
        estado = valores[2]

        self.lbl_footer.configure(
            text=f"Estudiante seleccionado: {estudiante} | Estado actual: {estado}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmListaEntregasDocente(root)
    root.mainloop()