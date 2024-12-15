#! /usr/bin/env python3.13


from functools import wraps
from typing import Any, Callable, TypeVar


# Types:
FuncT = TypeVar('FuncT', bound=Callable[..., Any])


# def make_html(element: str) -> function:
def make_html(element: str) -> Callable[..., Any]:
    '''
    Decorator function with argument
    * Wraps text inside one or more HTML tags
    '''

    # Inner functions:
    # def decorator(func: FuncT) -> FuncT:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def process(*args: tuple[Any, ...], **kwargs:dict[str, Any]) -> str:
            return f'<{element}>{func(*args, **kwargs)}</{element}>'

        return process

    return decorator


@make_html('p')
@make_html('strong')
def get_text(text: str='Example input string') -> str:
    return text


if __name__ == '__main__':
    '''
    Example:
    @make_html('p')
    @make_html('strong')
    def get_text(text='I code with PyBites'):
        return text

    get_text() => <p><strong>I code with PyBites</strong></p>

    Notes:
    * Recall that:
      @decorate
      def target():
          ...

      Equivalent to:  target = decorate(target)
    * Decorators run at import time (vs. runtime)
    '''
    print(get_text())
