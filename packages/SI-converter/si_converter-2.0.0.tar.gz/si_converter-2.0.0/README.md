# Перевод единиц измерения в систему СИ
## Описание
Библиотека позволяет переводить единицы измерения в периодическую систему СИ (toSI), а также из системы СИ в нужную единицу измерения (fromSI).
## Установка
pip install "Название библиотеки"

## Использование
### В систему СИ (toSI)

from si_converter import SIConverter  
converter = SIConverter()  
result = converter.convert_from_si(3600, "time", "h")  
print(f"3600 секунд в часах: {result} ч")

### Из системы СИ (fromSI)

from si_converter import SIConverter  
converter = SIConverter()  
result = converter.convert_to_si(100, "mass", "g")  
print(f"100 граммов в килограммах: {result} кг")  
