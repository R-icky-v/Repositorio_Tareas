import tkinter as tk
from tkinter import ttk, messagebox


class frmCalificarEntrega(tk.Toplevel):
    def __init__(self, master=None, entrega=None):
        super().__init__(master)
        self.title("Calificar entrega")
        self.geometry("620x760")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        self.entrega = entrega or {
            "estudiante": "Juan Pérez",
            "fecha": "10/04/2026 22:15",
            "estado": "Entregado",
            "archivo": "practica1_juan_perez.pdf",
            "nota": "",
            "comentario": ""
        }

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
        self.C_NARANJA   = "#F59E0B"

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

    def _entry(self, parent, placeholder="", width=None):
        frame = tk.Frame(parent, bg=self.C_GRIS_BD, bd=0)
        inner = tk.Frame(frame, bg="white", bd=0)
        inner.pack(padx=1, pady=1, fill="both", expand=True)

        widget = tk.Entry(
            inner,
            font=("Segoe UI", 10),
            bd=0,
            relief="flat",
            bg="white",
            fg=self.C_HINT,
            insertbackground=self.C_AZUL,
            width=width if width else 20
        )
        widget.insert(0, placeholder)
        widget._placeholder = placeholder
        widget._is_ph = True

        def on_focus_in(e, w=widget):
            if w._is_ph:
                w.delete(0, "end")
                w.configure(fg=self.C_TEXTO)
                w._is_ph = False

        def on_focus_out(e, w=widget):
            if not w.get().strip():
                w.insert(0, placeholder)
                w.configure(fg=self.C_HINT)
                w._is_ph = True

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)
        widget.pack(fill="both", expand=True, padx=10, pady=8)

        return frame, widget

    def _textarea(self, parent, placeholder="", height=7):
        frame = tk.Frame(parent, bg=self.C_GRIS_BD, bd=0)
        inner = tk.Frame(frame, bg="white", bd=0)
        inner.pack(padx=1, pady=1, fill="both", expand=True)

        widget = tk.Text(
            inner,
            font=("Segoe UI", 10),
            height=height,
            bd=0,
            relief="flat",
            bg="white",
            fg=self.C_HINT,
            insertbackground=self.C_AZUL,
            wrap="word",
            padx=10,
            pady=8
        )
        widget.insert("1.0", placeholder)
        widget._placeholder = placeholder
        widget._is_ph = True

        def on_focus_in(e):
            if widget._is_ph:
                widget.delete("1.0", "end")
                widget.configure(fg=self.C_TEXTO)
                widget._is_ph = False

        def on_focus_out(e):
            if not widget.get("1.0", "end").strip():
                widget.insert("1.0", placeholder)
                widget.configure(fg=self.C_HINT)
                widget._is_ph = True

        widget.bind("<FocusIn>", on_focus_in)
        widget.bind("<FocusOut>", on_focus_out)
        widget.pack(fill="both", expand=True)

        return frame, widget

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
        header = tk.Frame(self, bg=self.C_AZUL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="  ✓  ", bg="#155A9E", fg="white",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=(16, 0))

        tk.Label(
            header, text="Panel de calificación", bg=self.C_AZUL, fg="white",
            font=("Segoe UI", 13, "bold")
        ).pack(side="left", padx=10)

        tk.Label(
            header, text="US-10 · Docente", bg=self.C_AZUL, fg="#A8C8F0",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=18)

        body = tk.Frame(self, bg="white", padx=28, pady=12)
        body.pack(fill="both", expand=True)

        card = tk.Frame(
            body, bg=self.C_GRIS_BG,
            highlightthickness=1, highlightbackground=self.C_GRIS_BD
        )
        card.pack(fill="x", pady=(0, 14))

        tk.Label(
            card,
            text="Práctica 1 — Circuitos en serie",
            bg=self.C_GRIS_BG,
            fg=self.C_TEXTO,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", padx=16, pady=(14, 4))

        tk.Label(
            card,
            text=f"Estudiante: {self.entrega['estudiante']}",
            bg=self.C_GRIS_BG,
            fg=self.C_LABEL,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16, pady=(0, 2))

        tk.Label(
            card,
            text=f"Fecha de entrega: {self.entrega['fecha']}",
            bg=self.C_GRIS_BG,
            fg=self.C_LABEL,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16, pady=(0, 2))

        color_estado = self.C_VERDE if self.entrega["estado"] == "Entregado" else self.C_NARANJA
        tk.Label(
            card,
            text=f"Estado: {self.entrega['estado']}",
            bg=self.C_GRIS_BG,
            fg=color_estado,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(0, 2))

        tk.Label(
            card,
            text=f"Archivo entregado: {self.entrega['archivo']}",
            bg=self.C_GRIS_BG,
            fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(4, 14))

        self.lbl_estado = tk.Label(
            body,
            text="Complete la calificación y los comentarios privados del docente.",
            bg="white",
            fg=self.C_HINT,
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_estado.pack(anchor="w", pady=(0, 10))

        self._label(body, "Calificación (0 - 100)", required=True)
        ef_nota, self.txtNota = self._entry(body, "Ej: 85", width=12)
        ef_nota.pack(fill="x", ipady=3)

        fila = tk.Frame(body, bg="white")
        fila.pack(fill="x", pady=(14, 3))

        tk.Label(
            fila, text="Comentarios privados", bg="white", fg=self.C_LABEL,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            fila, text=" (máx. 500 caracteres)", bg="white", fg=self.C_HINT,
            font=("Segoe UI", 8)
        ).pack(side="left")

        ef_com, self.txtComentario = self._textarea(
            body,
            "Escribe observaciones internas sobre esta entrega...",
            height=9
        )
        ef_com.pack(fill="x")

        self.lbl_contador = tk.Label(
            body,
            text="0 / 500 caracteres",
            bg="white",
            fg=self.C_HINT,
            font=("Segoe UI", 8)
        )
        self.lbl_contador.pack(anchor="e", pady=(6, 0))

        self.txtComentario.bind("<KeyRelease>", self._actualizar_contador)

        acciones = tk.Frame(
            body, bg=self.C_GRIS_BG,
            highlightthickness=1, highlightbackground=self.C_GRIS_BD
        )
        acciones.pack(fill="x", pady=(18, 0))

        tk.Label(
            acciones,
            text="Acciones de calificación",
            bg=self.C_GRIS_BG,
            fg=self.C_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=14, pady=(12, 4))

        tk.Label(
            acciones,
            text="Guardar conserva los cambios como borrador. Publicar deja la calificación lista para mostrarse.",
            bg=self.C_GRIS_BG,
            fg=self.C_LABEL,
            font=("Segoe UI", 8),
            wraplength=520,
            justify="left"
        ).pack(anchor="w", padx=14, pady=(0, 12))

        self.lbl_confirmacion = tk.Label(
            body,
            text="",
            bg="white",
            fg=self.C_VERDE,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_confirmacion.pack(anchor="w", pady=(14, 0))

        sep = tk.Frame(self, bg=self.C_GRIS_BD, height=1)
        sep.pack(fill="x", side="bottom", before=body)

        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self._btn(
            footer, "Cancelar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
            self.destroy, width=10
        ).pack(side="left")

        self._btn(
            footer, "Guardar", "#E6F1FB", self.C_AZUL, "#C8DFF5",
            self._guardar, width=12
        ).pack(side="left", padx=10)

        self._btn(
            footer, "Publicar", self.C_VERDE, "white", self.C_VERDE_HOV,
            self._publicar, width=12
        ).pack(side="right")

    def _get_entry_text(self, widget):
        return "" if getattr(widget, "_is_ph", False) else widget.get().strip()

    def _get_textarea_text(self, widget):
        val = widget.get("1.0", "end").strip()
        return "" if getattr(widget, "_is_ph", False) else val

    def _actualizar_contador(self, event=None):
        texto = self._get_textarea_text(self.txtComentario)
        cantidad = len(texto)

        if cantidad > 500:
            actual = self.txtComentario.get("1.0", "end-1c")
            self.txtComentario.delete("1.0", "end")
            self.txtComentario.insert("1.0", actual[:500])
            cantidad = 500

        color = self.C_ERROR if cantidad >= 500 else self.C_HINT
        self.lbl_contador.configure(text=f"{cantidad} / 500 caracteres", fg=color)

    def _validar(self):
        nota_txt = self._get_entry_text(self.txtNota)
        comentario = self._get_textarea_text(self.txtComentario)

        if not nota_txt:
            messagebox.showwarning("Campo requerido", "Debes ingresar una calificación.")
            self.lbl_estado.configure(text="Falta ingresar la calificación.", fg=self.C_ERROR)
            self.txtNota.focus()
            return None

        try:
            nota = float(nota_txt)
        except ValueError:
            messagebox.showwarning("Valor inválido", "La calificación debe ser numérica.")
            self.lbl_estado.configure(text="La calificación ingresada no es válida.", fg=self.C_ERROR)
            self.txtNota.focus()
            return None

        if nota < 0 or nota > 100:
            messagebox.showwarning("Rango inválido", "La calificación debe estar entre 0 y 100.")
            self.lbl_estado.configure(text="La calificación está fuera del rango permitido.", fg=self.C_ERROR)
            self.txtNota.focus()
            return None

        if len(comentario) > 500:
            messagebox.showwarning("Límite excedido", "El comentario no puede superar los 500 caracteres.")
            self.lbl_estado.configure(text="El comentario excede el límite permitido.", fg=self.C_ERROR)
            return None

        return {"nota": nota, "comentario": comentario}

    def _guardar(self):
        datos = self._validar()
        if not datos:
            return

        self.lbl_estado.configure(
            text="Calificación guardada como borrador.",
            fg=self.C_AZUL
        )
        self.lbl_confirmacion.configure(
            text=f"✔ Borrador guardado: {datos['nota']:.0f}/100"
        )

        messagebox.showinfo(
            "Borrador guardado",
            "La calificación fue guardada correctamente como borrador."
        )

    def _publicar(self):
        datos = self._validar()
        if not datos:
            return

        confirmar = messagebox.askyesno(
            "Confirmar publicación",
            f"¿Deseas publicar la calificación de {datos['nota']:.0f}/100 para {self.entrega['estudiante']}?"
        )

        if not confirmar:
            self.lbl_estado.configure(
                text="La publicación fue cancelada.",
                fg=self.C_HINT
            )
            self.lbl_confirmacion.configure(text="")
            return

        self.lbl_estado.configure(
            text="Calificación publicada correctamente.",
            fg=self.C_VERDE
        )
        self.lbl_confirmacion.configure(
            text=f"✔ Calificación publicada: {datos['nota']:.0f}/100 para {self.entrega['estudiante']}"
        )

        messagebox.showinfo(
            "Calificación publicada",
            f"La calificación de {self.entrega['estudiante']} fue publicada correctamente."
        )


class frmListaEntregasDocente(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lista de entregas")
        self.geometry("900x690")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

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
            {"estudiante": "Juan Pérez", "fecha": "10/04/2026 22:15", "estado": "Entregado", "archivo": "practica1_juan_perez.pdf"},
            {"estudiante": "María López", "fecha": "—", "estado": "Pendiente", "archivo": "Sin archivo"},
            {"estudiante": "Carlos Rojas", "fecha": "12/04/2026 01:10", "estado": "Atrasado", "archivo": "carlos_rojas_redes.pdf"},
            {"estudiante": "Ana Torres", "fecha": "10/04/2026 19:40", "estado": "Entregado", "archivo": "ana_torres_practica1.docx"},
            {"estudiante": "Luis Fernández", "fecha": "—", "estado": "Pendiente", "archivo": "Sin archivo"},
            {"estudiante": "Camila Vargas", "fecha": "09/04/2026 18:20", "estado": "Entregado", "archivo": "camila_vargas_tarea.pdf"},
            {"estudiante": "Diego Romero", "fecha": "11/04/2026 02:05", "estado": "Atrasado", "archivo": "diego_romero_entrega.pdf"},
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

        body = tk.Frame(self, bg="white", padx=20, pady=18)
        body.pack(fill="both", expand=True)

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
            text="Doble clic sobre una fila para abrir el panel individual de calificación.",
            bg=self.C_GRIS_BG,
            fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(6, 14))

        resumen = tk.Frame(body, bg="white")
        resumen.pack(fill="x", pady=(0, 14))

        total = len(self.datos_entregas)
        entregados = sum(1 for x in self.datos_entregas if x["estado"] == "Entregado")
        pendientes = sum(1 for x in self.datos_entregas if x["estado"] == "Pendiente")
        atrasados = sum(1 for x in self.datos_entregas if x["estado"] == "Atrasado")

        self._label_chip(resumen, "Total", total, "#EEF4FF", "#3538CD")
        self._label_chip(resumen, "Entregados", entregados, "#ECFDF3", self.C_VERDE_TXT)
        self._label_chip(resumen, "Pendientes", pendientes, "#FFFAEB", self.C_NARANJA_TXT)
        self._label_chip(resumen, "Atrasados", atrasados, "#FEF3F2", self.C_ROJO_TXT)

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
        self.tree.bind("<Double-1>", self._abrir_calificacion)

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
            estudiante = fila["estudiante"]
            fecha = fila["fecha"]
            estado = fila["estado"]

            if filtro and filtro not in estudiante.lower():
                continue

            iid = self.tree.insert(
                "", "end",
                values=(estudiante, fecha, estado),
                tags=(self._estado_tag(estado),)
            )

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

    def _abrir_calificacion(self, event=None):
        seleccionado = self.tree.selection()
        if not seleccionado:
            return

        valores = self.tree.item(seleccionado[0], "values")
        estudiante = valores[0]

        entrega = next((x for x in self.datos_entregas if x["estudiante"] == estudiante), None)
        if not entrega:
            return

        frmCalificarEntrega(self, entrega=entrega)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmListaEntregasDocente(root)
    root.mainloop()