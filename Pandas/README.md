# Pandas README

## The Pandas library and docs

* [Pandas](https://pandas.pydata.org) data analysis library
* [Docs](https://pandas.pydata.org/docs/)
  * [API Reference](https://pandas.pydata.org/docs/reference/index.html#api)
  * [Getting Started](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)
  * [User Guide](https://pandas.pydata.org/docs/user_guide/index.html#user-guide)

## Usage notes

* Overview
  * Series:

    ```python
    se = pandas.Series(range(5), index=list('abcde'))

    se
    a    0
    b    1
    c    2
    d    3
    e    4
    dtype: int64
    ```

  * Terminology
    * data or values (i.e., range(5) from above)
    * axis labels (i.e., index=list('abcde') from above)
  * Indexing
    * Label based - use axis label(s):
      * Use single label, list of labels, or slice of labels
        * Note:  slicing with .loc includes the end (in contrast to Python!)
    * Position based - integer offset into data:
      * Same as above, but slicing does not include the end (like Python)
  * Example indexing:

    ```python
    se.loc[1:3]  =>  TypeError!

    se.loc['b':'d']
    b    1
    c    2
    d    3
    dtype: int64

    # Can also do this, but prefer .loc:
    se[1:3]
    b    1
    c    2
    dtype: int64
    # Warning:  With integer indexes, this can behave differently than expected

    se.iloc[1:3]
    b    1
    c    2
    dtype: int64

    se.iloc['b':'d']  =>  TypeError!
    ```
