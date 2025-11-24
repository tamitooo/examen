from dataclasses import dataclass
from typing import List

MAX_EVALUATIONS = 10
EXTRA_POINTS_VALUE = 1.0  # configurable: cuánto sumar si hay política colectiva
MIN_GRADE = 0.0
MAX_GRADE = 20.0  # ajusta según escala de tu curso (por ejemplo 20)

@dataclass
class Evaluation:
    score: float
    weight: float  # porcentaje (ej. 30 significa 30%)

    def __post_init__(self):
        if self.weight < 0 or self.weight > 100:
            raise ValueError("weight debe estar entre 0 y 100")
        if self.score < MIN_GRADE or self.score > MAX_GRADE:
            raise ValueError(f"score debe estar entre {MIN_GRADE} y {MAX_GRADE}")

class AttendancePolicy:
    """Política de asistencia.
    Si no se alcanza la asistencia mínima, la nota final será 0 (penalización total).
    Esta regla puede ajustarse si tu enunciado pide otra cosa.
    """
    def apply(self, has_reached_minimum: bool, current_grade: float) -> float:
        if not has_reached_minimum:
            return 0.0
        return current_grade

class ExtraPointsPolicy:
    """Aplica puntos extra si all_years_teachers == True."""
    def __init__(self, extra_points_value: float = EXTRA_POINTS_VALUE):
        self.extra_points_value = extra_points_value

    def apply(self, all_years_teachers: bool, current_grade: float) -> float:
        if all_years_teachers:
            return min(current_grade + self.extra_points_value, MAX_GRADE)
        return current_grade

class StudentRecord:
    def __init__(self, evaluations: List[Evaluation], has_reached_minimum_classes: bool, all_years_teachers: bool):
        if len(evaluations) > MAX_EVALUATIONS:
            raise ValueError(f"Máximo de evaluaciones es {MAX_EVALUATIONS}")
        self.evaluations = evaluations
        self.has_reached_minimum_classes = has_reached_minimum_classes
        self.all_years_teachers = all_years_teachers

class GradeCalculator:
    def __init__(self, attendance_policy: AttendancePolicy = None, extra_policy: ExtraPointsPolicy = None):
        self.attendance_policy = attendance_policy or AttendancePolicy()
        self.extra_policy = extra_policy or ExtraPointsPolicy()

    def weighted_average(self, evaluations: List[Evaluation]) -> float:
        # Validación: suma de pesos no necesita ser 100% obligatoria, pero informamos
        total_weight = sum(ev.weight for ev in evaluations)
        if total_weight == 0:
            return 0.0
        # promedio ponderado: sum(score * weight) / sum(weight)
        weighted_sum = sum(ev.score * ev.weight for ev in evaluations)
        avg = weighted_sum / total_weight
        return avg

    def calculate_final(self, record: StudentRecord) -> dict:
        # Determinista: no use de random ni tiempo
        detalle = {}
        prom_ponderado = self.weighted_average(record.evaluations)
        detalle['promedio_ponderado'] = round(prom_ponderado, 4)

        # Aplicar penalización por asistencia
        after_attendance = self.attendance_policy.apply(record.has_reached_minimum_classes, prom_ponderado)
        detalle['aplico_penalizacion_asistencia'] = not record.has_reached_minimum_classes
        detalle['nota_despues_asistencia'] = round(after_attendance, 4)

        # Aplicar puntos extra
        final_with_extra = self.extra_policy.apply(record.all_years_teachers, after_attendance)
        detalle['aplico_puntos_extra'] = record.all_years_teachers
        detalle['puntos_extra_aplicados'] = round(final_with_extra - after_attendance, 4)
        detalle['nota_final'] = round(final_with_extra, 4)

        return detalle

# CLI helper
def run_cli():
    print("=== CS-GradeCalculator (terminal) ===")
    try:
        n = int(input(f"Número de evaluaciones (0..{MAX_EVALUATIONS}): ").strip())
    except ValueError:
        print("Entrada inválida. Intenta de nuevo.")
        return

    if n < 0 or n > MAX_EVALUATIONS:
        print(f"El número de evaluaciones debe estar entre 0 y {MAX_EVALUATIONS}")
        return

    evals = []
    for i in range(n):
        try:
            sc_txt = input(f"Evaluación {i+1} - nota (0..{MAX_GRADE}): ").strip()
            wt_txt = input(f"Evaluación {i+1} - peso (%) (ej. 30): ").strip()
            score = float(sc_txt)
            weight = float(wt_txt)
            ev = Evaluation(score=score, weight=weight)
            evals.append(ev)
        except Exception as e:
            print(f"Entrada inválida para la evaluación {i+1}: {e}")
            return

    att_txt = input("¿El estudiante alcanzó la asistencia mínima? (s/n): ").strip().lower()
    has_att = att_txt in ('s', 'si', 'y', 'yes')

    extra_txt = input("¿Los docentes acordaron puntos extra este año? (s/n): ").strip().lower()
    all_years = extra_txt in ('s', 'si', 'y', 'yes')

    record = StudentRecord(evaluations=evals, has_reached_minimum_classes=has_att, all_years_teachers=all_years)
    calc = GradeCalculator()
    result = calc.calculate_final(record)

    print("\n--- Detalle del Cálculo ---")
    print(f"Promedio ponderado: {result['promedio_ponderado']}")
    print(f"Se aplicó penalización por asistencia: {result['aplico_penalizacion_asistencia']}")
    print(f"Nota después de asistencia: {result['nota_despues_asistencia']}")
    print(f"Puntos extra aplicados: {result['puntos_extra_aplicados']}")
    print(f"Nota final: {result['nota_final']}")
    print("---------------------------")

if __name__ == "__main__":
    run_cli()
