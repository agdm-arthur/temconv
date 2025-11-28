#!/usr/bin/python3
from abc import ABC, abstractmethod # Import abstract method.
from decimal import Decimal, getcontext # Precise floats using strings.
getcontext().prec = 23 # Set internal decimal precision.

num = Decimal # Shorthand for calling Decimal().
def quant(x): # Define how much to round visually.
    return x.quantize(num("0.01"))

unit_list = ( # List of units to show.
# Temperature.
"C (Celsius)\n"
"F (Fahrenheit)\n"
"K (Kelvin)\n"
# Distance.
"KM (Kilometer)\n"
"LK (Leuk)\n"
"MI (Mile)"
)

# 1st pattern, "Strategy". Abstract base for conversion strategies.
class ConvertStrat(ABC):
    @abstractmethod
    def convert(self, value):
        pass # Later to implement conversion.

# The actual worker, an "affine" class that is used for many formulas.
class Calc(ConvertStrat):
    def __init__(self, multiplier, offset=0):
        self.multiplier = num(multiplier)
        self.offset = num(offset)
    def convert(self, value):
        return value * self.multiplier + self.offset

# 2nd pattern, "Factory Method". Maps conversions to created strategies.
# If there were more unique strategies, they could also be included.
class ConverterFactory:
    strategy_map = {
        # Temperature.
        ("C", "F"): Calc("1.8", num(32)),
        ("C", "K"): Calc(1, "273.15"),
        ("F", "C"): Calc(num(5)/num(9), num(-160)/num(9)),
        ("F", "K"): Calc(num(5)/num(9), num(-160)/num(9)+num("273.15")),
        ("K", "C"): Calc(1, "-273.15"),
        ("K", "F"): Calc("1.8", num(32)-num("491.67")),

        # Distance.
        ("KM", "LK"): Calc(0.179985),
        ("KM", "MI"): Calc(0.621371),
        ("LK", "KM"): Calc(5.556000),
        ("LK", "MI"): Calc(3.452338),
        ("MI", "KM"): Calc(1.609344),
        ("MI", "LK"): Calc(0.289658)
    } # Dictionary used as factory registry.

    @staticmethod
    def get_strategy(from_unit, to_unit):
        # Returns a strategy instance if found.
        return ConverterFactory.strategy_map.get((from_unit, to_unit))

# Has concepts of polymorphism, reference variables and array.
class UnitConverter:
    def __init__(self):
        self.history = [] # Conversion history.

    def convert(self, value, from_unit, to_unit):
        # Gets strategy from factory.
        strategy = ConverterFactory.get_strategy(from_unit, to_unit)
        if not strategy:
            raise ValueError("\033c" "Invalid conversion.")
        # Compute, store and return.
        result = strategy.convert(value)
        self.history.append((value, from_unit, result, to_unit))
        return result

# Interactive CLI starts here.
# Input, convert, repeat. Also prints history on exit.
def main():
    converter = UnitConverter()

    class RequestExit(Exception):
        pass

    def get_raw(prompt):
        user_input = input(prompt)
        if user_input.strip().lower() in ("exit", "quit"):
            raise RequestExit
        return user_input

    # Normalizes input to reduce redundancy.
    def unit(prompt):
        return get_raw(prompt).strip().upper()

    while 1:
        try:
            try:
                # Read value using Decimal().
                raw_value = get_raw("\033c" "Value:" "\n> ")
                value = num(raw_value)
                from_unit = unit("\033c" "From:\n" f"{unit_list}" "\n> ")
                to_unit = unit("\033c" "To:\n" f"{unit_list}" "\n> ")
                # Displays result.
                result = converter.convert(value, from_unit, to_unit)
                print("\033c" "Result:", quant(result), to_unit)
            except RequestExit:
                break
            except Exception: # Catches and displays errors.
                print("\033c" "Invalid input.")
            try:
                get_raw("Press any key to continue..." "\n> ")
            except RequestExit:
                break
        except KeyboardInterrupt:
            break

    # Print history on exit if it exists.
    if converter.history:
        print("\033c" "History:")
        for value, from_unit, result, to_unit in converter.history:
            print(f"{value} {from_unit} > {quant(result)} {to_unit}")
    else:
        print("\033c", end="")

# Program entry point, preserves hierarchical OOP structure.
if __name__ == "__main__":
    main()