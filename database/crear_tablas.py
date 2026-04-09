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