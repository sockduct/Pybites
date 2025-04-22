#! /usr/bin/env python3.13
'''
You are given a list of operas and a list of composers. For two given composers
find operas (where one of the composers is the author) at which premiere both
could have been together (i.e. they both had to be alive). Consider just a
theoretical possibility of presence, so omit health condition, traveling
problems, resources, and any other problems (excluding death) which could
restrict their presence.

The list of operas consists of namedtuple('Opera', 'author play date') objects.
The list of composers contains dictionaries with keys => composer names and
values => namedtuple('Composer', 'name born died') objects.

Complete the operas_both_at_premiere(guest, composers) function. Parameters:
* guest - one of the composers but not the author of an opera
* composer - the author of an opera

If the required composer or guest is not in the list of composers, raise a
ValueError exception. You can use the _get_date helper to convert date strings
into datetime objects.

Return a list (or generator) of titles of operas. See the tests for more
information.

Note that the list of operas in the Bite is shortened.

Sources:
* https://en.wikipedia.org/wiki/List_of_operas_by_Wolfgang_Amadeus_Mozart
* https://en.wikipedia.org/wiki/List_of_compositions_by_Ludwig_van_Beethoven
* https://en.wikipedia.org/wiki/List_of_works_for_the_stage_by_Richard_Wagner
* https://en.wikipedia.org/wiki/List_of_compositions_by_Giuseppe_Verdi
'''


from collections import namedtuple
from collections.abc import Iterator
from datetime import datetime, date
from pprint import pprint


Composer = namedtuple('Composer', 'name born died')
Opera = namedtuple('Opera', 'author play date')

composers = {
    "beethoven": Composer("Ludwig van Beethoven",
                          "17 December 1770", "26 March 1827"),
    "wagner": Composer("Richard Wagner",
                       "22 May 1813", "13 February 1883"),
    "verdi": Composer("Giuseppe Verdi",
                      "9 October 1813", "27 January 1901"),
    "mozart": Composer("Wolfgang Amadeus Mozart",
                       "27 January 1756", "5 December 1791"),
}

operas = [
    Opera("mozart", "Apollo and Hyacinth", "13 May 1767"),
    Opera("mozart", "Marriage of Figaro", "1 May 1786"),
    Opera("mozart", "Don Giovanni", "29 October 1787"),
    Opera("mozart", "Così fan tutte", "6 January 1790"),
    Opera("mozart", "The Clemency of Titus", "6 September 1791"),
    Opera("mozart", "The Magic Flute", "30 September 1791"),
    Opera("wagner", "The Fairies", "29 June 1888"),
    Opera("wagner", "Rienzi", "20 October 1842"),
    Opera("wagner", "The Flying Dutchman", "2 January 1843"),
    Opera("wagner", "Tannhäuser", "19 October 1845"),
    Opera("wagner", "Lohengrin", "28 August 1850"),
    Opera("wagner", "The Rhinegold", "22 September 1869"),
    Opera("wagner", "The Valkyrie", "26 June 1870"),
    Opera("wagner", "Siegfried", "16 August 1876"),
    Opera("wagner", "Twilight of the Gods", "17 August 1876"),
    Opera("wagner", "Tristan and Isolde", "10 June 1865"),
    Opera("wagner", "The Master-Singers of Nuremberg", "21 June 1868"),
    Opera("wagner", "Parsifal", "26 July 1882"),
    Opera("beethoven", "Fidelio", "20 November 1805"),
    Opera("verdi", "Nabucco", "9 March 1842"),
    Opera("verdi", "Ernani", "9 March 1844"),
    Opera("verdi", "Macbeth", "14 March 1847"),
    Opera("verdi", "Il corsaro", "25 October 1848"),
    Opera("verdi", "Rigoletto", "11 March 1851"),
    Opera("verdi", "La traviata", "6 March 1853"),
    Opera("verdi", "Aroldo", "16 August 1857"),
    Opera("verdi", "Macbeth", "21 April 1865"),
    Opera("verdi", "Don Carlos", "11 March 1867"),
    Opera("verdi", "Aida", "24 December 1871"),
    Opera("verdi", "Otello", "5 February 1887"),
    Opera("verdi", "Falstaff", "9 February 1893"),
]


def _get_date(date_str: str) -> date:
    return datetime.date(datetime.strptime(date_str, "%d %B %Y"))


def operas_both_at_premiere(guest: str, composer: str) -> Iterator[str]:
    """Retrieves a list of titles of operas, where the guest and the composer
       could have been together at premiere.

       That is the Opera.author matches the composer passed in, and both guest
       and composer are alive at the time of Opera.date.

       If guest and/or composer are not in the composers dict, raise a
       ValueError

       Args:
       guest (str): one of the composers but not the author of an opera
       composer (str): the author of an opera

       Returns a list (or generator) of titles of operas.
    """
    # Validity check:
    for entity in (guest, composer):
        if entity not in composers:
            raise ValueError(f'"{entity}" not in list of composers.')

    # Operas by composer:
    compositions = [
        (opera.play, _get_date(opera.date))
        for opera in operas if opera.author == composer
    ]

    # Premieres where both could have made it:
    composer_died = _get_date(composers[composer].died)
    guest_born = _get_date(composers[guest].born)
    guest_died = _get_date(composers[guest].died)
    return (
        play for play, dt in compositions
        if (guest_born < dt < guest_died) and dt < composer_died
    )


if __name__ == '__main__':
    pprint(list(operas_both_at_premiere('verdi', 'wagner')))
