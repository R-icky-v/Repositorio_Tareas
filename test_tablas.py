import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from database.conexion import get_conexion

conn = get_conexion()
cursor = conn.cursor()

# Verifica cursos
cursor.execute("SELECT * FROM cursos")
cursos = cursor.fetchall()
print(f"✅ Tabla cursos — {len(cursos)} registros: {cursos}")

# Verifica usuarios
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()
print(f"✅ Tabla usuarios — {len(usuarios)} registros: {usuarios}")

# Verifica tareas
cursor.execute("SELECT * FROM tareas")
tareas = cursor.fetchall()
print(f"✅ Tabla tareas — {len(tareas)} registros: {tareas}")

cursor.close()
conn.close()


#aaaa