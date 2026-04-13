import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

perfil_activo = {
    'id':       None,
    'nombre':   None,
    'apellido': None,
    'rol':      None
}

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
        id_curso_defecto = IDS['curso'] # Obtenemos el ID del curso del .env

        # 1. ASEGURAR EL CURSO (Nuevo bloque)
        # Esto evita el error de "foreign key constraint"
        cursor.execute("SELECT id FROM cursos WHERE id = %s", (id_curso_defecto,))
        if not cursor.fetchone():
            print(f"⚠️ Curso por defecto no encontrado. Creándolo...")
            cursor.execute('''
                INSERT INTO cursos (id, nombre) 
                VALUES (%s, %s)
            ''', (id_curso_defecto, "Sistemas de Información I"))
            conn.commit()

        # 2. ASEGURAR EL USUARIO
        cursor.execute('''
            SELECT id, nombre, apellido, rol
            FROM usuarios
            WHERE id = %s
        ''', (id_usuario,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"⚠️ Usuario {rol} no encontrado. Creando perfil...")
            # Personalizamos según el rol para no confundirlos
            if rol == 'estudiante':
                nombre, apellido = "Pedro", "Diaz"
            else:
                nombre, apellido = "Doctor", "Docente"
                
            email = f"{rol}.{id_usuario[:5]}@umss.edu" # Email único basado en ID
            
            cursor.execute('''
                INSERT INTO usuarios (id, nombre, apellido, email, rol)
                VALUES (%s, %s, %s, %s, %s)
            ''', (id_usuario, nombre, apellido, email, rol))
            conn.commit()
            usuario = (id_usuario, nombre, apellido, rol)

        # 3. CARGAR PERFIL
        perfil_activo['id']       = usuario[0]
        perfil_activo['nombre']   = usuario[1]
        perfil_activo['apellido'] = usuario[2]
        perfil_activo['rol']      = usuario[3]
        
        print('✅ Sesion e infraestructura listas.')
        
        cursor.close()
        conn.close()
        return perfil_activo
        
    except Exception as e:
        print('❌ Error: ' + str(e))
        return {'id': None}