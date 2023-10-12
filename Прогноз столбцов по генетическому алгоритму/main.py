import pandas as pd
from deap import algorithms, base, creator, tools
import random
import numpy as np

# Загрузка данных из файла
housing = pd.read_csv("housing.csv")

# Создание целевой функции, которая вычисляет ошибку прогноза
def eval_prediction(individual):
    # Преобразование генов в список столбцов
    cols = [housing.columns[i] for i, gene in enumerate(individual) if gene]
    # Выбор данных только из выбранных столбцов
    data = housing[cols]
    # Создание модели прогнозирования и вычисление ошибки
    model = ... # Здесь следует использовать модель прогнозирования, подходящую для задачи
    error = ... # Здесь следует вычислить ошибку прогноза
    return error,

# Создание класса для описания генома
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Инициализация объектов инструментов генетического алгоритма
toolbox = base.Toolbox()

# Определение функции для генерации случайных генов
toolbox.register("attr_bool", random.randint, 0, 1)

# Определение функции для генерации особей
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, len(housing.columns))

# Определение функции для генерации популяции
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Определение функции оценки приспособленности
toolbox.register("evaluate", eval_prediction)

# Определение функции скрещивания
toolbox.register("mate", tools.cxTwoPoint)

# Определение функции мутации
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# Определение функции выбора
toolbox.register("select", tools.selTournament, tournsize=3)

# Создание начальной популяции
population = toolbox.population(n=100)

# Запуск генетического алгоритма
NGEN = 50
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    # Выбор новой популяции из потомков и родителей
    population = toolbox.select(offspring, k=len(population))

    # Выбор лучшей особи
    best_individual = tools.selBest(population, k=1)[0]

    # Преобразование генов в список столбцов
    best_cols = [housing.columns[i] for i, gene in enumerate(best_individual) if gene]

    # Выбор данных только из лучших столбцов
    best_data = housing[best_cols]

    # Обучение модели на лучших данных
    best_model = ...  # Здесь следует использовать модель прогнозирования, подходящую для задачи
    best_model.fit(best_data, housing["MEDV"])

    # Прогнозирование столбца "MEDV" на тестовых данных
    test = ...  # Здесь следует загрузить тестовые данные, если они имеются
    test_cols = ...  # Здесь следует выбрать те же столбцы, что и для лучшей особи
    test_data = test[test_cols]
    predictions = best_model.predict(test_data)

    # Вывод результатов
    print("Best columns:", best_cols)
    print("Predictions:", predictions)
