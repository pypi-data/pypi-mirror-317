"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-15
- Purpose: Main file that is invoked via `python -m exploration`.
    Accepts arguments or prompts the user for which command to execute
    and what file(s) to apply it to. Run `python -m exploration -h` for
    more information. See the `main` module for a Python-based API for
    the same functionality.
"""

from . import main

if __name__ == "__main__":
    main.main()
