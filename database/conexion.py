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
        # Validación de seguridad: Si no hay HOST, el .env no cargó
        db_host = os.getenv("DB_HOST")
        if not db_host:
            print("❌ Error: No se encontraron las variables en el archivo .env")
            return None

        conexion = psycopg2.connect(
            host     = db_host,
            port     = os.getenv("DB_PORT"),
            dbname   = os.getenv("DB_NAME"),
            user     = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")
        )
        return conexion
    except Exception as e:
        print(f"❌ Error de conexion: {e}")
        return None