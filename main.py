import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Actualizamos el import con el nuevo nombre
from database.crear_tablas import crear_tablas, crear_tabla_entregas, crear_tabla_inscripciones, inyectar_tarea_y_matricula
from views.seleccion_perfil import abrir_seleccion_perfil

if __name__ == '__main__':
    # 1. Crear infraestructura
    crear_tablas()
    crear_tabla_inscripciones() 
    crear_tabla_entregas()
    
    # 2. Inyectar los datos 100% seguros
    #
    inyectar_tarea_y_matricula()
    
    # 3. Iniciar App
    abrir_seleccion_perfil()
    