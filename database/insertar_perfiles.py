import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.conexion import get_conexion

def insertar_perfiles():
    conn = get_conexion()
    cursor = conn.cursor()

    try:
        # Limpiar perfiles anteriores
        cursor.execute('DELETE FROM entregas')
        cursor.execute('DELETE FROM tareas')
        cursor.execute('DELETE FROM usuarios')
        cursor.execute('DELETE FROM cursos')

        # Insertar curso
        cursor.execute('''
            INSERT INTO cursos (nombre)
            VALUES ('Sistemas de Informacion II')
            RETURNING id
        ''')
        id_curso = cursor.fetchone()[0]

        # Insertar docente
        cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, email, rol)
            VALUES ('Carlos', 'Mamani', 'docente@sis.com', 'docente')
            RETURNING id
        ''')
        id_docente = cursor.fetchone()[0]

        # Insertar estudiante
        cursor.execute('''
            INSERT INTO usuarios (nombre, apellido, email, rol)
            VALUES ('Maria', 'Lopez', 'estudiante@sis.com', 'estudiante')
            RETURNING id
        ''')
        id_estudiante = cursor.fetchone()[0]

        conn.commit()

        print('Perfiles creados correctamente')
        print('ID docente:     ' + str(id_docente))
        print('ID estudiante:  ' + str(id_estudiante))
        print('ID curso:       ' + str(id_curso))

        return {
            'id_docente':    id_docente,
            'id_estudiante': id_estudiante,
            'id_curso':      id_curso
        }

    except Exception as e:
        conn.rollback()
        print('Error al insertar perfiles: ' + str(e))

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    insertar_perfiles()