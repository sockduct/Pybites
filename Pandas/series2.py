'''
In Introducing pandas series and Let's play with pandas series we looked at
creating some simple pandas Series and then we looked at how to retrieve values
and slices of values from the series. In this final bite based on Series we'll
look at some options available to you to change the values of the elements in
the series using some basic maths type manipulation. Then we look at creating
some masks.

Series Maths
We'll start with two bites that perform some maths type manipulation to a
pandas series.

In the first part we write a function that takes a Series, a function (addition,
subtraction, multiplication and division) and an integer value. The task is to
apply the value and the function to each value in the series.

In the second part, instead of applying the function to a series and an integer,
the function is applied to two series. Hint: Keep in mind the indexes of both of
the series.

Series Masks
We'll complete this little mini path on pandas Series by looking at creating
masks. As mentioned in the code comments don't confuse masks in this context
with the pandas.Series.mask
(https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.mask.html).
This is a very powerful and useful method but not what we're looking for here.

For parts three and four we want a Boolean Mask:
In both NumPy and Pandas we can create masks to filter data. Masks are ’Boolean’
arrays – that is arrays of true and false values and provide a powerful and
flexible method to selecting data.

For the third part of this bite we simply need to create a mask to filter
certain letters from a series of letters. You don't need to worry about case or
anything like that (anyhow changing case is changing the contents of the series
so probably wouldn't want to do that).

As per Computer Software for Quartiles
(https://en.wikipedia.org/wiki/Quartile#Computer_Software_for_Quartiles): The
Excel function QUARTILE(array, quart) provides the desired quartile value for a
given array of data. In the Quartile function, array is the dataset of numbers
that is being analyzed and quart is any of the following 5 values depending on
which quartile is being calculated, e.g.,

| Quart |      Output QUARTILE Value       |
| :---: | :------------------------------: |
|   0   |          Minimum value           |
|   1   | Lower Quartile (25th percentile) |
|   2   |              Median              |
|   3   | Upper Quartile (75th percentile) |
|   4   |          Maximum value           |

For this part not only do we want the Median (the 50th percentile or second
quartile value), we also want the mean value. The requirement is to take a
series of floats and return all values in the series that are within the given
range. So for this you need to create a mask on which to filter the series,
apply the mask and then return the series result.

Of course these snippets are not all as easy and straight forward as they seem.
You'll need to refer to the docstrings and the tests to really fully understand
the requirements.
'''

from collections import defaultdict

import pandas as pd


def series_simple_math(ser: pd.Series, function: str, number: int) -> pd.Series:
    """Write some simple math helper functions for series.
    Take the given series, perform the required operation and return the new
    series.  For example. Give the series:
        0    0
        1    1
        2    2
        dtype: int64

    Function 'add' and 'number' 2 you should return
        0     2
        1     3
        2     4
        dtype: int64

    :param ser: Series to perform operation on
    :param function: The operation to perform
    :param number: The number to apply the operation to
    """
    match function:
        case 'add':
            return ser + number
        case 'sub':
            return ser - number
        case 'mul':
            return ser * number
        case 'div':
            return ser / number
        case _:
            raise ValueError(f'Expected function type of add/sub/mul/div, not:  {function}')


def complex_series_maths(ser_01: pd.Series, ser_02: pd.Series, function: str) -> pd.Series:
    """Write some math helper functions for series.
    Take the two given series, perform the required operation and return the new
    series.  For example. Give the series:
        0    0
        1    1
        2    2
        dtype: int64

    And the series:
        0     2
        1     3
        2     4
        dtype: int64

    If the function given is 'add' you should return
        0     2
        1     4
        2     6
        dtype: int64

    :param ser_01: Primary series to perform operation on
    :param ser_02: Secondary series to perform operation on
    :param function: The operation to perform

    Note:
    For this function always add ser_02 to ser_01,
        subtract ser_02 from ser_01,
        multiply ser_01 by ser_02,
        divide ser_01 by ser_02
    Don't worry about None's and NaN and divide by zero.
        Let pandas do the work for you.
    """
    match function:
        case 'add':
            return ser_01 + ser_02
        case 'sub':
            return ser_01 + ser_02
        case 'mul':
            return ser_01 * ser_02
        case 'div':
            return ser_01 / ser_02
        case _:
            raise ValueError(f'Expected function type of add/sub/mul/div, not:  {function}')


def create_series_mask(ser: pd.Series, mask: list) -> pd.Series:
    """Write a trivial function to create a pandas series mask of a list
    of letters.
    Be careful, although this sounds very similar to the .mask() method,
        that's not what we're looking for here.
    For example. Give the series x:
        0    0
        1    1
        2    2
        3    3
        4    4
        dtype: int64

    You can create a mask for even numbers like this:
    >>> mask = x % 2 == 0
    >>> mask
        0     True
        1    False
        2     True
        3    False
        4     True
        dtype: bool

    And then apply the mask:
    >>> x[mask]
        0    0
        2    2
        4    4
        dtype: int64

    Of course for simpler masks you can just do this:
    >>> x[x % 2 == 0]
        0    0
        2    2
        4    4
        dtype: int64

    :param ser: Series to perform operation on
    :param mask: The list of letters to be masked
    """
    mapping = defaultdict(bool, dict.fromkeys(mask, True))
    return ser.map(mapping)


def custom_series_function(ser: pd.Series, within: float) -> pd.Series:
    """A more challenging mask to apply.
    When passed a series of floats, return all values
        within the given rage of:
         - the minimum value
         - the 1st quartile value
         - the second quartile value
         - the mean
         - the third quartile value
         - the maximum value
    You may want to brush up on some simple statistics to help you here.
    Also, the series is passed to you sorted ascending.
        Be sure that you don't return values out of sequence.

    So, for example if your mean is 5.0 and within is 0.1
        return all values between 4.9 and 5.1 inclusive

    :param ser: Series to perform operation on
    :param within: The value to calculate the range of number within
    """
    get_mask = lambda ser, loc, stats: ser.between(
        stats.loc[loc] - within, stats.loc[loc] + within, inclusive='both'
    )

    stats = ser.describe()
    final_mask = pd.Series(False, index=ser.index)
    for mask in ('min', '25%', '50%', 'mean', '75%', 'max'):
        final_mask = final_mask | get_mask(ser, mask, stats)

    return ser[final_mask]
