import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Perfil activo — None hasta que el usuario elija
perfil_activo = {
    'id':       None,
    'nombre':   None,
    'apellido': None,
    'rol':      None
}

# IDs fijos cargados del .env
IDS = {
    'docente':    os.getenv('ID_DOCENTE'),
    'estudiante': os.getenv('ID_ESTUDIANTE'),
    'curso':      os.getenv('ID_CURSO')
}

def iniciar_sesion(rol):
    from database.conexion import get_conexion
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        id_usuario = IDS[rol]
        cursor.execute('''
            SELECT id, nombre, apellido, rol
            FROM usuarios
            WHERE id = %s
        ''', (id_usuario,))
        usuario = cursor.fetchone()
        if usuario:
            perfil_activo['id']       = usuario[0]
            perfil_activo['nombre']   = usuario[1]
            perfil_activo['apellido'] = usuario[2]
            perfil_activo['rol']      = usuario[3]
            print('Sesion iniciada como: ' + usuario[3])
        cursor.close()
        conn.close()
        return perfil_activo
    except Exception as e:
        print('Error al iniciar sesion: ' + str(e))

def obtener_perfil():
    return perfil_activo

def cerrar_sesion():
    perfil_activo['id']       = None
    perfil_activo['nombre']   = None
    perfil_activo['apellido'] = None
    perfil_activo['rol']      = None
    print('Sesion cerrada')