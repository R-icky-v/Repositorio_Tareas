import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

# Busca el .env desde la raíz del proyecto
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def get_conexion():
    try:
        conexion = psycopg2.connect(
            host     = os.getenv("DB_HOST"),
            port     = os.getenv("DB_PORT"),
            dbname   = os.getenv("DB_NAME"),
            user     = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD")
        )
        return conexion
    except Exception as e:
        print(f"❌ Error de conexion: {e}")
        return None
    
    