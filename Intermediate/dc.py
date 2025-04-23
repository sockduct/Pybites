#! /usr/bin/env python3.13
'''
As you might have noticed we are now on Python 3.7 so time for a Bite on data
classes which were introduced with PEP 557.

What are they? Raymond Hettinger summarized it nicely in his great talk:
a mutible named tuple with defaults.

One advantage is the code it saves you typing so they might become an essential
part of your Python toolkit!

In this Bite we have you write a data class called Bite that managed 3
attributes: number, title, and level. Their types are int, str and str
respectively.

There are 3 more requirements:
*   title needs to be capitalized upon instantiation (you get a hint in the
    tests for this one :) - make sure to read the tests for additional specs,
    including some of the differences between data classes and namedtuples!)
*   level takes a default argument of Beginner.
*   A collection of Bite instances needs to be orderable (using sort / sorted -
    this is not by default but configurable ...)

Good luck and keep up with the language, exciting new things are getting added!
On that note feel free to make us more Bite requests via our Bites homepage
(you'll find a form per Bite level at the bottom of the page ...)

For more resources on data classes we recommned watching Hettinger's talk as
well as reading through Anthony Shaw's A brief tour of Python 3.7 data classes.
Have fun!
'''


from dataclasses import dataclass


@dataclass(order=True)
class Bite:
    number: int
    title: str
    level: str='Beginner'

    def __post_init__(self) -> None:
        self.title = self.title.capitalize()


if __name__ == '__main__':
    print(Bite(4, 'testing'))
