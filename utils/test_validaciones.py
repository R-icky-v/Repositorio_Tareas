from validaciones import validar_tarea

# Caso 1: todo mal
errores = validar_tarea("", "2020-01-01", "archivo.exe")
print("Caso 1:", errores)

# Caso 2: título bien, fecha mal
errores = validar_tarea("Tarea 1", "2020-01-01", "archivo.pdf")
print("Caso 2:", errores)

# Caso 3: todo bien
errores = validar_tarea("Tarea 1", "2030-01-01", "archivo.pdf")
print("Caso 3:", errores)