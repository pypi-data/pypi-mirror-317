import math


class Quadratic:
    """
    Класс для решения квадратных уравнений вида ax^2 + bx + c = 0.
    """

    def __init__(self, a, b, c):
        """
        Инициализация коэффициентов уравнения.
        :param a: Коэффициент при x^2
        :param b: Коэффициент при x
        :param c: Свободный член
        """
        self.a = a
        self.b = b
        self.c = c

    def calculate_discriminant(self):
        """
        Вычисляет дискриминант уравнения.
        :return: Значение дискриминанта
        """
        return self.b ** 2 - 4 * self.a * self.c

    def solve(self):
        """
        Решает уравнение на основе коэффициентов.
        :return: Кортеж с корнями уравнения или сообщение о решении
        """
        if self.a == 0:
            if self.b == 0:
                return "Нет решений" if self.c != 0 else "Бесконечно много решений"
            return f"Линейное уравнение, корень: {-self.c / self.b}"

        D = self.calculate_discriminant()

        if D > 0:
            # Два вещественных корня
            x1 = (-self.b + math.sqrt(D)) / (2 * self.a)
            x2 = (-self.b - math.sqrt(D)) / (2 * self.a)
            return x1, x2
        elif D == 0:
            # Один (двукратный) корень
            x = -self.b / (2 * self.a)
            return x,
        else:
            # Комплексные корни
            real_part = -self.b / (2 * self.a)
            imaginary_part = math.sqrt(-D) / (2 * self.a)
            return (real_part + imaginary_part * 1j, real_part - imaginary_part * 1j)