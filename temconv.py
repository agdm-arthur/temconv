#!/usr/bin/python3

from abc import ABC, abstractmethod      # Import abstract method.
from decimal import Decimal, getcontext  # Precise decimals.

# Set internal decimal precision.
getcontext().prec = 22

# Decimal constants reused to avoid redundancy.
# 'n01' is used for rounding.
n9 = Decimal(9)
n5 = Decimal(5)
n32 = Decimal(32)
n273 = Decimal("273.15")
n01 = Decimal("0.01")

# 1st pattern, "Strategy". Abstract base for conversion strategies.
class ConversionStrategy(ABC):
    @abstractmethod
    def convert(self, value): pass  # Implement conversion.

# The actual strategies. Each holds a single conversion formula.
class CelsiusToFahrenheit(ConversionStrategy):
    def convert(self, value): return value * n9 / n5 + n32

class CelsiusToKelvin(ConversionStrategy):
    def convert(self, value): return value + n273

class FahrenheitToCelsius(ConversionStrategy):
    def convert(self, value): return (value - n32) * n5 / n9

class FahrenheitToKelvin(ConversionStrategy):
    def convert(self, value): return (value - n32) * n5 / n9 + n273

class KelvinToCelsius(ConversionStrategy):
    def convert(self, value): return value - n273

class KelvinToFahrenheit(ConversionStrategy):
    def convert(self, value): return (value - n273) * n9 / n5 + n32

# 2nd design pattern, "Factory Method". Maps conversions to strategies.
class ConverterFactory:
    strategy_map = {
        ("C", "F"): CelsiusToFahrenheit(),
        ("C", "K"): CelsiusToKelvin(),
        ("F", "C"): FahrenheitToCelsius(),
        ("F", "K"): FahrenheitToKelvin(),
        ("K", "C"): KelvinToCelsius(),
        ("K", "F"): KelvinToFahrenheit()
    }  # Dictionary used as a simple factory registry.

    @staticmethod
    def get_strategy(from_unit, to_unit):
        # Returns a strategy instance or 'None' if map missing.
        return ConverterFactory.strategy_map.get((from_unit, to_unit))

# Converter makes use of polymorphism, reference variables and array.
class TemperatureConverter:
    def __init__(self):
        self.history = []  # History of conversions.

    def convert(self, value, from_unit, to_unit):
        # Obtain strategy from factory.
        strategy = ConverterFactory.get_strategy(from_unit, to_unit)
        if not strategy:
            raise ValueError("Invalid conversion units")
        # Compute, round to two decimals, store and return.
        raw_result = strategy.convert(value)
        result = raw_result.quantize(n01)
        self.history.append((value, from_unit, result, to_unit))
        return result

# Interactive CLI for input, convert, repeat. Also prints history on exit.
def main():
    converter = TemperatureConverter()

    # Normalize unit input to reduce redundancy.
    def unit(prompt): return input(prompt).strip().upper()

    while True:
        try:
            # Read value using the decimal library.
            value = Decimal(input("Value: "))
            from_unit = unit("From (C/F/K): ")
            to_unit = unit("To (C/F/K): ")
            result = converter.convert(value, from_unit, to_unit)
            # Displays result (rounded).
            print("Result:", result.quantize(n01), to_unit)
        except Exception as error:  # Catches errors.
            print(error)
        if input("Continue? (y/n): ").lower() != 'y':
            break

    # Print history after exit.
    print("\nHistory:")
    for value, from_unit, result, to_unit in converter.history:
        print(f"{value} {from_unit} > {result.quantize(n01)} {to_unit}")

# Program entry point, preserves hierarchical OOP structure.
if __name__ == "__main__":
    main()