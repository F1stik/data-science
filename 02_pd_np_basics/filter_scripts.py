import pandas as pd

# путь к файлу выписки
FILE_PATH = "D:\Python\project\data-science\data\raw\bsb_bank_statement.csv"   # <-- измени на свой путь

import pandas as pd
import json
from pathlib import Path

FILE_PATH = "bsb_bank_statement.csv"          # путь к выписке
MAP_FILE = "exact_map.json"                   # файл, куда сохраняем разметку


df = pd.read_csv(r'D:\Python\project\data-science\data\raw\bsb_bank_statement.csv')

df.columns = [
    'operation_date', 'transaction_date', 'card_last4',
    'description', 'place', 'currency',
    'amount_original', 'amount', 'balance'
]

df['place'] = (
    df['place']
    .astype(str)
    .str.upper()
    .str.replace('"', '', regex=False)
    .str.replace('«', '', regex=False)
    .str.replace('»', '', regex=False)
    .str.strip()
)

# ЗАГРУЗКА УЖЕ СУЩЕСТВУЮЩЕЙ РАЗМЕТКИ
if Path(MAP_FILE).exists():
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        exact_map = json.load(f)
    print(f"Загружено {len(exact_map)} ранее размеченных мест\n")
else:
    exact_map = {}
    print("Файл разметки не найден — начинаем с нуля\n")

# =ФУНКЦИЯ КАТЕГОРИЙ
def get_category(place):
    if pd.isna(place):
        return 'Прочее'
    
    place = str(place).upper()
    
    # Сначала точные совпадения
    if place in exact_map:
        return exact_map[place]
    
    # правила
    if any(word in place for word in ['PERSON TO PERSON', 'INTERNET-BANKING']):
        return 'Аренда'
    if any(word in place for word in ['SOSEDI', 'SANTA', 'EVROOPT', 'EUROOPT', 'UNIVERSAM', 'GIPPO', 'GREEN', 'MILA', 'GALAMART', 'PROSTORE', 'ALMI', 'IZYUM', 'KOPEECHKA', 'KARAVAY', 'NASHA LAVKA', 'MAYAK', 'TRI TSENY', 'FIX PRICE', 'SUPERPROD', 'PRODUKTY', 'N9869', 'IZYSKANNAYA KUHN', 'TM N3']):
        return 'Продукты'
    if any(word in place for word in ['KAFE', 'CAFÉ', 'RESTORAN', 'БУФЕТ', 'BUFET', 'STOLOV', 'PIZZA', 'BURGER', 'KFC', 'SUSHI', 'SHAVERMA', 'DONER', 'KEBAB', 'PEREMENA', 'VKUSFRI', 'BUBBLE TEA', 'COFFEE', 'KOFE', 'CRISPY', 'PONCHIK', 'SYAO FAN', 'PAB 12', 'SEN KHANOY', 'SHAURMA', 'AZIATSKOE BISTRO', 'TOKINY', 'ART FOOD', 'DOST.GOTOVOY']):
        return 'Кафе и рестораны'
    if any(word in place for word in ['PYATY ELEMENT', '5 ELEMENT', '21VEK', 'DNS ELEKTRONIKA']):
        return 'Техника'
    if any(word in place for word in ['DZHINSOMANIYA']):
        return 'Одежда'
    if any(word in place for word in ['APTEKA', 'АПТЕКА', 'PHARM', 'FABRIKA ZDOROVYA']):
        return 'Аптеки'
    if any(word in place for word in ['TRANSPORT', 'YANDEX', 'TAXI', 'АЗС', 'AZS', 'МАЗС', 'PASS.RW', 'HELLO']):
        return 'Транспорт'
    if any(word in place for word in ['WILDBERRIES', 'OZON', 'JOOM', 'ALIEXPRESS', 'PRINOSIM RADOST']):
        return 'Онлайн-магазины'
    if any(word in place for word in ['KINO', 'SKYLINE', 'MUZEY', '24AFISHA']):
        return 'Развлечения'
    if any(word in place for word in ['ATM']):
        
        return 'Снятие наличных'
    if any(word in place for word in ['LEONARDO']):
        return 'Хобби'
    if any(word in place for word in ['CROCUS24']):
        return 'Подарки'
    if any(word in place for word in ['COSMOS', 'TELECOM']):
        return 'Связь'
    if any(word in place for word in ['OSTROV CHIST']):
        return 'Дом и быт'
    if any(word in place for word in ['ERIP', 'PEREVOD', 'P2P', 'COMPAY']):
        return 'Банковские операции'
    
    return 'Прочее'


df['category'] = df['place'].apply(get_category)

#
prochee_places = (
    df[df['category'] == 'Прочее']
    .groupby('place')['amount']
    .sum()
    .sort_values(ascending=False)
    .index
    .tolist()
)

categories = [
    "Пропустить",
    "Продукты",
    "Кафе и рестораны",
    "Аренда",
    "Техника",
    "Одежда",
    "Аптеки",
    "Транспорт",
    "Онлайн-магазины",
    "Развлечения",
    "Снятие наличных",
    "Хобби",
    "Подарки",
    "Связь",
    "Дом и быт",
    "Банковские операции"
]

print(f"Осталось разметить: {len(prochee_places)} мест\n")

try:
    for place in prochee_places:
        print("\n" + "=" * 60)
        print(f"Место: {place}")
        print("К какой категории отнести?\n")
        
        for i, cat in enumerate(categories):
            print(f"{i}. {cat}")
        
        while True:
            try:
                choice = int(input("\nНомер категории: "))
                if 0 <= choice < len(categories):
                    selected = categories[choice]
                    if selected != "Пропустить":
                        exact_map[place] = selected
                        # Сразу сохраняем на диск
                        with open(MAP_FILE, "w", encoding="utf-8") as f:
                            json.dump(exact_map, f, ensure_ascii=False, indent=2)
                        print(f"→ Сохранено: {place} → {selected}")
                    else:
                        print("→ Пропущено")
                    break
                else:
                    print("Нет такого номера")
            except ValueError:
                print("Введи число")

except KeyboardInterrupt:
    print("\n\nСкрипт остановлен пользователем (Ctrl+C)")

print("\n" + "=" * 60)
print(f"Всего размечено мест: {len(exact_map)}")
print(f"Файл сохранён: {MAP_FILE}")
print("=" * 60)