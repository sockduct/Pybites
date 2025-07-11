#! /usr/bin/env python3.13
'''
In this Bite you'll add type hints to the provided Employee class, making the
code more explicit and improving type checking, readability, and static analysis
support.

Type hints provide clarity on the expected types of class attributes and method
arguments.

In addition, the optional use of dataclass simplifies the class by automatically
generating the constructor (__init__), __repr__, and equality methods (see also
Newbie Bite 39).

However, the dataclass is not required — manual definition of the __init__
method can be retained if preferred, and type hints can still be applied in
either case.
'''


from dataclasses import dataclass


@dataclass
class Employee:
    """Simple Employee class

    :param first_name: String of first name
    :param last_name: String of last name
    :param days_per_week: Integer of how many days per week worked
    :param hours_per_day: Float of hours worked per day
    :param wage: Float of hourly pay
    :param weekly_pay: Property which returns a string for weekly pay
    """
    first_name: str
    last_name: str
    days_per_week: int
    hours_per_day: float
    wage: float

    def _rounder(self, number: float, places: int) -> str:
        """Rounds a number the specified number of places

        :param number: Float of number of round
        :param places: Integer of places to round to
        :return: String representation of the rounded number in US $
        """
        amount = round(number, places)
        return f"${amount:0.2f}"

    @property
    def weekly_pay(self) -> str:
        """Returns amount of weekly pay in US currency

        For instance: $250.75
        """
        total_hours = self.hours_per_day * self.days_per_week
        total_wage = total_hours * self.wage
        return self._rounder(total_wage, 2)


if __name__ == "__main__":
    coder = Employee("Joe", "Blow", 5, 8, 18.0)
    print(coder.weekly_pay)
