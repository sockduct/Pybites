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
from decimal import Decimal, ROUND_DOWN as ROUND
from operator import add, sub


def get_individuals(total: Decimal, individual: Decimal, people: int,
                    op: Callable[[Decimal, Decimal], Decimal]) -> list[Decimal]:
    for i in range(1, people):
        total = total.quantize(Decimal('1.01'), rounding=ROUND)
        individuals = [op(individual, Decimal('0.01'))] * i + [individual] * (people - i)
        individual_total = sum(individuals)
        ### print(f'{total=}, {individual=}, {people=}, {i=}, {individuals=}, {individual_total=}')
        if individual_total == total:
            return individuals

    raise ValueError('Unable to find matching total.')


def get_amounts(total: Decimal, people: int) -> list[Decimal]:
    individual = Decimal(total/people).quantize(Decimal('1.01'), rounding=ROUND)

    if (people_total := individual * people) == total:
        return [individual] * people
    elif people_total < total:
        return get_individuals(total, individual, people, add)
    else:
        return get_individuals(total, individual, people, sub)


def check_split(item_total: str, tax_rate: str, tip: str, people: int) -> tuple[str, list[Decimal]]:
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

    grand_total3 = total * (1 + tax) * (1 + tip_pct)
    grand_total = Decimal(
        total * (1 + tax) * (1 + tip_pct)).quantize(Decimal('1.01'), rounding=ROUND
    )
    amounts = get_amounts(grand_total, people)

    return f'${grand_total:0.2f}', f'{grand_total3:0.3f}', amounts


if __name__ == '__main__':
    ## print(check_split('$107.93', '6.3%', '22%', 3))
    for args, expected in [
        (('$8.68', '4.75%', '10%', 3), '$10.00'),
        (('$8.44', '6.75%', '11%', 3), '$10.00'),
        (('$9.99', '3.25%', '10%', 2), '$11.34'),
        (('$186.70', '6.75%', '18%', 6), '$235.17'),
        (('$191.57', '6.75%', '15%', 6), '$235.18'),
        (('$0.00', '0%', '0%', 1), '$0.00'),
        (('$100.03', '0%', '0%', 4), '$100.03'),
        (('$141.86', '2%', '18%', 9), '$170.75'),
        (('$16.99', '10%', '20%', 1), '$22.43'),
        (('$16.99', '10%', '20%', 2), '$22.43'),
        (('$16.99', '10%', '20%', 3), '$22.43'),
        (('$16.99', '10%', '20%', 4), '$22.43'),
    ]:
        print(f'{args} => {check_split(*args)}, {expected=}')
