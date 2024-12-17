#! /usr/bin/env python3.13


from functools import wraps
from typing import Any, Callable, TypeVar


# Types:
FuncT = TypeVar('FuncT', bound=Callable[..., Any])


# Not return type of function but of Callable[..., Any]:
def make_html(element: str) -> Callable[..., Any]:
    '''
    Decorator function with argument
    * Wraps text inside one or more HTML tags
    '''

    # Inner functions:
    # Tried this:  def decorator(func: FuncT) -> FuncT:
    # But get error from mypy, expected:
    # * _Wrapped[
    #            [VarArg(Any), KwArg(Any)], Any,
    #            [VarArg(tuple[Any, ...]), KwArg(dict[str, Any])], str
    #   ]
    # Not quite sure how to do that...
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        # Alternatively:  def wrapper(...)
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
