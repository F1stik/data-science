import sys
import pandas as pd
import numpy as np

print("=== Проверка окружения ===")
print("Python:", sys.version.split()[0])
print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Окружение работает корректно!")