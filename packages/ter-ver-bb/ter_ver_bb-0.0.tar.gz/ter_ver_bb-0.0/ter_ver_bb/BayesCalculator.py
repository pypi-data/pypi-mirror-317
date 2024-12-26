class Bayes:
    @staticmethod
    def bayes_theorem(prior, likelihood, marginal):
        """
        Применение теоремы Байеса.
        :param prior: Априорная вероятность (P(A))
        :param likelihood: Условная вероятность (P(B|A))
        :param marginal: Маргинальная вероятность (P(B))
        :return: Результат применения теоремы Байеса (P(A|B))
        """
        return (prior * likelihood) / marginal