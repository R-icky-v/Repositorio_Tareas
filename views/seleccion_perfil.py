import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from database.sesion import iniciar_sesion

def abrir_seleccion_perfil():
    ventana = tk.Tk()
    ventana.title('Repositorio de Tareas')
    ventana.geometry('400x300')
    ventana.resizable(False, False)
    ventana.configure(bg='#f0f0f0')

    # ── Título ────────────────────────────────────────────────
    tk.Label(
        ventana,
        text='Repositorio de Tareas',
        font=('Arial', 18, 'bold'),
        bg='#f0f0f0'
    ).pack(pady=30)

    tk.Label(
        ventana,
        text='Selecciona tu perfil para continuar',
        font=('Arial', 11),
        bg='#f0f0f0',
        fg='#666666'
    ).pack(pady=5)

    # ── Botones ───────────────────────────────────────────────
    def entrar_como_docente():
        perfil = iniciar_sesion('docente')
        if perfil['id']:
            ventana.destroy()
            abrir_menu_docente(perfil)

    def entrar_como_estudiante():
        perfil = iniciar_sesion('estudiante')
        if perfil['id']:
            ventana.destroy()
            abrir_menu_estudiante(perfil)

    frame_botones = tk.Frame(ventana, bg='#f0f0f0')
    frame_botones.pack(pady=40)

    tk.Button(
        frame_botones,
        text='Docente',
        font=('Arial', 13, 'bold'),
        bg='#4a90d9',
        fg='white',
        width=12,
        height=2,
        cursor='hand2',
        command=entrar_como_docente
    ).grid(row=0, column=0, padx=20)

    tk.Button(
        frame_botones,
        text='Estudiante',
        font=('Arial', 13, 'bold'),
        bg='#27ae60',
        fg='white',
        width=12,
        height=2,
        cursor='hand2',
        command=entrar_como_estudiante
    ).grid(row=0, column=1, padx=20)

    ventana.mainloop()


def abrir_menu_docente(perfil):
    ventana = tk.Tk()
    ventana.title('Docente — ' + perfil['nombre'] + ' ' + perfil['apellido'])
    ventana.geometry('400x300')
    ventana.configure(bg='#f0f0f0')

    tk.Label(
        ventana,
        text='Bienvenido, ' + perfil['nombre'],
        font=('Arial', 16, 'bold'),
        bg='#f0f0f0'
    ).pack(pady=30)

    tk.Label(
        ventana,
        text='Perfil: Docente',
        font=('Arial', 11),
        bg='#f0f0f0',
        fg='#4a90d9'
    ).pack()

    # Aquí tus compañeros agregarán los botones del menú docente
    tk.Label(
        ventana,
        text='(Aqui iran las opciones del docente)',
        font=('Arial', 10),
        bg='#f0f0f0',
        fg='#999999'
    ).pack(pady=20)

    ventana.mainloop()


def abrir_menu_estudiante(perfil):
    ventana = tk.Tk()
    ventana.title('Estudiante — ' + perfil['nombre'] + ' ' + perfil['apellido'])
    ventana.geometry('400x300')
    ventana.configure(bg='#f0f0f0')

    tk.Label(
        ventana,
        text='Bienvenido, ' + perfil['nombre'],
        font=('Arial', 16, 'bold'),
        bg='#f0f0f0'
    ).pack(pady=30)

    tk.Label(
        ventana,
        text='Perfil: Estudiante',
        font=('Arial', 11),
        bg='#f0f0f0',
        fg='#27ae60'
    ).pack()

    # Aquí tus compañeros agregarán los botones del menú estudiante
    tk.Label(
        ventana,
        text='(Aqui iran las opciones del estudiante)',
        font=('Arial', 10),
        bg='#f0f0f0',
        fg='#999999'
    ).pack(pady=20)

    ventana.mainloop()


if __name__ == '__main__':
    abrir_seleccion_perfil()
    
