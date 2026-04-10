import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os

class frmCrearTarea(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Crear nueva tarea")
        self.geometry("560x820")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")
        self.archivo_seleccionado = ""

        # Datos de cursos (solo para IU)
        self.cursos_info = {
            "Sistemas Operativos": "Docente: Ing. Pérez | Paralelo A | Lun-Mié 08:00",
            "Base de Datos II": "Docente: Lic. Gómez | Paralelo B | Mar-Jue 10:00",
            "Programación II": "Docente: Ing. Rojas | Paralelo A | Lun-Vie 14:00",
            "Redes I": "Docente: Ing. Torres | Paralelo C | Sáb 08:00",
            "Ingeniería de Software II": "Docente: Ing. Vargas | Paralelo B | Vie 18:30"
        }

        # Colores
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

    def _entry(self, parent, placeholder="", height=None):
        frame = tk.Frame(parent, bg=self.C_GRIS_BD, bd=0)
        inner = tk.Frame(frame, bg="white", bd=0)
        inner.pack(padx=1, pady=1, fill="both", expand=True)

        if height:
            widget = tk.Text(inner, font=("Segoe UI", 10), height=height,
                             bd=0, relief="flat", bg="white", fg=self.C_HINT,
                             insertbackground=self.C_AZUL, wrap="word",
                             padx=10, pady=8)
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
        else:
            widget = tk.Entry(inner, font=("Segoe UI", 10),
                              bd=0, relief="flat", bg="white", fg=self.C_HINT,
                              insertbackground=self.C_AZUL)
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

        widget.pack(fill="both", expand=True, padx=2)

        return frame, widget

    def _label(self, parent, text, required=False):
        f = tk.Frame(parent, bg="white")
        f.pack(fill="x", pady=(14, 3))
        tk.Label(f, text=text, bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        if required:
            tk.Label(f, text=" *", bg="white", fg=self.C_ERROR,
                     font=("Segoe UI", 9, "bold")).pack(side="left")

    def _btn(self, parent, text, bg, fg, hover, command, width=14):
        btn = tk.Label(parent, text=text, bg=bg, fg=fg,
                       font=("Segoe UI", 10, "bold"),
                       cursor="hand2", padx=18, pady=10,
                       relief="flat", bd=0, width=width)
        btn.bind("<Button-1>", lambda e: command())
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        return btn

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────
        header = tk.Frame(self, bg=self.C_AZUL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="  +  ", bg="#155A9E", fg="white",
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=(16, 0))
        tk.Label(header, text="Nueva tarea", bg=self.C_AZUL, fg="white",
                 font=("Segoe UI", 13, "bold")).pack(side="left", padx=10)
        tk.Label(header, text="US-09 · Docente", bg=self.C_AZUL, fg="#A8C8F0",
                 font=("Segoe UI", 9)).pack(side="right", padx=18)

        # ── Cuerpo ──────────────────────────────────────────────
        body = tk.Frame(self, bg="white", padx=28, pady=6)
        body.pack(fill="both", expand=True)

        # Título
        self._label(body, "Título de la tarea", required=True)
        ef, self.txtTitulo = self._entry(body, "Ej: Práctica 1 — Circuitos en serie")
        ef.pack(fill="x", ipady=4)

        # Descripción
        self._label(body, "Descripción", required=True)
        ef2, self.rtbDescripcion = self._entry(
            body,
            "Describí los objetivos y requisitos de la tarea...",
            height=4
        )
        ef2.pack(fill="x")

        # Fecha + Hora
        fila = tk.Frame(body, bg="white")
        fila.pack(fill="x", pady=(14, 0))

        col1 = tk.Frame(fila, bg="white")
        col1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(col1, text="Fecha límite ", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(col1, text="*", bg="white", fg=self.C_ERROR,
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        ef3, self.txtFecha = self._entry(col1, "dd/mm/aaaa")
        ef3.pack(fill="x", ipady=4, pady=(3, 0))

        col2 = tk.Frame(fila, bg="white")
        col2.pack(side="left", fill="x", expand=True)
        tk.Label(col2, text="Hora límite", bg="white", fg=self.C_LABEL,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ef4, self.txtHora = self._entry(col2, "23:59")
        ef4.pack(fill="x", ipady=4, pady=(3, 0))

        # ── TU APORTE: Curso asignado ───────────────────────────
        self._label(body, "Curso asignado", required=True)

        frame_combo = tk.Frame(body, bg=self.C_GRIS_BD, bd=0)
        frame_combo.pack(fill="x")

        inner_combo = tk.Frame(frame_combo, bg="white", bd=0)
        inner_combo.pack(padx=1, pady=1, fill="both", expand=True)

        self.cmbCurso = ttk.Combobox(
            inner_combo,
            state="readonly",
            font=("Segoe UI", 10),
            values=["Seleccione un curso"] + list(self.cursos_info.keys())
        )
        self.cmbCurso.pack(fill="x", padx=8, pady=8, ipady=4)
        self.cmbCurso.current(0)
        self.cmbCurso.bind("<<ComboboxSelected>>", self._actualizar_info_curso)

        self.lbl_info_curso = tk.Label(
            body,
            text="Selecciona un curso para ver más detalles.",
            bg="white",
            fg=self.C_HINT,
            font=("Segoe UI", 8)
        )
        self.lbl_info_curso.pack(anchor="w", pady=(4, 0))

        self.lbl_estado_curso = tk.Label(
            body,
            text="",
            bg="white",
            fg=self.C_VERDE,
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_estado_curso.pack(anchor="w", pady=(2, 0))

        # Material de apoyo
        self._label(body, "Material de apoyo")
        tk.Label(body, text="(opcional)", bg="white", fg=self.C_HINT,
                 font=("Segoe UI", 8)).pack(anchor="w")

        drop = tk.Frame(body, bg=self.C_GRIS_BG, bd=0,
                        highlightthickness=1, highlightbackground=self.C_GRIS_BD)
        drop.pack(fill="x", pady=(4, 0), ipady=12)

        tk.Label(drop, text="↑", bg=self.C_GRIS_BG, fg=self.C_AZUL,
                 font=("Segoe UI", 18)).pack()
        tk.Label(drop, text="Adjuntar archivo", bg=self.C_GRIS_BG, fg=self.C_TEXTO,
                 font=("Segoe UI", 10, "bold")).pack()
        tk.Label(drop, text="PDF, DOC, PNG — máx. 10 MB", bg=self.C_GRIS_BG,
                 fg=self.C_HINT, font=("Segoe UI", 8)).pack()

        btn_arch = tk.Label(drop, text="Examinar archivo", bg="white", fg=self.C_AZUL,
                            font=("Segoe UI", 9, "bold"), cursor="hand2",
                            padx=14, pady=6, relief="flat",
                            highlightthickness=1, highlightbackground=self.C_AZUL)
        btn_arch.pack(pady=(8, 0))
        btn_arch.bind("<Button-1>", lambda e: self._examinar())
        btn_arch.bind("<Enter>", lambda e: btn_arch.configure(bg=self.C_AZUL, fg="white"))
        btn_arch.bind("<Leave>", lambda e: btn_arch.configure(bg="white", fg=self.C_AZUL))

        self.lbl_archivo = tk.Label(body, text="Ningún archivo seleccionado",
                                    bg="white", fg=self.C_HINT, font=("Segoe UI", 8))
        self.lbl_archivo.pack(anchor="w", pady=(4, 0))

        # Estado visual pequeño
        self.lbl_estado = tk.Label(
            body,
            text="Formulario listo para completar.",
            bg="white",
            fg=self.C_HINT,
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_estado.pack(anchor="w", pady=(12, 0))

        self.lbl_confirmacion = tk.Label(
            body,
            text="",
            bg="white",
            fg=self.C_VERDE,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_confirmacion.pack(anchor="w", pady=(6, 0))
        
        # ── Footer con botones ──────────────────────────────────
        sep = tk.Frame(self, bg=self.C_GRIS_BD, height=1)
        sep.pack(fill="x", side="bottom", before=body)

        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self._btn(footer, "Cancelar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
                  self.destroy, width=10).pack(side="left")

        self._btn(footer, "Guardar borrador", "#E6F1FB", self.C_AZUL, "#C8DFF5",
                  self._guardar_borrador, width=14).pack(side="left", padx=10)

        self._btn(footer, "  Publicar tarea  ", self.C_VERDE, "white", self.C_VERDE_HOV,
                  self._publicar, width=14).pack(side="right")

    # ── Lógica ──────────────────────────────────────────────────
    def _examinar(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("PDF", ".pdf"), ("Word", ".docx"),
                       ("Imágenes", ".png *.jpg *.jpeg"), ("Todos", ".*")]
        )
        if ruta:
            self.archivo_seleccionado = ruta
            nombre = os.path.basename(ruta)
            self.lbl_archivo.configure(text=f"Archivo: {nombre}", fg=self.C_VERDE)
            self.lbl_estado.configure(text="Archivo adjunto correctamente.", fg=self.C_VERDE)

    def _actualizar_info_curso(self, event=None):
        curso = self.cmbCurso.get()

        if curso == "Seleccione un curso":
            self.lbl_info_curso.configure(
                text="Selecciona un curso para ver más detalles.",
                fg=self.C_HINT
            )
            self.lbl_estado_curso.configure(text="")
            self.lbl_estado.configure(text="Aún falta seleccionar un curso.", fg=self.C_HINT)
            return

        info = self.cursos_info.get(curso, "Sin información adicional.")
        self.lbl_info_curso.configure(text=info, fg=self.C_LABEL)
        self.lbl_estado_curso.configure(text="✔ Curso asignado correctamente.")
        self.lbl_estado.configure(text=f"Curso '{curso}' seleccionado.", fg=self.C_VERDE)

    def _get_text(self, widget):
        if isinstance(widget, tk.Text):
            val = widget.get("1.0", "end").strip()
            return "" if getattr(widget, "_is_ph", False) else val
        else:
            return "" if getattr(widget, "_is_ph", False) else widget.get().strip()

    def _validar(self):
        if not self._get_text(self.txtTitulo):
            messagebox.showwarning("Campo requerido", "El título no puede estar vacío.")
            self.txtTitulo.focus()
            self.lbl_estado.configure(text="Falta completar el título.", fg=self.C_ERROR)
            return False

        if not self._get_text(self.rtbDescripcion):
            messagebox.showwarning("Campo requerido", "La descripción no puede estar vacía.")
            self.lbl_estado.configure(text="Falta completar la descripción.", fg=self.C_ERROR)
            return False

        if not self._get_text(self.txtFecha):
            messagebox.showwarning("Campo requerido", "Ingresá una fecha límite.")
            self.txtFecha.focus()
            self.lbl_estado.configure(text="Falta completar la fecha límite.", fg=self.C_ERROR)
            return False

        if self.cmbCurso.get() == "Seleccione un curso":
            messagebox.showwarning("Campo requerido", "Debes seleccionar un curso.")
            self.lbl_estado.configure(text="Falta seleccionar el curso.", fg=self.C_ERROR)
            self.cmbCurso.focus()
            return False

        return True

    def _guardar_borrador(self):
        if not self._get_text(self.txtTitulo):
            messagebox.showwarning("Aviso", "Ingresá al menos un título para guardar el borrador.")
            self.lbl_estado.configure(text="No se pudo guardar el borrador.", fg=self.C_ERROR)
            return

        self.lbl_estado.configure(text="Borrador guardado correctamente.", fg=self.C_VERDE)
        messagebox.showinfo("Borrador guardado", "La tarea fue guardada como borrador.")

    def _publicar(self):
        if not self._validar():
            self.lbl_confirmacion.configure(text="")
            return

        titulo = self._get_text(self.txtTitulo)
        curso = self.cmbCurso.get()

        confirmar = messagebox.askyesno(
            "Confirmar publicación",
            f"¿Deseas publicar la tarea '{titulo}' en el curso '{curso}'?"
        )

        if not confirmar:
           self.lbl_estado.configure(text="La publicación fue cancelada.", fg=self.C_HINT)
           self.lbl_confirmacion.configure(text="")
           return

        self.lbl_estado.configure(
            text=f"Tarea preparada para el curso: {curso}",
            fg=self.C_VERDE
        )

        self.lbl_confirmacion.configure(
            text=f"✔ La tarea '{titulo}' fue asignada y publicada correctamente en '{curso}'."
        )

        messagebox.showinfo(
            "Tarea publicada",
            f"'{titulo}' fue publicada correctamente en '{curso}'."
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmCrearTarea(root)
    root.mainloop()