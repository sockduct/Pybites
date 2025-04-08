#! /usr/bin/env python3.13
"""
Pairs wines and cheeses by similarity of wine name and cheese name.

Many gourmets struggle to find the perfect pairing of wines and cheeses. A
number of considerations are relevant, each of which creates a unique
combination. Finding the perfect match is a life long pursuit.

For the purposes of this bite, you will pair cheese and wines by the
similarities of their names. We've helpfully provided a name similarity
function, defined as:

             sum of values of intersection of char counters of names
similarity = ―――――――――――――――――――――――――――――――――――――――――――――――――――――――
                   1 + square of length difference of both words

Notes:
* Upper and lower case letters are ignored in the summing process.
* Space " ", dash "-", and apostrophe "'" are considered valid characters.

Examples:
'house' 'mouse'            -> {'e': 1, 'o': 1, 's': 1, 'u': 1}  -> 4 / (1 + pow(5 - 5),2)) = 4
'parapraxis' 'explanation' -> {'a': 2, 'i': 1, 'p': 1, 'x': 1}  -> 5 / (1 + pow(10 - 11),2) = 2.5
'parapraxis' 'parallax'    -> {'a': 3, 'p': 1, 'r': 1, 'x': 1}  -> 6 / (1 + (10 - 8)**2 ) = 1.2
'roosters-do-sound' 'cocka-doodle-doo'
                           -> {'-': 2, 'd': 2, 'e': 1, 'o': 4} -> 9 / (1 + pow(17-16),2) = 4.5
'Cabernet sauvignon' 'Dorset Blue Vinney' ->
                           -> {'e': 2, 'n': 2, 'o': 1, 'r': 1, 's': 1, 't': 1, ' ': 1, 'b': 1,
                               'u': 1, 'v': 1, 'i': 1} -> 13 / (1 + pow(18 - 18),2) = 13

Three wine lists are provided: red, white, sparkling.

Pair the wine with the forty-three cheeses mentioned in the Monty Python's
Flying Circus sketch "Cheese Shop".

Tasks
Complete the function best_match_per_wine() which returns the best scored
wine-cheese pair. Matching can be for a certain wine type (i.e. red, white,
sparkling) or for all types. Raise ValueError for wines that do not appear in
the lists of known wines.

Complete the function match_wine_5cheeses() which returns a sorted list of
wines, where for each wine are listed 5 best matching cheeses.

All types of wines (red, white, and sparkling) are included.

Lists of cheeses are sorted by descending similarity score and then ascending
alphabetical order.

Output example:
[('Barbera', ['Cheddar', 'Gruyère', 'Boursin', 'Parmesan', 'Liptauer']),
...
 ('Zinfandel', ['Caithness', 'Bel Paese', 'Ilchester', 'Limburger', 'Lancashire'])
]

Areas: Counter sorting operator intersection
"""


from collections import Counter, defaultdict
from itertools import product
import operator
from pprint import pformat


CHEESES = [
    "Red Leicester",
    "Tilsit",
    "Caerphilly",
    "Bel Paese",
    "Red Windsor",
    "Stilton",
    "Emmental",
    "Gruyère",
    "Norwegian Jarlsberg",
    "Liptauer",
    "Lancashire",
    "White Stilton",
    "Danish Blue",
    "Double Gloucester",
    "Cheshire",
    "Dorset Blue Vinney",
    "Brie",
    "Roquefort",
    "Pont l'Evêque",
    "Port Salut",
    "Savoyard",
    "Saint-Paulin",
    "Carré de l'Est",
    "Bresse-Bleu",
    "Boursin",
    "Camembert",
    "Gouda",
    "Edam",
    "Caithness",
    "Smoked Austrian",
    "Japanese Sage Derby",
    "Wensleydale",
    "Greek Feta",
    "Gorgonzola",
    "Parmesan",
    "Mozzarella",
    "Pipo Crème",
    "Danish Fynbo",
    "Czech sheep's milk",
    "Venezuelan Beaver Cheese",
    "Cheddar",
    "Ilchester",
    "Limburger",
]

RED_WINES = [
    "Châteauneuf-du-Pape",  # 95% of production is red
    "Syrah",
    "Merlot",
    "Cabernet sauvignon",
    "Malbec",
    "Pinot noir",
    "Zinfandel",
    "Sangiovese",
    "Barbera",
    "Barolo",
    "Rioja",
    "Garnacha",
]

WHITE_WINES = [
    "Chardonnay",
    "Sauvignon blanc",
    "Semillon",
    "Moscato",
    "Pinot grigio",
    "Gewürztraminer",
    "Riesling",
]

SPARKLING_WINES = [
    "Cava",
    "Champagne",
    "Crémant d’Alsace",
    "Moscato d’Asti",
    "Prosecco",
    "Franciacorta",
    "Lambrusco",
]


def compare(wine: str, cheese: str) -> float:
    intersection = Counter(wine.lower()) & Counter(cheese.lower())
    numerator = sum(intersection.values())
    denominator = 1 + (len(wine) - len(cheese))**2
    return numerator/denominator


def best_match_per_wine(wine_type: str="all") -> tuple[str, str, float]:
    """Wine cheese pair with the highest match score
    returns a tuple which contains wine, cheese, score
    """
    match wine_type:
        case 'all' | 'ALL':
            wines = RED_WINES + WHITE_WINES + SPARKLING_WINES
        case 'red' | 'RED' | 'RED_WINES':
            wines = RED_WINES
        case 'white' | 'WHITE' | 'WHITE_WINES':
            wines = WHITE_WINES
        case 'sparkling' | 'SPARKLING' | 'SPARKLING_WINES':
            wines = SPARKLING_WINES
        case _:
            raise ValueError(
                f'Expected all, red, white, or sparking for wine type, got "{wine_type}".'
            )

    best: list[tuple[str, str, float]] = [
        (wine, cheese, compare(wine, cheese)) for wine in wines for cheese in CHEESES
    ]
    return max(best, key=lambda item: item[2])


def match_wine_5cheeses(*, format: bool=False) -> str|list[tuple[str, list[str]]]:
    """Pairs all types of wines with cheeses ; returns a sorted list of tuples,
    where each tuple contains: wine, list of 5 best matching cheeses.
    List of cheeses is sorted by score descending then alphabetically ascending.
    e.g: [
    ('Barbera', ['Cheddar', 'Gruyère', 'Boursin', 'Parmesan', 'Liptauer']),
    ...
    ...
    ('Zinfandel', ['Caithness', 'Bel Paese', 'Ilchester', 'Limburger', 'Lancashire'])
    ]
    """
    wines = RED_WINES + WHITE_WINES + SPARKLING_WINES
    scores = defaultdict(list)
    # For each wine, score it against all cheeses:
    for wine, cheese in product(wines, CHEESES):
        scores[wine].append((cheese, compare(wine, cheese)))

    # Sort each wine's cheeses by score descending then alphabetically ascending,
    # and keep only the top 5:
    for wine in scores:
        scores[wine] = sorted(scores[wine], key=lambda item: (-item[1], item[0]))[:5]

    # Sort wines in ascending order with only cheeses (drop scores):
    result = sorted((wine, [cheese for cheese, _ in cheeses]) for wine, cheeses in scores.items())
    # Optionally format result:
    return pformat(result, compact=True, width=120) if format else result


if __name__ == "__main__":
    for func, args in (('best_match_per_wine', None), ('match_wine_5cheeses', dict(format=True))):
        params = args or {}
        print(
            f'Invoking {func}({", ".join(f"{k}={v}" for k, v in params.items())}):  '
            f'{globals()[func](**params)}'
        )
