import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.conexion import get_conexion

def crear_tablas():
    conn = get_conexion()
    cursor = conn.cursor()

    try:
        # ── Tabla cursos ──────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                nombre TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        print("✅ Tabla cursos creada")

        # ── Tabla usuarios ────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                rol TEXT CHECK (rol IN ('docente', 'estudiante', 'administrador')),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        print("✅ Tabla usuarios creada")

        # ── Tabla tareas ──────────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tareas (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_limite TIMESTAMP NOT NULL,
                estado TEXT DEFAULT 'borrador' 
                    CHECK (estado IN ('borrador', 'publicada')),
                id_curso UUID REFERENCES cursos(id),
                id_docente UUID REFERENCES usuarios(id),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        print("✅ Tabla tareas creada")

        conn.commit()
        print("\n✅ Todas las tablas creadas exitosamente")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error al crear tablas: {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    crear_tablas()

def crear_tabla_entregas():
    conn = get_conexion()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entregas (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                id_tarea UUID REFERENCES tareas(id),
                id_estudiante UUID REFERENCES usuarios(id),
                ruta_archivo TEXT NOT NULL,
                nombre_archivo TEXT NOT NULL,
                fecha_entrega TIMESTAMP DEFAULT NOW(),
                estado TEXT DEFAULT 'entregado'
                    CHECK (estado IN ('entregado', 'anulado')),
                created_at TIMESTAMP DEFAULT NOW()
            );
        ''')
        conn.commit()
        print('Tabla entregas creada correctamente')

    except Exception as e:
        conn.rollback()
        print('Error al crear tabla entregas: ' + str(e))

    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    crear_tablas()
    crear_tabla_entregas()

def crear_tabla_inscripciones():
    try:
        conn = get_conexion()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inscripciones (
                id_estudiante UUID REFERENCES usuarios(id),
                id_curso UUID REFERENCES cursos(id),
                fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id_estudiante, id_curso)
            )
        ''')
        conn.commit()
        print("✅ Tabla inscripciones lista.")
    except Exception as e:
        print(f"❌ Error en inscripciones: {e}")
    finally:
        cursor.close()
        conn.close()

from database.sesion import IDS  # Importamos los IDs de tu .env

def inyectar_tarea_y_matricula():
    try:
        conn = get_conexion()
        cursor = conn.cursor()

        # 1. Usamos los IDs exactos de tu archivo .env
        id_docente_env = IDS['docente']
        id_estudiante_env = IDS['estudiante']
        id_curso_env = IDS['curso']

        # 2. Aseguramos que la tarea tenga asignado al DOCENTE del .env
        # Usamos 'publicada' que es el estado que permite tu CHECK
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, id_curso, id_docente, fecha_limite, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        ''', (
            '📝 Tarea para Docente y Estudiante', 
            'Esta tarea debe ser visible para ambos.', 
            id_curso_env, 
            id_docente_env, # <--- AQUÍ se vincula al docente
            '2026-12-31 23:59:00', 
            'publicada'
        ))

        # 3. Matriculamos al estudiante del .env en ese mismo curso
        cursor.execute('''
            INSERT INTO inscripciones (id_estudiante, id_curso) 
            VALUES (%s, %s) 
            ON CONFLICT DO NOTHING
        ''', (id_estudiante_env, id_curso_env))
        
        conn.commit()
        print("--------------------------------------------------")
        print(f"🚀 VÍNCULO EXITOSO")
        print(f"Docente ID: {id_docente_env}")
        print(f"Estudiante ID: {id_estudiante_env}")
        print("--------------------------------------------------")

    except Exception as e:
        print(f"❌ Error al sincronizar: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()