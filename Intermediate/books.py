#! /usr/bin/env python3.13
'''
In this Bite you are going to look at a list of Book namedtuples and sort them
by various criteria. Complete the 4 functions below. Consider using lambda and/
or one or more helper functions and/or attrgetter (operator module). Good luck
and have fun!
'''


from operator import attrgetter
from typing import NamedTuple


class Book(NamedTuple):
    title: str
    authors: str
    pages: int
    published: str


BOOKS = [
    Book(title="Python Interviews",
         authors="Michael Driscoll",
         pages=366,
         published="2018-02-28"),
    Book(title="Python Cookbook",
         authors="David Beazley, Brian K. Jones",
         pages=706,
         published="2013-05-10"),
    Book(title="The Quick Python Book",
         authors="Naomi Ceder",
         pages=362,
         published="2010-01-15"),
    Book(title="Fluent Python",
         authors="Luciano Ramalho",
         pages=792,
         published="2015-07-30"),
    Book(title="Automate the Boring Stuff with Python",
         authors="Al Sweigart",
         pages=504,
         published="2015-04-14"),
]
#
# To maintain original design:
books = BOOKS


# All functions return books sorted in ascending order:
def sort_books_by_len_of_title(books: list[Book]=BOOKS) -> list[Book]:
    """
    Expected last book in list:
    Automate the Boring Stuff with Python
    """
    return sorted(books, key=lambda book: len(book.title))


def sort_books_by_first_authors_last_name(books: list[Book]=BOOKS) -> list[Book]:
    """
    Expected last book in list:
    Automate the Boring Stuff with Python
    """
    return sorted(books, key=lambda book: book.authors.split(',')[0].split()[1])


def sort_books_by_number_of_page(books: list[Book]=BOOKS) -> list[Book]:
    """
    Expected last book in list:
    Fluent Python
    """
    # return sorted(books, key=lambda book: book.pages)
    # Better solution:
    return sorted(books, key=attrgetter('pages'))


def sort_books_by_published_date(books: list[Book]=BOOKS) -> list[Book]:
    """
    Expected last book in list:
    Python Interviews
    """
    # Could parse out datetime for sorting, but not necessary the way its formatted
    # return sorted(books, key=lambda book: book.published)
    return sorted(books, key=attrgetter('published'))


def display(books: Book|list[Book]) -> str:
    if not isinstance(books, Book):
        # list of Books:
        return '* ' + '\n* '.join(
            ', '.join(
                f'{field.title()}: {getattr(book, field)}' for field in book._fields
            )
            for book in books
        )

    # Single Book:
    book = books
    return '* ' + ', '.join(f'{field.title()}: {getattr(book, field)}' for field in book._fields)


if __name__ == '__main__':
    for func in ('sort_books_by_len_of_title', 'sort_books_by_first_authors_last_name',
                 'sort_books_by_number_of_page', 'sort_books_by_published_date'):
        print(f'Invoking {func}:\n{display(globals()[func]())}\n')
