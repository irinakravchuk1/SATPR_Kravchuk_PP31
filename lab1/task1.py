import pandas as pd

# Початкова таблиця з даними
data = {
    'Критерій/Альтернатива': ['A1', 'A2', 'A3', 'A4', 'Вага'],
    'K1': [3, 8, 4, 9, 8],
    'K2': [7, 3, 8, 6, 9],
    'K3': [2, 6, 3, 5, 6],
    'K4': [9, 7, 5, 4, 7]
}

# Ваги критеріїв
weights = [8, 9, 6, 7]

# Створення DataFrame
df = pd.DataFrame(data)
df.set_index('Критерій/Альтернатива', inplace=True)

# Виділяємо вагу окремо для обчислень
criteria_only_df = df.drop(index='Вага')

# Функція корисності
utility_df = criteria_only_df.mul(weights)

# Результати
utility_df['результат'] = utility_df.sum(axis=1)

# Найкращий кандидат
best_candidate = utility_df['результат'].idxmax()

# Вивід початкової таблиці
print("Початкова таблиця:")
print(df)

# Вивід таблиці обчислень
print("\nТаблиця обчислень:")
print(utility_df)

# Вивід найкращого кандидата
print(f"\nНайкращий кандидат: {best_candidate}")
