# coding: utf8
import sys
from fractions import Fraction
from typing import List, Any

Matrix = tuple[tuple[float]]
Icc = (0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49)


def calcul_norm_prior_vector(matrix: Matrix) -> list[float]:
    if len(matrix) != len(matrix[0]):
        raise Exception("Кількість рядків і стовпців у матриці має бути однаковою!")
    matr_size = len(matrix)
    norm_prior_vector = []
    for row in matrix:
        value = 1
        for elem in row:
            value *= elem
        norm_prior_vector.append(pow(value, 1.0 / matr_size))
    vector_sum = sum(norm_prior_vector)
    for i in range(matr_size):
        norm_prior_vector[i] = norm_prior_vector[i] / vector_sum
    return norm_prior_vector


def calcul_col_sums_vector(matrix: Matrix) -> list[float]:
    rows = len(matrix)
    columns = len(matrix[0])
    sums = []
    for i in range(rows):
        sum = 0
        for j in range(columns):
            sum += matrix[j][i]
        sums.append(sum)
    return sums


def calcul_lambda_ic_oc(sums: tuple[float], norm_prior_vector: tuple[float]) -> (float, float, float):
    if len(sums) != len(norm_prior_vector):
        raise Exception("Кількість сум стовпців має бути такою ж, як і кількість нормованих пріоритетів")
    lambda_val = 0
    number_of_priorities = len(sums)
    for i in range(number_of_priorities):
        lambda_val += sums[i] * norm_prior_vector[i]
    Ic = (lambda_val - number_of_priorities) / (number_of_priorities - 1)
    OC = Ic / Icc[number_of_priorities - 1]
    return lambda_val, Ic, OC


def transpose_matrix(matrix: Matrix) -> list[list[float]]:
    new_matr = []
    rows = len(matrix)
    columns = len(matrix[0])
    for i in range(columns):
        new_matr.append([])
        for j in range(rows):
            new_matr[i].append(matrix[j][i])
    return new_matr


def matrix_vector_product(matrix: Matrix, vector: tuple[float]) -> list[float]:
    if len(matrix[0]) != len(vector):
        raise Exception("Кількість стовпців у першій матриці має дорівнювати кількості рядків в другій матриці!")
    rows = len(matrix)
    res_vector = []
    for i in range(rows):
        value = 0
        for h in range(len(matrix[0])):
            value += matrix[i][h] * vector[h]
        res_vector.append(value)
    return res_vector


def read_matrix_from_file(filename: str) -> list[list[float]]:
    matr = []
    with open(filename, "r") as file:
        for line in file:
            matr.append([float(Fraction(x)) for x in line.split()])
    return matr


def input_int_in_range(min_val: int, max_val: int) -> int:
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

            criteria_prior_matrix = read_matrix_from_file("matrix.txt")

            print("\nМатриця критеріїв (matrix.txt):")
            for row in criteria_prior_matrix:
                print([round(x, 2) for x in row])

            alternatives_matrices = []
            for i in range(criteria_number):
                filename = f"K{i + 1}.txt"
                matrix = read_matrix_from_file(filename)
                alternatives_matrices.append(matrix)

                print(f"\nМатриця для критерію {i + 1} ({filename}):")
                for row in matrix:
                    print([round(x, 2) for x in row])

            norm_criteria_priorities = calcul_norm_prior_vector(tuple(tuple(row) for row in criteria_prior_matrix))
            criteria_col_sums = calcul_col_sums_vector(tuple(tuple(row) for row in criteria_prior_matrix))
            criteria_info = calcul_lambda_ic_oc(tuple(criteria_col_sums), tuple(norm_criteria_priorities))

            alternatives_priorities = []
            for matrix in alternatives_matrices:
                prior_vector = calcul_norm_prior_vector(tuple(tuple(row) for row in matrix))
                alternatives_priorities.append(prior_vector)

            alternatives_priorities = transpose_matrix(tuple(tuple(row) for row in alternatives_priorities))
            global_alternatives_priorities = matrix_vector_product(tuple(tuple(row) for row in alternatives_priorities),
                                                                   tuple(norm_criteria_priorities))

            print("\nМаємо такі нормалізовані пріоритети критеріїв:")
            for i in range(criteria_number):
                print(f"Критерій {i + 1}: {round(norm_criteria_priorities[i], 2)}")

            print("\nВизначимо узгодженість думок експертів:")
            for i in range(len(criteria_info)):
                if i == 0:
                    print(
                        f"Власне значення матриці попарних порівнянь критеріїв (лямбда) = {round(criteria_info[i], 2)}")
                elif i == 1:
                    print(f"Індекс узгодженості (Ic) = {round(criteria_info[i], 2)}")
                else:
                    print(f"Відносна узгодженість (OC) = {round(criteria_info[i], 2)}")

            if criteria_info[1] < 0.2 and criteria_info[2] < 0.1:
                print("\nОскільки значення індексу узгодженості менше 0.2 і значення відносної узгодженості менше 0.1,")
                print("то мжна вважати, що думка експертів узгоджена")
            elif criteria_info[1] < 0.2:
                print(
                    "\nОскільки значення індексу узгодженості менше 0.2, але значення відносної узгодженості не менше 0.1,")
                print("то думка експертів не зовсім узгоджена")
            elif criteria_info[2] < 0.1:
                print(
                    "\nОскільки значення значення відносної узгодженості менше 0.1, але індекс узгодженості більше 0.2,")
                print("то думка експертів не узгоджена")
            else:
                print(
                    "\nОскільки значення індексу узгодженості не менше 0.2 і значення відносної узгодженості не менше 0.1,")
                print("то можна вважати, що думка експертів не узгоджена")

            print("\nОтримали таку матрицю пріоритетів альтернатив за кожним критерієм:")
            print("\t", end=' ')
            for i in range(criteria_number):
                print(f"\tКритерій {i + 1}", end=' ')
            print()
            for i in range(alternatives_number):
                print(f"\tАльтернатива {i + 1}", end=' ')
                for j in range(criteria_number):
                    print(f"\t{round(alternatives_priorities[i][j], 2)}", end=' ')
                print()

            print("\nЗнайшли такі глобальні пріоритети альтернатив:")
            for i in range(alternatives_number):
                print(f"Альтернатива {i + 1}: {round(global_alternatives_priorities[i], 2)}")


if __name__ == "__main__":
    main()
