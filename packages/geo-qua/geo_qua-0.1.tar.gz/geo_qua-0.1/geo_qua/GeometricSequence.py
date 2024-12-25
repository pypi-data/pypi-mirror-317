import math


class Geometric:
    """
    Класс для работы с геометрической последовательностью.
    Геометрическая последовательность определяется первым членом a1 и знаменателем q.
    """
    def __init__(self, a1, q):
        """
        Инициализация геометрической последовательности.
        :param a1: Первый член последовательности
        :param q: Знаменатель последовательности
        """
        if q == 0:
            raise ValueError("Знаменатель q не может быть равен 0")
        self.a1 = a1
        self.q = q

    def nth_term(self, n):
        """
        Вычисляет n-й член последовательности.
        :param n: Номер члена (n >= 1)
        :return: Значение n-го члена
        """
        if n < 1:
            raise ValueError("Номер члена должен быть >= 1")
        return self.a1 * (self.q ** (n - 1))

    def sum_of_terms(self, n):
        """
        Вычисляет сумму первых n членов последовательности.
        :param n: Количество членов (n >= 1)
        :return: Сумма первых n членов
        """
        if n < 1:
            raise ValueError("Количество членов должно быть >= 1")
        if self.q == 1:
            # Если q = 1, все члены равны a1
            return self.a1 * n
        return self.a1 * (1 - self.q ** n) / (1 - self.q)

    def is_member(self, x):
        """
        Проверяет, принадлежит ли число последовательности.
        :param x: Число, которое нужно проверить
        :return: True, если принадлежит, иначе False
        """
        if x == 0:
            return self.a1 == 0  # Если первый член 0, тогда 0 принадлежит последовательности
        # Проверка на принадлежность через логарифмы: x = a1 * q^k
        ratio = x / self.a1
        if ratio <= 0:
            return False
        k = math.log(ratio, self.q)
        return k.is_integer()