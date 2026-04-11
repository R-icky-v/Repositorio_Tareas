import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.crear_tablas import crear_tablas, crear_tabla_entregas
from views.seleccion_perfil import abrir_seleccion_perfil

if __name__ == '__main__':
    # Crear tablas si no existen
    crear_tablas()
    crear_tabla_entregas()
    
    # Abrir pantalla de seleccion
    abrir_seleccion_perfil()