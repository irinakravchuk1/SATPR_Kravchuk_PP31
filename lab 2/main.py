# coding: utf8
import sys
from fractions import Fraction

# тип матриці
from typing import List, Any

Matrix = tuple[tuple[float]]

# середнє значення індексу узгодженості
Icc = (0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)

# знайти нормований вектор пріоритетів
def calcul_norm_prior_vector(matrix : Matrix) -> list[float]:
    if len(matrix) != len(matrix[0]):
        raise Exception("Кількість рядків і стовпців у матриці має бути однаковою!")

    matr_size = len(matrix)
    norm_prior_vector = []

    # знаходимо вектор середніх геометричних в кожному рядку матриці
    for row in matrix:
        value = 1
        for elem in row:
            value *= elem
        norm_prior_vector.append(pow(value, 1.0 / matr_size))

    # обчислення вектора нормованих пріорітетностей
    vector_sum = sum(norm_prior_vector)

    for i in range(matr_size):
        norm_prior_vector[i] = norm_prior_vector[i] / vector_sum
    return norm_prior_vector

# знайти вектор із сумами стовпців матриці
def calcul_col_sums_vector(matrix : Matrix) -> list[float]:
    rows = len(matrix)
    columns = len(matrix[0])

    sums = []
    for i in range(rows):
        sum = 0
        for j in range(columns):
            sum += matrix[j][i]
        sums.append(sum)
    return sums

# обчислити власне значення матриці (лямбда), Ic - індекс узгодженості, OC - відношення узгодженості
def calcul_lambda_ic_oc(sums : tuple[float], norm_prior_vector : tuple[float]) -> (float, float, float):
    if len(sums) != len(norm_prior_vector):
        raise Exception("Кількість сум стовпців має бути такою ж, як і кількість нормованих пріоритетів")

    lambda_val = 0
    number_of_priorities = len(sums)

    for i in range(number_of_priorities):
        lambda_val += sums[i] * norm_prior_vector[i]

    Ic = (lambda_val - number_of_priorities) / (number_of_priorities - 1)
    OC = Ic / Icc[number_of_priorities - 1]

    return lambda_val, Ic, OC

# транспонування матриці
def transpose_matrix(matrix : Matrix) -> list[list[float]]:
    new_matr = []
    rows = len(matrix)
    columns = len(matrix[0])

    for i in range(columns):
        new_matr.append([])
        for j in range(rows):
            new_matr[i].append(matrix[j][i])
    return new_matr

# множення матриці на вектор-стовпець
def matrix_vector_product(matrix : Matrix, vector : tuple[float]) -> list[float]:

    if len(matrix[0]) != len(vector):
        raise Exception("Кількість стовпців у першій матриці має дорівнювати кількості рядків в другій матриці!")
    rows = len(matrix)
    columns = 1
    elem_count = len(matrix[0])

    res_vector = []

    for i in range(rows):
        value = 0
        for h in range(elem_count):
            value += matrix[i][h] * vector[h]
        res_vector.append(value)
    return res_vector

# введення матриці попарних порівнянь (критеріїв/альтернатив) з клавіатури
def input_matr(matr_size : int) -> list[list[float]]:
    while True:
        matr = []

        for i in range(matr_size):
            while True:
                try:
                    row = [float(Fraction(j)) for j in input(str(i + 1) + ": ").split(' ', matr_size - 1)]

                    if len(row) != matr_size:
                        raise Exception("Введено некоректну кількість елементів у рядку матриці!")
                except Exception as e:
                    print(e)
                else:
                    matr.append(row)
                    break

        try:
            for i in range(matr_size):
                for j in range(matr_size):
                    if matr[i][j] <= 0 or matr[i][j] > 9:
                        raise Exception("Усі елементи матриці мають бути в межах від 0 не включно до 9 включно!")
                    if i == j and matr[i][j] != 1:
                        raise Exception("Діагональні елементи матриці мають бути одиницями!")
                    if matr[i][j] != 1.0 / matr[j][i]:
                        raise Exception("Введено некоректні значення елементів")
        except Exception as e:
            print(e)
        else:
            return matr

# введення одновимірного масиву з клавіатури
def input_vector(length : int) -> list[float]:

    while True:
        try:
            vect = [float(j) for j in input("Вектор: ").split(' ', length - 1)]

            if len(vect) != length:
                raise Exception("Введено некоректну кількість елементів у векторі!")
        except Exception as e:
            print(e)
        else:
            return vect

# введення цілого числа в проміжку
def input_int_in_range(min_val : int, max_val : int) -> int:
    while True:
        try:
            value = int(input(f"Введіть ціле число від {min_val} до {max_val} включно: "))

            if value < min_val or value > max_val:
                print("Введіть коректне число!")
                continue

        except Exception as e:
            print(e)
        else:
            return value

def main():
    while True:
        print("\nВведіть один із варіантів:")
        print("--- 0 - щоб завершити роботу")
        print("--- 1 - щоб здійснити експертну оцінку задачі методом ієрархій Саті\n")
        choice = input_int_in_range(0, 1)

        if choice == 0:
            sys.exit(0)
        elif choice == 1:

            print("\nВведіть кількість альтернатив у задачі (рядків у матриці):")
            alternatives_number = input_int_in_range(0, sys.maxsize)

            print("\nВведіть кількість критеріїв у задачі (стовпців у матриці):")
            criteria_number = input_int_in_range(0, len(Icc) - 1)

            print("\nВведіть матрицю попарних порівнянь для критеріїв:")
            print("--Елементи у кожному рядку вводьте через пробіл, для переходу на наступну стрічку вводьте Enter")
            print("--Вводьте дані так, щоб для значення пріоритета на i-тому рядку і на j-тому стовпці")
            print("  значення пріоритета на j-тому рядку та і-тому стовпці було оберненим, наприклад якщо a[i][j] = 5,")
            print("  то a[j][i] = 1/5 - значення можна вводити дробом.")
            print("--Значення елементів на діагоналі матриці, де i==j мають бути лише 1, наприклад a[0][0] = 1")
            print("--Усі значення мають бути не більшими ніж 9!")
            criteria_prior_matrix = input_matr(criteria_number)

            print("\nВведіть матриці попарних порівнянь альтернатив (пріоритетності) за кожним критерієм:")
            print("Для вводу кожної матриці використовуйте попередні правила для критеріїв!")
            alternatives_matrices = []
            for i in range(criteria_number):
                print(f"\nКритерій {i + 1}:")
                matrix = input_matr(alternatives_number)
                alternatives_matrices.append(matrix)

            print("\nВиконаємо необхідні обчислення...")

            # обчислимо нормалізований вектор пріоритетів критеріїв
            norm_criteria_priorities = calcul_norm_prior_vector(tuple(tuple(row) for row in criteria_prior_matrix))

            # обчислимо суми стовпців матриці попарних порівнянь критеріїв
            criteria_col_sums = calcul_col_sums_vector(tuple(tuple(row) for row in criteria_prior_matrix))

            # обчислимо власне значення матриці(лямбда), індекс узгодженості і відношення узгодженості
            criteria_info = calcul_lambda_ic_oc(tuple(criteria_col_sums), tuple(norm_criteria_priorities))

            # обчислимо пріоритети альтернатив за кожним критерієм
            alternatives_priorities = []
            for matrix in alternatives_matrices:
                prior_vector = calcul_norm_prior_vector(tuple(tuple(row) for row in matrix))
                alternatives_priorities.append(prior_vector)

            # транспонуємо матрицю пріоритетів альтернатив
            alternatives_priorities = transpose_matrix(tuple(tuple(row) for row in alternatives_priorities))

            # знаходимо вектор глобальних пріоритетів альтернатив
            global_alternatives_priorities = matrix_vector_product(tuple(tuple(row) for row in alternatives_priorities), tuple(norm_criteria_priorities))

            # виведемо результати
            print("\nМаємо такі нормалізовані пріоритети критеріїв:")
            for i in range(criteria_number):
                print(f"Критерій {i + 1}: {norm_criteria_priorities[i]}")

            print("\nВизначимо узгодженість думок експертів:")
            for i in range(len(criteria_info)):
                if i == 0:
                    print(f"Власне значення матриці попарних порівнянь критеріїв (лямбда) = {criteria_info[i]}")
                elif i == 1:
                    print(f"Індекс узгодженості (Ic) = {criteria_info[i]}")
                else:
                    print(f"Відносна узгодженість (OC) = {criteria_info[i]}")

            if criteria_info[1] < 0.2 and criteria_info[2] < 0.1:
                print("\nОскільки значення індексу узгодженості менше 0.2 і значення відносної узгодженості менше 0.1,")
                print("то мжна вважати, що думка експертів узгоджена")
            elif criteria_info[1] < 0.2:
                print("\nОскільки значення індексу узгодженості менше 0.2, але значення відносної узгодженості не менше 0.1,")
                print("то думка експертів не зовсім узгоджена")
            elif criteria_info[2] < 0.1:
                print("\nОскільки значення значення відносної узгодженості менше 0.1, але індекс узгодженості більше 0.2,")
                print("то думка експертів не узгоджена")
            else:
                print("\nОскільки значення індексу узгодженості не менше 0.2 і значення відносної узгодженості не менше 0.1,")
                print("то можна вважати, що думка експертів не узгоджена")

            print("\nОтримали таку матрицю пріоритетів альтернатив за кожним критерієм:")
            print("\t", end=' ')
            for i in range(criteria_number):
                print(f"\tКритерій {i + 1}", end=' ')
            print()
            for i in range(alternatives_number):
                print(f"\tАльтернатива {i + 1}", end=' ')
                for j in range(criteria_number):
                    print(f"\t{alternatives_priorities[i][j]}", end=' ')
                print()

            print("\nЗнайшли такі глобальні пріоритети альтернатив:")
            for i in range(alternatives_number):
                print(f"Альтернатива {i + 1}: {global_alternatives_priorities[i]}")

if __name__ == "__main__":
    main()
