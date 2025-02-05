#! /usr/bin/env python3.13


from collections import namedtuple


SUITS = 'Red Green Yellow Blue'.split()
UnoCard = namedtuple('UnoCard', 'suit name')


def create_uno_deck() -> list[UnoCard]:
    """
    Create a deck of 108 Uno cards:
    * There are four suits, Red, Green, Yellow and Blue
    * Each suit consists of one 0 card, two 1 cards, two 2s, 3s, 4s, 5s, 6s, 7s,
      8s and 9s; two Draw Two cards; two Skip cards; and two Reverse cards
    * There are also four Wild cards and four Wild Draw Four cards (no suit)

    Return a list of UnoCard namedtuples
    (for cards w/o suit use None in the namedtuple)
    """
    suit_cards = (
        ['0'] +
        [str(n) for n in range(1, 10)] * 2 +
        ['Draw Two', 'Skip', 'Reverse'] * 2
    )
    nosuit_cards = ['Wild', 'Wild Draw Four']

    return (
        [UnoCard(suit=suit, name=card) for suit in SUITS for card in suit_cards] +
        [UnoCard(suit=None, name=card) for card in nosuit_cards] * 4
    )


if __name__ == '__main__':
    deck = create_uno_deck()
