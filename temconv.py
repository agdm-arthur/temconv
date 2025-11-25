from abc import ABC, abstractmethod # Abstract method
from decimal import Decimal, getcontext
getcontext().prec = 22

n9 = Decimal(9)
n5 = Decimal(5)
n32 = Decimal(32)
n273 = Decimal("273.15")
n01 = Decimal("0.01")

# 1. Strategy Pattern: Each conversion is encapsulated in its own class.
class ConversionStrategy(ABC):  # Base interface for polymorphism
    @abstractmethod
    def convert(self, value): pass

class CelsiusToFahrenheit(ConversionStrategy):
    def convert(self, value): return value * n9/n5 + n32

class CelsiusToKelvin(ConversionStrategy):
    def convert(self, value): return value + n273

class FahrenheitToCelsius(ConversionStrategy):
    def convert(self, value): return (value - n32) * n5/n9

class FahrenheitToKelvin(ConversionStrategy):
    def convert(self, value): return (value - n32) * n5/n9 + n273

class KelvinToCelsius(ConversionStrategy):
    def convert(self, value): return value - n273

class KelvinToFahrenheit(ConversionStrategy):
    def convert(self, value): return (value - n273) * n9/n5 + n32

# 2. Factory Method Pattern: Centralized creation of strategy objects.
class ConverterFactory:
    strategy_map = {  # 3. Generic array structure via dictionary of strategy instances
        ("C","F"): CelsiusToFahrenheit(),
        ("C","K"): CelsiusToKelvin(),
        ("F","C"): FahrenheitToCelsius(),
        ("F","K"): FahrenheitToKelvin(),
        ("K","C"): KelvinToCelsius(),
        ("K","F"): KelvinToFahrenheit()
    }

    @staticmethod
    def get_strategy(from_unit, to_unit):
        return ConverterFactory.strategy_map.get((from_unit, to_unit))

# 4. Polymorphism + 5. Reference Variables + 6. Generic Array: Unified handling via base class and list.
class TemperatureConverter:
    def __init__(self):
        self.history = []  # 6. Generic array (list) to store conversion history

    def convert(self, value, from_unit, to_unit):
        strategy = ConverterFactory.get_strategy(from_unit, to_unit)
        if not strategy:
            raise ValueError("Invalid conversion units")
        raw_result = strategy.convert(value)
        result = raw_result.quantize(n01)
        self.history.append((value, from_unit, result, to_unit))
        return result

# 7. Interactive script using input/output loop.
def main():
    converter = TemperatureConverter()
    def unit(prompt): return input(prompt).strip().upper()

    while True:
        try:
            value = Decimal(input("Value: "))
            from_unit = unit("From (C/F/K): ")
            to_unit = unit("To (C/F/K): ")
            result = converter.convert(value, from_unit, to_unit)
            print("Result:", result.quantize(n01), to_unit)
        except Exception as error:
            print(error)
        if input("Continue? (y/n): ").lower() != 'y':
            break

    print("\nHistory:")
    for value, from_unit, result, to_unit in converter.history:
        print(f"{value} {from_unit} > {result.quantize(n01)} {to_unit}")

# 8. Hierarchical OOP structure via class inheritance and design patterns.
if __name__ == "__main__":
    main()