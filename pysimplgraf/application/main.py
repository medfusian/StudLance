import sys
from fractions import Fraction

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import numpy as np


class SimplexSolver:
    def __init__(self, A, b, c):
        self.A = np.array(A)
        self.b = np.array(b)
        self.c = np.array(c)
        self.m, self.n = self.A.shape
        self.N = set(range(self.n))
        self.B = set(range(self.n, self.n + self.m))

    def simplex(self):
        while True:
            # Сначала находим опорное решение методом искусственного базиса
            x = np.zeros(self.n + self.m)
            B = set()
            for i in range(self.m):
                e = np.zeros(self.m)
                e[i] = 1
                j = self.n + i
                x[j] = self.b[i]
                B.add(j)
                self.A = np.column_stack((self.A, e))
                self.N.discard(j)
            c = np.zeros(self.n + self.m)
            c[list(self.N)] = self.c[list(self.N)]
            self.c = c

            # Симплекс-метод
            while True:
                # Вычисляем оценки
                cb = self.c[list(B)]
                cn = self.c[list(self.N)]
                B_inv = np.linalg.inv(self.A[:, list(B)])
                xB = B_inv @ self.b
                delta = cn - cb @ B_inv @ self.A[:, list(self.N)]

                # Проверяем, является ли текущее решение оптимальным
                if all(delta <= 0):
                    x[list(B)] = xB
                    self.optimal = True
                    break

                # Находим разрешающий столбец
                j = list(self.N)[np.argmin(delta)]

                # Проверяем, является ли задача неограниченной
                if all(self.A[:, j] <= 0):
                    self.unbounded = True
                    break

                # Находим разрешающую строку
                i = np.argmin(xB / self.A[:, j])

                # Обновляем базис
                B.discard(list(B)[i])
                B.add(j)

            if self.optimal or self.unbounded:
                break

        return x[:self.n]


class ConditionTab(QWidget):
    def __init__(self):
        super().__init__()

        def solve(self):
            # получаем значения из таблицы
            matrix = []
            for i in range(self.table.rowCount()):
                row = []
                for j in range(self.table.columnCount()):
                    item = self.table.item(i, j)
                    if item is not None:
                        value = item.text()
                        try:
                            value = float(value)
                        except ValueError:
                            value = None
                        row.append(value)
                matrix.append(row)

            # создаем объект LinearProgrammingSolver и решаем задачу
            solver = LinearProgrammingSolver(matrix)
            solution = solver.solve()

            # выводим результаты решения
            # ...

        # Создаем виджеты для выбора количества переменных и ограничений
        self.var_label = QLabel("Количество переменных:")
        self.var_spinbox = QSpinBox()
        self.var_spinbox.setRange(1, 16)
        self.var_spinbox.setValue(2)

        self.const_label = QLabel("Количество ограничений:")
        self.const_spinbox = QSpinBox()
        self.const_spinbox.setRange(1, 16)
        self.const_spinbox.setValue(2)

        # Создаем виджеты для выбора метода решения
        self.method_label = QLabel("Метод решения:")
        self.method_combobox = QComboBox()
        self.method_combobox.addItems(["Симплекс метод", "Графический метод"])

        # Создаем виджеты для выбора задачи оптимизации
        self.optimization_label = QLabel("Задача оптимизации:")
        self.maximize_radio = QRadioButton("Максимизация")
        self.minimize_radio = QRadioButton("Минимизация")
        self.maximize_radio.setChecked(True)

        # Создаем виджеты для выбора вида дробей
        self.fraction_label = QLabel("Вид дробей:")
        self.fraction_combobox = QComboBox()
        self.fraction_combobox.addItems(["Обыкновенные дроби", "Десятичные дроби"])

        # Создаем виджеты для выбора базиса
        self.basis_label = QLabel("Базис:")
        self.basis_combobox = QComboBox()

        # Размещаем виджеты на форме
        layout = QGridLayout()
        layout.addWidget(self.var_label, 0, 0)
        layout.addWidget(self.var_spinbox, 0, 1)
        layout.addWidget(self.const_label, 1, 0)
        layout.addWidget(self.const_spinbox, 1, 1)
        layout.addWidget(self.method_label, 2, 0)
        layout.addWidget(self.method_combobox, 2, 1)
        layout.addWidget(self.optimization_label, 3, 0)
        layout.addWidget(self.maximize_radio, 3, 1)
        layout.addWidget(self.minimize_radio, 3, 2)
        layout.addWidget(self.fraction_label, 4, 0)
        layout.addWidget(self.fraction_combobox, 4, 1)
        layout.addWidget(self.basis_label, 5, 0)
        layout.addWidget(self.basis_combobox, 5, 1)
        self.setLayout(layout)

        # добавляем виджет QTableWidget
        self.table = QTableWidget()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)

        # добавляем кнопку "Решить"
        self.solve_button = QPushButton("Решить")

        # добавляем обработчик клика на кнопку
        self.solve_button.clicked.connect(self.solve)

        # создаем layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.solve_button)

        # устанавливаем layout для вкладки
        self.setLayout(layout)



class ArtificialBasisTab(QWidget):
    def __init__(self):
        super().__init__()
        # добавьте виджет вывода таблиц для метода искусственного базиса


class SimplexTab(QWidget):
    def __init__(self):
        super().__init__()

        # Создаем поля ввода матрицы коэффициентов и вектора правых частей
        self.matrix_edit = QTextEdit()
        self.rhs_edit = QTextEdit()

        # Создаем кнопку для запуска решения симплекс методом
        self.solve_btn = QPushButton("Решить")

        # Создаем окно вывода решения
        self.solution_edit = QTextEdit()
        self.solution_edit.setReadOnly(True)

        # Связываем кнопку с функцией для решения задачи
        self.solve_btn.clicked.connect(self.solve)

        # Создаем вертикальный контейнер и добавляем все элементы в него
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Матрица коэффициентов"))
        layout.addWidget(self.matrix_edit)
        layout.addWidget(QLabel("Вектор правых частей"))
        layout.addWidget(self.rhs_edit)
        layout.addWidget(self.solve_btn)
        layout.addWidget(QLabel("Решение"))
        layout.addWidget(self.solution_edit)
        self.setLayout(layout)

    def solve(self):
        # Получаем матрицу коэффициентов из поля ввода
        matrix_str = self.matrix_edit.toPlainText()
        matrix_rows = matrix_str.strip().split("\n")
        matrix = []
        for row_str in matrix_rows:
            row = [Fraction(x.strip()) for x in row_str.strip().split()]
            matrix.append(row)

        # Получаем вектор правых частей из поля ввода
        rhs_str = self.rhs_edit.toPlainText()
        rhs = [Fraction(x.strip()) for x in rhs_str.strip().split()]

        # Создаем объект LinearProgrammingSolver и решаем задачу симплекс методом
        solver = SimplexSolver(matrix, rhs)
        success, message = solver.simplex_method()
        if success:
            # Выводим найденное оптимальное решение
            self.solution_edit.setText("Оптимальное решение: " + str(solver.objective_value) + "\n")

            # Выводим найденные значения переменных
            for i, x in enumerate(solver.basic_variables):
                self.solution_edit.append("x{} = {}".format(x + 1, solver.basic_variable_values[i]))
        else:
            # Выводим сообщение об ошибке, если решение не найдено
            self.solution_edit.setText("Ошибка: " + message)


class MainTab(QWidget):
    def __init__(self):
        super().__init__()

        # Create tabs
        self.tabs = QTabWidget()
        self.condition_tab = ConditionTab()
        self.artificial_basis_tab = ArtificialBasisTab()
        self.simplex_tab = SimplexTab()
        # self.graphic_tab = GraphicTab()

        # Add tabs
        self.tabs.addTab(self.condition_tab, "Условие задачи")
        self.tabs.addTab(self.artificial_basis_tab, "Метод искусственного базиса")
        self.tabs.addTab(self.simplex_tab, "Симплекс метод")
        # self.tabs.addTab(self.graphic_tab, "Графический метод")

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)

        # Set layout
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainTab()
    ex.show()
    sys.exit(app.exec_())
