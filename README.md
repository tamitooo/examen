# Examen - Grade Calculator (Python backend)

Proyecto simple con arquitectura orientada a objetos para el cálculo de notas.

Características principales
- Evaluaciones con peso (máx 10) validadas.
- Políticas separadas: asistencia y puntos extra, inyectables en el calculador.
- `GradeCalculator.calculate_final()` devuelve un detalle con promedio ponderado, penalizaciones y puntos extra.
- CLI mínimo incluido en `grade_calculator.py` (función `run_cli()`).

Cumplimiento de criterios del examen

- RF01 — Registro de evaluaciones y pesos: Implementado en `Evaluation` y validado en `StudentRecord` (máx 10).
- RF02 — `has_reached_minimum_classes`: Implementado en `StudentRecord` y usado por `AttendancePolicy`.
- RF03 — `all_years_teachers`: Implementado en `StudentRecord` y usado por `ExtraPointsPolicy`.
- RF04 — `GradeCalculator.calculate_final()`: Realiza el flujo completo, devuelve campo `detalle` con valores intermedios.
- RF05 — CLI: `run_cli()` imprime detalle con promedio ponderado, penalización, puntos extra y nota final.

- RNF01 — Límite máximo 10 evaluaciones validado.
- RNF02 — Diseño sin estado global, OO — soporta concurrencia lógica.
- RNF03 — Determinista: no hay fuentes de aleatoriedad ni uso de tiempo.
- RNF04 — Complejidad O(n) en número de evaluaciones, muy rápido en práctica.

Cómo usar

Desde la carpeta `examen` puedes ejecutar los tests con:

```powershell
python -m unittest discover -v
```

O ejecutar el CLI:

```powershell
python grade_calculator.py
```
