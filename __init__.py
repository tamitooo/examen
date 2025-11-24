"""Paquete `examen` — Calculadora de notas

Se ofrece una arquitectura simple, orientada a objetos, sin estado global y con alta cohesión.

Exporta las clases principales usadas en los tests y en la CLI:
- Evaluation
- StudentRecord
- GradeCalculator
- AttendancePolicy
- ExtraPointsPolicy

Diseño:
- OO: cada política es una clase con método `apply` (injection por constructor en `GradeCalculator`).
- Sin estado global: todas las configuraciones pasan por instancias y constantes locales.
- Determinista y O(n) en número de evaluaciones.

Cumplimiento de criterios del examen (resumen):
- RF01: Registro de evaluaciones y pesos validado en `StudentRecord` y `Evaluation` (máx 10).
- RF02: `has_reached_minimum_classes` es parte de `StudentRecord` y usado por `AttendancePolicy`.
- RF03: `all_years_teachers` es parte de `StudentRecord` y usado por `ExtraPointsPolicy`.
- RF04: `GradeCalculator.calculate_final()` ejecuta el flujo completo y devuelve detalle.
- RF05: El módulo `grade_calculator.py` incluye un `run_cli()` para ejecutar desde terminal.

RNFs:
- RNF01: Límite máximo de evaluaciones validado en `StudentRecord` (constante `MAX_EVALUATIONS`).
- RNF02: Diseño sin estado global y OO — apto para concurrencia lógica.
- RNF03: Cálculo determinista — no usa random ni tiempo.
- RNF04: Cálculo O(n) simple y rápido (n = número de evaluaciones).

"""
from .grades import (
    Evaluation,
    StudentRecord,
    GradeCalculator,
    AttendancePolicy,
    ExtraPointsPolicy,
)

__all__ = [
    "Evaluation",
    "StudentRecord",
    "GradeCalculator",
    "AttendancePolicy",
    "ExtraPointsPolicy",
]
