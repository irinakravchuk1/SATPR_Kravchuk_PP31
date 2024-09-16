import pandas as pd
import numpy as np

# Вхідні дані
data = {
    'Критерій/Альтернатива': ['A1', 'A2', 'A3', 'A4', 'A5', 'Вага'],
    'K1': [85, 60, 30, 75, 40, 7],
    'K2': [30, 20, 12, 24, 15, 5],
    'K3': [22, 10, 5, 13, 7, 6],
    'K4': [0.65, 0.6, 0.45, 0.7, 0.55, 8],
    'K5': [6, 7, 5, 8, 7, 6]
}

# Створення DataFrame
df = pd.DataFrame(data)
df.set_index('Критерій/Альтернатива', inplace=True)

# Відділяємо рядок ваг для обчислень
weights = df.loc['Вага']
criteria_only_df = df.drop(index='Вага')

# Нормалізація
normalized_df = pd.DataFrame()

# Максимізація критеріїв K1, K3, K5
for col in ['K1', 'K3', 'K5']:
    max_val = criteria_only_df[col].max()
    min_val = criteria_only_df[col].min()
    normalized_df[col] = (criteria_only_df[col] - min_val) / (max_val - min_val)

# Мінімізація критерію K2
max_val_k2 = criteria_only_df['K2'].max()
min_val_k2 = criteria_only_df['K2'].min()
normalized_df['K2'] = (max_val_k2 - criteria_only_df['K2']) / (max_val_k2 - min_val_k2)

# Критерій K4 залишається без змін
normalized_df['K4'] = criteria_only_df['K4']

# Округлення значень в нормалізованій таблиці до 2 знаків після коми
normalized_df = normalized_df.round(2)

# Функція корисності
utility_df = normalized_df.mul(weights)

# Округлення значень у таблиці обчислень до 2 знаків після коми
utility_df = utility_df.round(2)

# Результати
utility_df['результат'] = utility_df.sum(axis=1)

# Найкращий кандидат
best_candidate = utility_df['результат'].idxmax()

# Вивід початкової таблиці
print("Початкова таблиця:")
print(df)

# Вивід нормалізованої таблиці
print("\nНормалізована таблиця:")
print(normalized_df)

# Вивід таблиці обчислень
print("\nТаблиця обчислень:")
print(utility_df)

# Вивід найкращого кандидата
print(f"\nНайкращий кандидат: {best_candidate}")
