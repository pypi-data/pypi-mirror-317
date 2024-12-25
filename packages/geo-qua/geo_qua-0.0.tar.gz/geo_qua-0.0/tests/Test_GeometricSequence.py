import unittest
from .GeometricSequence import Geometric


class TestGeometricSequence(unittest.TestCase):

    def test_nth_term(self):
        """Тест вычисления n-го члена последовательности"""
        sequence = Geometric(a1=2, q=3)
        self.assertEqual(sequence.nth_term(1), 2)
        self.assertEqual(sequence.nth_term(2), 6)
        self.assertEqual(sequence.nth_term(3), 18)
        self.assertEqual(sequence.nth_term(5), 162)

    def test_sum_of_terms(self):
        """Тест вычисления суммы первых n членов"""
        sequence = Geometric(a1=2, q=3)
        self.assertAlmostEqual(sequence.sum_of_terms(1), 2)
        self.assertAlmostEqual(sequence.sum_of_terms(2), 8)
        self.assertAlmostEqual(sequence.sum_of_terms(3), 26)
        self.assertAlmostEqual(sequence.sum_of_terms(5), 242)

    def test_sum_of_terms_q_equals_1(self):
        """Тест суммы для последовательности, где q = 1"""
        sequence = Geometric(a1=5, q=1)
        self.assertEqual(sequence.sum_of_terms(3), 15)
        self.assertEqual(sequence.sum_of_terms(10), 50)

    def test_is_member(self):
        """Тест проверки принадлежности числа последовательности"""
        sequence = Geometric(a1=2, q=3)
        self.assertTrue(sequence.is_member(2))    # Первый член
        self.assertTrue(sequence.is_member(6))    # Второй член
        self.assertTrue(sequence.is_member(162))  # Пятый член
        self.assertFalse(sequence.is_member(50))  # Не принадлежит

    def test_invalid_n_for_nth_term(self):
        """Тест исключения для n < 1 при вычислении n-го члена"""
        sequence = Geometric(a1=2, q=3)
        with self.assertRaises(ValueError):
            sequence.nth_term(0)
        with self.assertRaises(ValueError):
            sequence.nth_term(-1)

    def test_invalid_n_for_sum_of_terms(self):
        """Тест исключения для n < 1 при вычислении суммы"""
        sequence = Geometric(a1=2, q=3)
        with self.assertRaises(ValueError):
            sequence.sum_of_terms(0)
        with self.assertRaises(ValueError):
            sequence.sum_of_terms(-1)

    def test_zero_denominator(self):
        """Тест исключения при q = 0"""
        with self.assertRaises(ValueError):
            Geometric(a1=2, q=0)

    def test_is_member_invalid_cases(self):
        """Тест проверки на принадлежность для отрицательных и нулевых значений"""
        sequence = Geometric(a1=2, q=3)
        self.assertFalse(sequence.is_member(-6))  # Отрицательное число
        self.assertFalse(sequence.is_member(0))   # Ноль не может быть членом последовательности


if __name__ == "__main__":
    unittest.main()
