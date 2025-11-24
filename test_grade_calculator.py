import unittest
import io
from unittest.mock import patch
from grades import Evaluation, StudentRecord, GradeCalculator, AttendancePolicy, ExtraPointsPolicy, run_cli

class TestGradeCalculator(unittest.TestCase):
    def test_normal_calculation(self):
        evs = [Evaluation(14, 50), Evaluation(16, 50)]
        record = StudentRecord(evs, has_reached_minimum_classes=True, all_years_teachers=False)
        calc = GradeCalculator()
        res = calc.calculate_final(record)
        self.assertAlmostEqual(res['promedio_ponderado'], 15.0)
        self.assertFalse(res['aplico_penalizacion_asistencia'])
        self.assertEqual(res['puntos_extra_aplicados'], 0.0)
        self.assertAlmostEqual(res['nota_final'], 15.0)

    def test_no_attendance_penalty(self):
        evs = [Evaluation(12, 100)]
        record = StudentRecord(evs, has_reached_minimum_classes=False, all_years_teachers=False)
        calc = GradeCalculator()
        res = calc.calculate_final(record)
        self.assertEqual(res['nota_final'], 0.0)

    def test_extra_points_applied(self):
        evs = [Evaluation(13.5, 100)]
        record = StudentRecord(evs, has_reached_minimum_classes=True, all_years_teachers=True)
        calc = GradeCalculator()
        res = calc.calculate_final(record)
        self.assertAlmostEqual(res['promedio_ponderado'], 13.5)
        self.assertAlmostEqual(res['puntos_extra_aplicados'], 1.0)
        self.assertAlmostEqual(res['nota_final'], 14.5)

    def test_zero_evaluations(self):
        evs = []
        record = StudentRecord(evs, has_reached_minimum_classes=True, all_years_teachers=False)
        calc = GradeCalculator()
        res = calc.calculate_final(record)
        self.assertEqual(res['promedio_ponderado'], 0.0)
        self.assertEqual(res['nota_final'], 0.0)

    def test_invalid_weights_or_scores(self):
        with self.assertRaises(ValueError):
            Evaluation(-1, 50)
        with self.assertRaises(ValueError):
            Evaluation(10, -5)
        with self.assertRaises(ValueError):
            # más de MAX_EVALUATIONS
            evs = [Evaluation(10,10)] * 11
            StudentRecord(evs, True, False)

    def test_score_at_bounds_and_extra_caps(self):
        # score at minimum bound
        evs_min = [Evaluation(0.0, 100)]
        record_min = StudentRecord(evs_min, has_reached_minimum_classes=True, all_years_teachers=False)
        calc = GradeCalculator()
        res_min = calc.calculate_final(record_min)
        self.assertEqual(res_min['promedio_ponderado'], 0.0)
        self.assertEqual(res_min['nota_final'], 0.0)

        # score at maximum bound and extra points should be capped at MAX_GRADE
        evs_max = [Evaluation(20.0, 100)]
        record_max = StudentRecord(evs_max, has_reached_minimum_classes=True, all_years_teachers=True)
        res_max = calc.calculate_final(record_max)
        self.assertAlmostEqual(res_max['promedio_ponderado'], 20.0)
        # extra points applied should not increase above 20.0
        self.assertAlmostEqual(res_max['nota_final'], 20.0)

    def test_weight_greater_than_100_raises(self):
        with self.assertRaises(ValueError):
            Evaluation(10.0, 150.0)

    def test_extra_points_caps_at_max_grade(self):
        # Ensure extra points do not push grade above MAX_GRADE
        evs = [Evaluation(19.5, 100)]
        record = StudentRecord(evs, has_reached_minimum_classes=True, all_years_teachers=True)
        calc = GradeCalculator()
        res = calc.calculate_final(record)
        # punto extra = 1.0 por defecto -> 19.5 + 1.0 = 20.5 -> capped to 20.0
        self.assertAlmostEqual(res['nota_final'], 20.0)

    def test_run_cli_invalid_number(self):
        # Simulate non-integer input for number of evaluations
        user_inputs = ['abc']
        with patch('builtins.input', side_effect=user_inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            run_cli()
            output = fake_out.getvalue()
            self.assertIn('Entrada inválida', output)

    def test_run_cli_invalid_evaluation_input(self):
        # Simulate n=1 and invalid score input
        user_inputs = ['1', 'not_a_number', '30']
        with patch('builtins.input', side_effect=user_inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            run_cli()
            output = fake_out.getvalue()
            self.assertIn('Entrada inválida para la evaluación 1', output)

    def test_run_cli_valid_flow(self):
        # Simulate a full valid run: 1 evaluation, score 15, weight 100, attended, no extra
        user_inputs = ['1', '15', '100', 's', 'n']
        with patch('builtins.input', side_effect=user_inputs), patch('sys.stdout', new=io.StringIO()) as fake_out:
            run_cli()
            output = fake_out.getvalue()
            self.assertIn('Promedio ponderado: 15.0', output)
            self.assertIn('Nota final: 15.0', output)

if __name__ == "__main__":
    unittest.main()
