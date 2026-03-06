# Testing README

## Running pytest

* Standard:
  `pytest -v`

* Include current working directory:
  * Option 1:

    ```PowerShell
    $env:PYTHONPATH='.'
    ```

  * Option 2:

    ```python
    # Within test file:
    import sys

    # Make local module imports stable when tests are run from cwd:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ```

## Test coverage

* CLI only (preferred):

  ```PowerShell
  pytest -q --cov=<TARGET_SCRIPT> --cov-report=term-missing <TARGET_TEST_SCRIPT>.py
  ```

* CLI only, suppress warnings for older versions:

  ```PowerShell
  pytest -q --cov=account --cov-report=term-missing `
      -W "ignore:.*currentThread.*:DeprecationWarning:coverage\\.pytracer" `
      -W "ignore:.*co_lnotab.*:DeprecationWarning:coverage\\.parser"

  # Or permanently in pytest.ini:
  [pytest]
  filterwarnings =
      ignore:.*currentThread.*:DeprecationWarning:coverage\.pytracer
      ignore:.*co_lnotab.*:DeprecationWarning:coverage\.parser
  ```

* HTML:

  ```PowerShell
  pytest -q --cov=<TARGET_SCRIPT> --cov-report=term-missing --cov-report=html `
      <TARGET_TEST_SCRIPT1>.py <TARGET_TEST_SCRIPT2>.py
  ```
