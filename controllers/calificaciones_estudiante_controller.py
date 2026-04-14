class CalificacionesEstudianteController:
    @staticmethod
    def obtener_resumen_notas(id_estudiante):
        # 1. Traer datos de la BD
        from database.tarea_queries import obtener_calificaciones_estudiante
        notas_raw = obtener_calificaciones_estudiante(id_estudiante)
        
        if not notas_raw:
            return [], 0.0

        # 2. Calcular promedio (T-05.2)
        total_puntos = sum(n[1] for n in notas_raw)
        promedio = total_puntos / len(notas_raw)
        
        return notas_raw, round(promedio, 2)