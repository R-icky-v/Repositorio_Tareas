import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tkinter as tk
from tkinter import ttk, messagebox
from database.sesion import iniciar_sesion
from views.crear_tarea_view import CrearTareaView
from views.ver_tareas_view import VerTareasView 
from views.tareas_estudiante_view import TareasEstudianteView
from views.ver_calificaciones_view import VerCalificacionesView

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

    # ── Botones de Selección ──────────────────────────────────
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
    ventana.geometry('400x450') 
    ventana.configure(bg='#f0f0f0')

    tk.Label(
        ventana,
        text='Bienvenido, ' + perfil['nombre'],
        font=('Arial', 16, 'bold'),
        bg='#f0f0f0'
    ).pack(pady=20)

    # --- ACCIONES DEL DOCENTE ---
    def ir_a_crear_tarea():
        # ID de curso estático para pruebas
        id_curso_prueba = "c3808b8b-dab9-47f1-9809-dcd2848849d4" 
        CrearTareaView(ventana, id_curso_prueba, perfil['id'])

    def ir_a_ver_tareas():
        """
        Esta es la clave: VerTareasView debe contener el botón 
        de 'Calificar' para cada tarea seleccionada.
        """
        VerTareasView(ventana, perfil['id'])

    # --- BOTÓN 1: CREAR (US-09) ---
    tk.Button(
        ventana,
        text='➕ Crear Nueva Tarea',
        font=('Arial', 12, 'bold'),
        bg='#4a90d9',
        fg='white',
        width=20,
        height=2,
        cursor='hand2',
        command=ir_a_crear_tarea
    ).pack(pady=10)

    # --- BOTÓN 2: VER Y CALIFICAR (US-10) ---
    tk.Button(
        ventana,
        text='📋 Gestionar y Calificar',
        font=('Arial', 12),
        bg='white',
        fg='#333333',
        width=20,
        height=2,
        cursor='hand2',
        command=ir_a_ver_tareas 
    ).pack(pady=10)

    # Botón para salir
    tk.Button(
        ventana,
        text='Cerrar Sesión',
        font=('Arial', 10),
        command=ventana.destroy,
        bg='#e74c3c',
        fg='white',
        width=15
    ).pack(pady=20)

    ventana.mainloop()


def abrir_menu_estudiante(perfil):
    ventana = tk.Tk()
    ventana.title('Estudiante — ' + perfil['nombre'] + ' ' + perfil['apellido'])
    ventana.geometry('400x450') # Aumentamos un poco el alto para el nuevo botón
    ventana.configure(bg='#f0f0f0')

    tk.Label(
        ventana,
        text='Bienvenido, ' + perfil['nombre'],
        font=('Arial', 16, 'bold'),
        bg='#f0f0f0'
    ).pack(pady=30)

    # --- LÓGICA DE NAVEGACIÓN ---
    def ejecutar_ver_tareas():
        TareasEstudianteView(ventana, perfil['id'])

    def ejecutar_ver_calificaciones():
        # Llamada a la vista de la US-05
        VerCalificacionesView(ventana, perfil['id'])

    # --- BOTÓN 1: TAREAS (US-03) ---
    tk.Button(
        ventana,
        text='📋 Ver Tareas Pendientes',
        font=('Arial', 11, 'bold'),
        command=ejecutar_ver_tareas,
        bg='#3498db',
        fg='white',
        width=25,
        pady=10,
        cursor='hand2'
    ).pack(pady=10)

    # --- BOTÓN 2: CALIFICACIONES (US-05) ---
    tk.Button(
        ventana,
        text='⭐ Mis Calificaciones',
        font=('Arial', 11, 'bold'),
        command=ejecutar_ver_calificaciones,
        bg='#27ae60', # Color verde para diferenciarlo
        fg='white',
        width=25,
        pady=10,
        cursor='hand2'
    ).pack(pady=10)

    # Botón para salir
    tk.Button(
        ventana,
        text='Cerrar Sesión',
        font=('Arial', 10),
        command=ventana.destroy,
        bg='#e74c3c',
        fg='white',
        width=15
    ).pack(pady=25)

    ventana.mainloop()

if __name__ == '__main__':
    abrir_seleccion_perfil()