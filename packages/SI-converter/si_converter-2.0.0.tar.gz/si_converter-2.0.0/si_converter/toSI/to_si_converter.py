class SIConverter:
    def __init__(self):
        self.unit_conversions = {
            "length": {
                "km": 1000,        # 1 км = 1000 м
                "cm": 0.01,        # 1 см = 0.01 м
                "mm": 0.001,       # 1 мм = 0.001 м
                "inch": 0.0254,    # 1 дюйм = 0.0254 м
                "ft": 0.3048       # 1 фут = 0.3048 м
            },
            "mass": {
                "kg": 1,           # 1 кг = 1 кг
                "g": 0.001,        # 1 г = 0.001 кг
                "mg": 0.000001,    # 1 мг = 0.000001 кг
                "lb": 0.453592     # 1 фунт = 0.453592 кг
            },
            "time": {
                "s": 1,            # 1 сек = 1 сек
                "min": 60,         # 1 мин = 60 сек
                "h": 3600          # 1 час = 3600 сек
            }
        }

    def convert_to_si(self, value, unit_type, from_unit):
        if unit_type not in self.unit_conversions:
            raise ValueError(f"Тип '{unit_type}' не поддерживается. Используйте: {list(self.unit_conversions.keys())}")
        if from_unit not in self.unit_conversions[unit_type]:
            raise ValueError(f"Единица '{from_unit}' не поддерживается для типа '{unit_type}'. Используйте: {list(self.unit_conversions[unit_type].keys())}")
        conversion_factor = self.unit_conversions[unit_type][from_unit]
        return value * conversion_factor