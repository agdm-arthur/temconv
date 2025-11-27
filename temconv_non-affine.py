#!/usr/bin/python3
from abc import ABC, abstractmethod
from decimal import Decimal, getcontext
getcontext().prec = 23

num = Decimal
round_num = num("0.01")
unit_list = ("\n"
"C (Celsius)\n"       "F (Fahrenheit)\n"    "K (Kelvin)\n"
"KM (Kilometer)\n"    "L (Leuk)\n"          "MI (Mile)\n"
)

class ConversionStrategy(ABC):
    @abstractmethod
    def convert(self, value):
        pass

class CelsiusToFahrenheit(ConversionStrategy):
    def convert(self, value):
        return value * num(9) / num(5) + num(32)

class CelsiusToKelvin(ConversionStrategy):
    def convert(self, value):
        return value + num("273.15")

class FahrenheitToCelsius(ConversionStrategy):
    def convert(self, value):
        return (value - num(32)) * num(5) / num(9)

class FahrenheitToKelvin(ConversionStrategy):
    def convert(self, value):
        return (value - num(32)) * num(5) / num(9) + num("273.15")

class KelvinToCelsius(ConversionStrategy):
    def convert(self, value):
        return value - num("273.15")

class KelvinToFahrenheit(ConversionStrategy):
    def convert(self, value):
        return (value - num("273.15")) * num(9) / num(5) + num(32)

class KilometerToLeuk(ConversionStrategy):
    def convert(self, value):
        return value * num("0.179985")

class KilometerToMile(ConversionStrategy):
    def convert(self, value):
        return value * num("0.621371")

class LeukToKilometer(ConversionStrategy):
    def convert(self, value):
        return value * num("5.556")

class LeukToMile(ConversionStrategy):
    def convert(self, value):
        return value * num("3.452338")

class MileToKilometer(ConversionStrategy):
    def convert(self, value):
        return value * num("1.609344")

class MileToLeuk(ConversionStrategy):
    def convert(self, value):
        return value * num("0.289658")

class ConverterFactory:
    strategy_map = {
        ("C", "F"): CelsiusToFahrenheit(),
        ("C", "K"): CelsiusToKelvin(),
        ("F", "C"): FahrenheitToCelsius(),
        ("F", "K"): FahrenheitToKelvin(),
        ("K", "C"): KelvinToCelsius(),
        ("K", "F"): KelvinToFahrenheit(),
        ("KM", "L"): KilometerToLeuk(),
        ("KM", "MI"): KilometerToMile(),
        ("L", "KM"): LeukToKilometer(),
        ("L", "MI"): LeukToMile(),
        ("MI", "KM"): MileToKilometer(),
        ("MI", "L"): MileToLeuk()
    }

    @staticmethod
    def get_strategy(from_unit, to_unit):
        return ConverterFactory.strategy_map.get((from_unit, to_unit))

class UnitConverter:
    def __init__(self):
        self.history = []

    def convert(self, value, from_unit, to_unit):
        strategy = ConverterFactory.get_strategy(from_unit, to_unit)
        if not strategy:
            raise ValueError("\033c" "Invalid conversion.")
        raw_result = strategy.convert(value)
        result = raw_result.quantize(round_num)
        self.history.append((value, from_unit, result, to_unit))
        return result

def main():
    converter = UnitConverter()

    def unit(prompt):
        return input(prompt).strip().upper()

    while 1:
        try:
            value = num(input("\033c" "Value:" "\n> "))
            from_unit = unit("\033c" "From:" f"{unit_list}" "> ")
            to_unit = unit("\033c" "To:" f"{unit_list}" "> ")
            result = converter.convert(value, from_unit, to_unit)
            print("\033c" "Result:", result.quantize(round_num), to_unit)
        except Exception as error:
            print(error)
        if input("Continue? (y/n):" "\n> ").lower() != 'y':
            break

    print("\033c" "History:")
    for value, from_unit, result, to_unit in converter.history:
        print(f"{value} {from_unit} > {result.quantize(round_num)} {to_unit}")

if __name__ == "__main__":
    main()