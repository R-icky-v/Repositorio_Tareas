import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime, timedelta

class frmEntregaTarea(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Entrega de tarea")
        self.geometry("560x760")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        self.archivo_seleccionado = ""
        self.entrega_realizada = False

        # Simulación de fecha límite
        # Cambia esto por tu fecha real
        self.fecha_limite = datetime.now() + timedelta(minutes=5)

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
        self.C_BLOQ_BG   = "#E5E7EB"
        self.C_BLOQ_TXT  = "#98A2B3"

        self._build_ui()
        self._verificar_estado_entrega()

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

        # Información de tarea
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

        self.lbl_fecha_limite = tk.Label(
            card_info,
            text="Fecha límite: --/--/---- --:--",
            bg=self.C_GRIS_BG, fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_fecha_limite.pack(anchor="w", padx=14, pady=(6, 12))

        # Estado general
        self.lbl_estado_general = tk.Label(
            body,
            text="Formulario listo para entregar.",
            bg="white", fg=self.C_HINT,
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_estado_general.pack(anchor="w", pady=(0, 8))

        # Área de carga
        self._label(body, "Archivo de entrega", required=True)

        self.drop = tk.Frame(
            body, bg=self.C_GRIS_BG, bd=0,
            highlightthickness=1, highlightbackground=self.C_GRIS_BD
        )
        self.drop.pack(fill="x", pady=(4, 0), ipady=14)

        tk.Label(
            self.drop, text="↑", bg=self.C_GRIS_BG, fg=self.C_AZUL,
            font=("Segoe UI", 22)
        ).pack()

        tk.Label(
            self.drop, text="Adjuntar archivo de entrega",
            bg=self.C_GRIS_BG, fg=self.C_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack()

        tk.Label(
            self.drop, text="PDF, DOCX, PNG, JPG — máx. 10 MB",
            bg=self.C_GRIS_BG, fg=self.C_HINT,
            font=("Segoe UI", 8)
        ).pack()

        self.btn_archivo = tk.Label(
            self.drop, text="Examinar archivo", bg="white", fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold"), cursor="hand2",
            padx=14, pady=6, relief="flat",
            highlightthickness=1, highlightbackground=self.C_AZUL
        )
        self.btn_archivo.pack(pady=(10, 0))
        self.btn_archivo.bind("<Button-1>", lambda e: self._examinar())
        self.btn_archivo.bind("<Enter>", lambda e: self._on_hover_archivo(True))
        self.btn_archivo.bind("<Leave>", lambda e: self._on_hover_archivo(False))

        self.lbl_archivo = tk.Label(
            body, text="Ningún archivo seleccionado",
            bg="white", fg=self.C_HINT, font=("Segoe UI", 8)
        )
        self.lbl_archivo.pack(anchor="w", pady=(6, 0))

        # Confirmación visual
        self.lbl_confirmacion = tk.Label(
            body,
            text="",
            bg="white",
            fg=self.C_VERDE,
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_confirmacion.pack(anchor="w", pady=(18, 0))

        self.lbl_detalle_confirmacion = tk.Label(
            body,
            text="",
            bg="white",
            fg=self.C_LABEL,
            font=("Segoe UI", 8)
        )
        self.lbl_detalle_confirmacion.pack(anchor="w", pady=(4, 0))

        # Aviso de bloqueo
        self.lbl_bloqueo = tk.Label(
            body,
            text="",
            bg="white",
            fg=self.C_ERROR,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_bloqueo.pack(anchor="w", pady=(14, 0))

        # Footer
        sep = tk.Frame(self, bg=self.C_GRIS_BD, height=1)
        sep.pack(fill="x", side="bottom", before=body)

        footer = tk.Frame(self, bg=self.C_GRIS_BG, padx=24, pady=14)
        footer.pack(fill="x", side="bottom")

        self.btn_cancelar = self._btn(
            footer, "Cancelar", "#F0F2F5", self.C_LABEL, "#E2E5EA",
            self.destroy, width=10
        )
        self.btn_cancelar.pack(side="left")

        self.btn_reemplazar = self._btn(
            footer, "Reemplazar archivo", "#E6F1FB", self.C_AZUL, "#C8DFF5",
            self._examinar, width=16
        )
        self.btn_reemplazar.pack(side="left", padx=10)

        self.btn_enviar = self._btn(
            footer, "Enviar entrega", self.C_VERDE, "white", self.C_VERDE_HOV,
            self._enviar, width=14
        )
        self.btn_enviar.pack(side="right")

    def _on_hover_archivo(self, enter):
        if getattr(self, "bloqueado", False):
            return
        if enter:
            self.btn_archivo.configure(bg=self.C_AZUL, fg="white")
        else:
            self.btn_archivo.configure(bg="white", fg=self.C_AZUL)

    def _examinar(self):
        if getattr(self, "bloqueado", False):
            return

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
        self.lbl_estado_general.configure(
            text="Archivo listo para enviar.",
            fg=self.C_VERDE
        )

    def _abrir_modal_carga(self):
        self.modal = tk.Toplevel(self)
        self.modal.title("Subiendo archivo")
        self.modal.geometry("360x180")
        self.modal.resizable(False, False)
        self.modal.configure(bg="white")
        self.modal.transient(self)
        self.modal.grab_set()
        self.modal.protocol("WM_DELETE_WINDOW", lambda: None)

        cont = tk.Frame(self.modal, bg="white", padx=24, pady=20)
        cont.pack(fill="both", expand=True)

        tk.Label(
            cont, text="Procesando entrega",
            bg="white", fg=self.C_TEXTO,
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            cont, text="Espere mientras se carga su archivo...",
            bg="white", fg=self.C_LABEL,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(4, 14))

        self.pb = ttk.Progressbar(
            cont, orient="horizontal", mode="determinate", length=290
        )
        self.pb.pack(fill="x")

        self.lbl_pb = tk.Label(
            cont, text="0%",
            bg="white", fg=self.C_AZUL,
            font=("Segoe UI", 9, "bold")
        )
        self.lbl_pb.pack(anchor="e", pady=(8, 0))

        self.lbl_pb_estado = tk.Label(
            cont, text="Iniciando carga...",
            bg="white", fg=self.C_HINT,
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_pb_estado.pack(anchor="w", pady=(12, 0))

        self._animar_progreso(0)

    def _animar_progreso(self, valor):
        if valor > 100:
            self.modal.destroy()
            self._confirmar_entrega()
            return

        self.pb["value"] = valor
        self.lbl_pb.configure(text=f"{valor}%")

        if valor < 25:
            txt = "Validando archivo..."
        elif valor < 60:
            txt = "Subiendo contenido..."
        elif valor < 90:
            txt = "Registrando entrega..."
        else:
            txt = "Finalizando proceso..."

        self.lbl_pb_estado.configure(text=txt)
        self.modal.after(35, lambda: self._animar_progreso(valor + 2))

    def _confirmar_entrega(self):
        self.entrega_realizada = True

        nombre = os.path.basename(self.archivo_seleccionado)
        fecha_entrega = datetime.now().strftime("%d/%m/%Y %H:%M")

        self.lbl_confirmacion.configure(
            text="✔ ENTREGADO CORRECTAMENTE"
        )
        self.lbl_detalle_confirmacion.configure(
            text=f"Archivo enviado: {nombre} | Fecha de entrega: {fecha_entrega}"
        )
        self.lbl_estado_general.configure(
            text="La entrega fue registrada con éxito.",
            fg=self.C_VERDE
        )

        self._bloquear_por_entregado()

        messagebox.showinfo(
            "Entrega completada",
            "Tu tarea fue entregada correctamente."
        )

    def _bloquear_por_entregado(self):
        self._desactivar_boton_label(
            self.btn_enviar, self.C_BLOQ_BG, self.C_BLOQ_TXT
        )
        self._desactivar_boton_label(
            self.btn_archivo, self.C_BLOQ_BG, self.C_BLOQ_TXT, borde=self.C_GRIS_BD
        )
        self._desactivar_boton_label(
            self.btn_reemplazar, self.C_BLOQ_BG, self.C_BLOQ_TXT
        )

    def _bloquear_por_fecha(self):
        self.bloqueado = True

        self._desactivar_boton_label(
            self.btn_enviar, self.C_BLOQ_BG, self.C_BLOQ_TXT
        )
        self._desactivar_boton_label(
            self.btn_archivo, self.C_BLOQ_BG, self.C_BLOQ_TXT, borde=self.C_GRIS_BD
        )
        self._desactivar_boton_label(
            self.btn_reemplazar, self.C_BLOQ_BG, self.C_BLOQ_TXT
        )

        self.lbl_estado_general.configure(
            text="La fecha límite fue superada.",
            fg=self.C_ERROR
        )
        self.lbl_bloqueo.configure(
            text="⛔ Entrega bloqueada por vencimiento del plazo."
        )

    def _desactivar_boton_label(self, widget, bg, fg, borde=None):
        widget.configure(bg=bg, fg=fg, cursor="arrow")
        widget.unbind("<Button-1>")
        widget.unbind("<Enter>")
        widget.unbind("<Leave>")
        if borde:
            widget.configure(highlightbackground=borde)

    def _verificar_estado_entrega(self):
        ahora = datetime.now()
        self.lbl_fecha_limite.configure(
            text=f"Fecha límite: {self.fecha_limite.strftime('%d/%m/%Y %H:%M')}"
        )

        if not self.entrega_realizada and ahora > self.fecha_limite:
            self._bloquear_por_fecha()
            return

        if not self.entrega_realizada:
            restante = self.fecha_limite - ahora
            total_seg = int(restante.total_seconds())

            if total_seg <= 0:
                self._bloquear_por_fecha()
                return

            horas = total_seg // 3600
            minutos = (total_seg % 3600) // 60
            segundos = total_seg % 60

            self.lbl_estado_general.configure(
                text=f"Tiempo restante: {horas:02d}:{minutos:02d}:{segundos:02d}",
                fg=self.C_AZUL
            )

            self.after(1000, self._verificar_estado_entrega)

    def _enviar(self):
        if getattr(self, "bloqueado", False):
            return

        if self.entrega_realizada:
            messagebox.showinfo(
                "Entrega registrada",
                "La tarea ya fue entregada anteriormente."
            )
            return

        if not self.archivo_seleccionado:
            messagebox.showwarning(
                "Archivo requerido",
                "Debes seleccionar un archivo antes de enviar la entrega."
            )
            self.lbl_estado_general.configure(
                text="Falta seleccionar un archivo.",
                fg=self.C_ERROR
            )
            return

        if datetime.now() > self.fecha_limite:
            self._bloquear_por_fecha()
            return

        confirmar = messagebox.askyesno(
            "Confirmar entrega",
            "¿Deseas enviar tu archivo de entrega ahora?"
        )

        if not confirmar:
            self.lbl_estado_general.configure(
                text="La entrega fue cancelada por el usuario.",
                fg=self.C_HINT
            )
            return

        self._abrir_modal_carga()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = frmEntregaTarea(root)
    root.mainloop()