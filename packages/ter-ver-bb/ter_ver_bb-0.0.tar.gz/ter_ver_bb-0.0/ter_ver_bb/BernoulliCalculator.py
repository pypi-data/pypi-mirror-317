import math


class Bernoulli:
    @staticmethod
    def bernoulli_probability(n, k, p):
        """
        Вычисление вероятности по формуле Бернулли.
        :param n: Количество испытаний
        :param k: Количество успехов
        :param p: Вероятность успеха
        :return: Вероятность ровно k успехов
        """
        coefficient = math.comb(n, k)
        return coefficient * (p ** k) * ((1 - p) ** (n - k))