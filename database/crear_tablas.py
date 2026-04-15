import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.conexion import get_conexion
from database.sesion import IDS  # Importamos los IDs estáticos para la sincronización

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.conexion import get_conexion
from database.sesion import IDS  

def crear_tablas():
    conn = get_conexion()
    if conn is None: return 
    try:
        cursor = conn.cursor()
        # Estructura base (Cursos, Usuarios, Tareas)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                nombre TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS usuarios (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                rol TEXT CHECK (rol IN ('docente', 'estudiante', 'administrador')),
                created_at TIMESTAMP DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS tareas (
                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha_limite TIMESTAMP NOT NULL,
                estado TEXT DEFAULT 'borrador' CHECK (estado IN ('borrador', 'publicada')),
                id_curso UUID REFERENCES cursos(id),
                id_docente UUID REFERENCES usuarios(id),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        print("✅ Estructura base verificada")
    except Exception as e:
        if conn: conn.rollback()
        print(f"❌ Error Estructura: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()

def crear_tabla_inscripciones():
    conn = get_conexion()
    if conn is None: return
    try:
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
        print("✅ Tabla inscripciones verificada")
    except Exception as e:
        if conn: conn.rollback()
        print(f"❌ Error Inscripciones: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()

def inyectar_tarea_y_matricula():
    conn = get_conexion()
    if conn is None: return
    try:
        cursor = conn.cursor()
        id_docente = IDS['docente']
        id_estudiante = IDS['estudiante']
        id_curso = IDS['curso']

        # 1. Asegurar el curso
        cursor.execute("INSERT INTO cursos (id, nombre) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", 
                       (id_curso, "Sistemas de Información I"))

        # 2. Asegurar el estudiante en la tabla usuarios (Si no existe, el FK de inscripciones falla)
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, apellido, email, rol) 
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """, (id_estudiante, "Pedro", "Diaz", "estudiante@umss.edu", "estudiante"))

        # 3. Asegurar el docente
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, apellido, email, rol) 
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """, (id_docente, "Doctor", "Docente", "docente@umss.edu", "docente"))

        # 4. Inscribir al estudiante (EL PUENTE CRÍTICO)
        cursor.execute("INSERT INTO inscripciones (id_estudiante, id_curso) VALUES (%s, %s) ON CONFLICT DO NOTHING", 
                       (id_estudiante, id_curso))

        # 5. Crear la tarea PUBLICA (Si está en borrador, el estudiante no la ve)
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, id_curso, id_docente, fecha_limite, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        ''', ('📝 Proyecto Final', 'Presentación del sistema.', id_curso, id_docente, '2026-12-31', 'publicada'))
        
        # Dentro de inyectar_tarea_y_matricula...
        # 6. MIGRACIÓN AUTOMÁTICA (Asignamos las tareas viejas al nuevo docente)
        cursor.execute("UPDATE tareas SET id_docente = %s WHERE id_docente != %s OR id_docente IS NULL", 
                    (id_docente, id_docente))
        #conn.commit()

        conn.commit()
        print("🚀 Flujo Sincronizado: Estudiante, Curso e Inscripción vinculados.")
    except Exception as e:
        print(f"❌ Error Sincronización: {e}")
        if conn: conn.rollback()
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()

def crear_tabla_entregas():
    conn = get_conexion()
    if conn is None: return
    try:
        cursor = conn.cursor()
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
        print('✅ Tabla entregas lista')
    except Exception as e:
        if conn: conn.rollback()
        print('❌ Error entregas: ' + str(e))
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()

def crear_tabla_inscripciones():
    conn = get_conexion()
    if conn is None: return
    try:
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
        if conn: conn.rollback()
        print(f"❌ Error inscripciones: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()

def inyectar_tarea_y_matricula():
    conn = get_conexion()
    if conn is None: return
    try:
        cursor = conn.cursor()
        from database.sesion import IDS
        
        id_docente = IDS['docente']
        id_estudiante = IDS['estudiante']
        id_curso = IDS['curso']

        # 1. Asegurar el CURSO
        cursor.execute("INSERT INTO cursos (id, nombre) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING", 
                        (id_curso, "Sistemas de Información I"))

        # 2. Asegurar el ESTUDIANTE
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, apellido, email, rol) 
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """, (id_estudiante, "Pedro", "Diaz", "pedro@umss.edu", "estudiante"))

        # 3. Asegurar el DOCENTE
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, apellido, email, rol) 
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING
        """, (id_docente, "Doctor", "Docente", "docente@umss.edu", "docente"))

        # 4. CREAR UNA TAREA DE PRUEBA (Solo si no existe ninguna)
        cursor.execute('''
            INSERT INTO tareas (id, titulo, descripcion, id_curso, id_docente, fecha_limite, estado)
            VALUES (gen_random_uuid(), %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        ''', ('📚 Proyecto Final - Repositorio', 'Subir el sistema completo.', id_curso, id_docente, '2026-12-31 23:59:00', 'publicada'))

        # 5. MATRICULAR AL ESTUDIANTE
        cursor.execute('''
            INSERT INTO inscripciones (id_estudiante, id_curso) 
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        ''', (id_estudiante, id_curso))

        # --- CAMBIOS DE UNIFICACIÓN Y VISIBILIDAD EN TIEMPO REAL ---
        
        # 6. SINCRONIZACIÓN FORZOSA: 
        # Asegura que TODAS las tareas (antiguas y las recién creadas por el docente) 
        # tengan el ID de curso correcto y estado 'publicada'.
        cursor.execute("""
            UPDATE tareas 
            SET id_curso = %s, estado = 'publicada'
            WHERE id_docente = %s AND (id_curso != %s OR id_curso IS NULL OR estado = 'borrador')
        """, (id_curso, id_docente, id_curso))
        
        # 7. RECLAMAR TAREAS HUÉRFANAS:
        # Si hay tareas de pruebas anteriores con otros IDs de docente, las traemos al actual.
        cursor.execute("""
            UPDATE tareas 
            SET id_docente = %s, id_curso = %s, estado = 'publicada'
            WHERE id_docente != %s OR id_docente IS NULL
        """, (id_docente, id_curso, id_docente))
        
        conn.commit()
        print("✅ [OK] Tareas sincronizadas: El estudiante ahora verá lo que el docente cree.")

    except Exception as e:
        print(f"❌ Error de inyección: {e}")
        if conn: conn.rollback()
    finally:
        if 'cursor' in locals(): cursor.close()
        if conn: conn.close()
        
# Ejecución al llamar el script directamente
if __name__ == '__main__':
    crear_tablas()
    crear_tabla_inscripciones()
    crear_tabla_entregas()
    inyectar_tarea_y_matricula()