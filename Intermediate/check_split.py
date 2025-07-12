#! /usr/bin/env python3.13
'''
Three old friends Bob, Mary, and Alice meet at PyCon and decide to go out to
dinner together. They have a wonderful time discussing lambda calculus and
laughing about import antigravity.

At the end of the meal, being such good friends they decide to split the check
"evenly" 3 ways.

Given an item total add tax (based on the given tax rate) and a tip (applied
post-tax) producing a grand total. Next, split the grand total amount as evenly
as possible amongst the friends. The sum of the per person split should be
equivalent to the grand total.

Tasks
Complete check_split(item_total, tax_rate, tip, people), see the docstring for
input parameters and expected return values.
'''


from collections.abc import Callable
from operator import add, sub


type Numeric = int | float


def get_individuals(total: float, individual: float, people: int,
                    op: Callable[[Numeric, Numeric], Numeric]) -> list[Numeric]:
    for i in range(1, people):
        individuals = [op(individual, 0.01)] * i + [individual] * (people - i)
        individual_total = sum(individuals)
        print(f'{total=}, {individual=}, {people=}, {i=}, {individuals=}, {individual_total=}')
        if sum(individuals) == total:
            return individuals

    raise ValueError('Unable to find matching total.')


def get_amounts(total: float, people: int) -> list[float]:
    individual = round(total/people, 2)

    if (people_total := individual * people) == total:
        return [individual] * people
    elif people_total < total:
        return get_individuals(total, individual, people, add)
    else:
        return get_individuals(total, individual, people, sub)


def check_split(item_total: str, tax_rate: str, tip: str, people: int) -> tuple[str, list[float]]:
    """Calculate check value and evenly split.

       :param item_total: str (e.g. '$8.68')
       :param tax_rate: str (e.g. '4.75%)
       :param tip: str (e.g. '10%')
       :param people: int (e.g. 3)

       :return: tuple of (grand_total: str, splits: list)
                e.g. ('$10.00', [3.34, 3.33, 3.33])
    """
    total = float(item_total.lstrip('$'))
    tax = float(tax_rate.rstrip('%'))/100
    tip_pct = float(tip.rstrip('%'))/100

    grand_total = round(total * (1 + tax) * (1 + tip_pct), 2)
    amounts = get_amounts(grand_total, people)

    return f'${grand_total}', amounts


if __name__ == '__main__':
    print(check_split('$107.93', '6.3%', '22%', 3))
