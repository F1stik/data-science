import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)

n = 1000

products = ['Капучино', 'Латте', 'Эспрессо', 'Американо', 'Раф', 'Флэт Уайт']
prices_dict = {
    'Капучино': 180, 'Латте': 210, 'Эспрессо': 120,
    'Американо': 150, 'Раф': 250, 'Флэт Уайт': 190
}

data = []
start_date = datetime(2025, 3, 1)

for i in range(n):
    random_days = np.random.randint(0, 31)
    hour = np.random.choice(
        [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        p=[0.08, 0.13, 0.15, 0.12, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.03, 0.02, 0.02]
    )
    minute = np.random.randint(0, 60)

    order_time = start_date + timedelta(
        days=int(random_days), hours=int(hour), minutes=int(minute)
    )

    product = np.random.choice(products, p=[0.27, 0.24, 0.16, 0.13, 0.12, 0.08])
    price = prices_dict[product]
    quantity = np.random.choice([1, 2, 3, 4], p=[0.55, 0.25, 0.15, 0.05])
    total = price * quantity

    data.append({
        'order_id': 1000 + i,
        'datetime': order_time,
        'product': product,
        'price': price,
        'quantity': quantity,
        'total': total
    })

df = pd.DataFrame(data)

# === Правильное сохранение в data/raw ===
project_root = Path(__file__).parent.parent          # поднимаемся из scripts/ в корень
csv_path = project_root / "data" / "raw" / "coffee_shop_orders.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)   # создаём папки, если нужно

df.to_csv(csv_path, index=False, encoding='utf-8-sig')

print(f"✅ Датасет успешно создан и сохранён: {csv_path}")
print(f"Количество строк: {len(df)}")