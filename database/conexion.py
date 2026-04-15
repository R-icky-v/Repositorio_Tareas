import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

# --- CAMBIO PARA EJECUTABLE ---
# Si el programa corre como un .exe (frozen), usa la ruta del ejecutable
if getattr(sys, 'frozen', False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent.parent

env_path = base_path / '.env'
load_dotenv(dotenv_path=env_path)

def get_conexion():
    try:
        # CONEXIÓN BLINDADA: Datos directos para evitar fallos del .env en el .exe
        conexion = psycopg2.connect(
            host     = "db.kfctnpmhoqgoqyvenzby.supabase.co",
            port     = "5432",
            dbname   = "postgres",
            user     = "postgres",
            password = "repositorio_tareas",
            connect_timeout = 10  # Tiempo de espera extendido para datos móviles
        )
        return conexion
    except Exception as e:
        print(f"❌ Error crítico de conexión: {e}")
        return None
    
