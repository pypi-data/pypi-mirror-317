# ter_ver

ter_ver_bb — это Python-библиотека для вычислений по формулам Бернулли и Байеса.

## Установка
```bash
pip install ter_ver_bb
```

## Использование
```python
from ter_ver_bb.BernoulliCalculator import Bernoulli
from ter_ver_bb.BayesCalculator import Bayes

# Пример использования
# Формула Бернулли
probability = Bernoulli.bernoulli_probability(5, 2, 0.5)
print("Вероятность по Бернулли:", probability)

# Формула Байеса
posterior = Bayes.bayes_theorem(0.01, 0.9, 0.1)
print("Результат по формуле Байеса:", posterior)
```

## Тестирование
Запустите тесты с помощью команды:
```bash
python -m unittest discover tests
```

## Зависимости
- math