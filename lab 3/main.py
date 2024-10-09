# coding: utf8
probab_and_demand = tuple[float, int]


# Функція для зчитування даних з файлу і обчислення ймовірностей та констант
def read_stats_and_constants_from_file(filename: str) -> tuple[float, float, float, tuple[probab_and_demand]]:
    stats = []
    total_first_column = 0
    cost, price, sale_price = 0, 0, 0

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # Перший рядок файлу містить константи cost, price, sale_price
        cost, price, sale_price = map(float, lines[0].split())

        # Підраховуємо суму першого стовпчика для обчислення ймовірностей
        for line in lines[1:]:
            total_first_column += float(line.split()[0])

        # Формуємо кортежі з ймовірностями та попитом
        for line in lines[1:]:
            parts = line.split()
            prob = float(parts[0]) / total_first_column  # Ймовірність = значення з 1-го стовпця / загальна сума
            demand = int(parts[1])
            stats.append((prob, demand))

    return cost, price, sale_price, tuple(stats)


# Функція для прийняття рішення щодо кількості товару
def makeDecision(cost: float, price: float, sale_price: float, stats: tuple[probab_and_demand]) -> tuple[float, int]:
    net_profit: float = price - cost
    net_loss: float = sale_price - cost

    general_expected_incomes: [float] = []
    for i in range(len(stats)):
        available: int = stats[i][1]
        general_expected_incomes.append(0)
        for stat in stats:
            demand: int = stat[1]
            sold: int = min(available, demand)
            not_sold: int = available - sold
            expected_by_demand: float = sold * net_profit + not_sold * net_loss
            general_expected_incomes[i] += expected_by_demand * stat[0]

    max_expected_income: float = max(general_expected_incomes)
    recommend_produce: int = stats[general_expected_incomes.index(max_expected_income)][1]

    return round(max_expected_income, 2), recommend_produce


# меню для вибору задачі
def show_menu():
    print("\nОберіть задачу для виконання:")
    print("1 - Задача 9")
    print("2 - Задача 11")
    print("0 - Вийти")
    choice = input("Ваш вибір (0, 1 або 2): ")
    return choice


def execute_task_9():
    print("Задача 9:")
    task9_cost, task9_price, task9_sale_price, task9_stats = read_stats_and_constants_from_file('task9.txt')

    print(f"Собівартість виготовлення однієї булочки, пенсів: {task9_cost:.2f}")
    print(f"Ціна продажу однієї булочки, пенсів: {task9_price:.2f}")
    print(f"Чистий дохід за продаж однієї булочки: {task9_price - task9_cost:.2f}")
    print(f"Збиток за непродаж однієї булочки, пенсів: {task9_sale_price - task9_cost:.2f}\n")

    for stat in task9_stats:
        print(f"Ймовірність попиту: {stat[0]:.2f}, попит на булочки (тис. шт./день): {stat[1]}")

    task9_res = makeDecision(task9_cost, task9_price, task9_sale_price, task9_stats)
    print(f"\n--Отже нам варто виготовляти таку кількість булочок (тис. шт.) в день: {task9_res[1]}")
    print(f"--Тоді ми матимемо такий очікуваний прибуток, тис. пенсів: {task9_res[0]:.2f}")


def execute_task_11():
    print("Задача 11:")
    task11_cost, task11_price, task11_sale_price, task11_stats = read_stats_and_constants_from_file('task11.txt')

    print(f"Ціна закупки однієї булочки, доларів: {task11_cost:.2f}")
    print(f"Ціна продажу однієї булочки, доларів: {task11_price:.2f}")
    print(f"Ціна розпродажу однієї булочки, доларів: {task11_sale_price:.2f}")
    print(f"Чистий дохід за продаж однієї булочки, доларів: {task11_price - task11_cost:.2f}")
    print(f"Збиток за розпродаж однієї булочки, доларів: {task11_sale_price - task11_cost:.2f}\n")

    for stat in task11_stats:
        print(f"Ймовірність попиту: {stat[0]:.2f}, попит на булочки (шт./день): {stat[1]}")

    task11_res = makeDecision(task11_cost, task11_price, task11_sale_price, task11_stats)
    print(f"\n--Отже нам варто виготовляти таку кількість булочок (шт.) в день: {task11_res[1]}")
    print(f"--Тоді ми матимемо такий очікуваний прибуток, доларів: {task11_res[0]:.2f}")


def main():
    while True:
        choice = show_menu()

        if choice == '1':
            execute_task_9()
        elif choice == '2':
            execute_task_11()
        elif choice == '0':
            print("Завершення програми.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")

    exit()  # Додаємо exit для завершення програми після виходу з циклу


if __name__ == "__main__":
    main()
