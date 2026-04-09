from database.conexion import get_conexion

conn = get_conexion()
if conn:
    print("✅ Conexión exitosa a Supabase")
    conn.close()
else:
    print("❌ No se pudo conectar")