import unittest
from .QuadraticSolver import Quadratic


class TestQuadratic(unittest.TestCase):

    def test_two_real_roots(self):
        """Тест уравнения с двумя вещественными корнями: x^2 - 3x + 2 = 0"""
        solver = Quadratic(1, -3, 2)
        roots = solver.solve()
        self.assertAlmostEqual(roots[0], 2.0)
        self.assertAlmostEqual(roots[1], 1.0)

    def test_one_real_root(self):
        """Тест уравнения с одним вещественным корнем: x^2 + 2x + 1 = 0"""
        solver = Quadratic(1, 2, 1)
        roots = solver.solve()
        self.assertAlmostEqual(roots[0], -1.0)

    def test_complex_roots(self):
        """Тест уравнения с комплексными корнями: x^2 + x + 1 = 0"""
        solver = Quadratic(1, 1, 1)
        roots = solver.solve()
        self.assertAlmostEqual(roots[0].real, -0.5)
        self.assertAlmostEqual(roots[0].imag, 0.8660254037844386)
        self.assertAlmostEqual(roots[1].real, -0.5)
        self.assertAlmostEqual(roots[1].imag, -0.8660254037844386)

    def test_linear_equation(self):
        """Тест линейного уравнения: 2x - 4 = 0"""
        solver = Quadratic(0, 2, -4)
        result = solver.solve()
        self.assertEqual(result, "Линейное уравнение, корень: 2.0")

    def test_no_solution(self):
        """Тест уравнения без решений: 0x + 0 = 5"""
        solver = Quadratic(0, 0, 5)
        result = solver.solve()
        self.assertEqual(result, "Нет решений")

    def test_infinite_solutions(self):
        """Тест уравнения с бесконечным числом решений: 0x + 0 = 0"""
        solver = Quadratic(0, 0, 0)
        result = solver.solve()
        self.assertEqual(result, "Бесконечно много решений")

    def test_discriminant_calculation(self):
        """Тест вычисления дискриминанта"""
        solver = Quadratic(1, -3, 2)
        discriminant = solver.calculate_discriminant()
        self.assertEqual(discriminant, 1)

    def test_negative_discriminant(self):
        """Тест дискриминанта для уравнения с комплексными корнями"""
        solver = Quadratic(1, 1, 1)
        discriminant = solver.calculate_discriminant()
        self.assertEqual(discriminant, -3)


if __name__ == "__main__":
    unittest.main()
