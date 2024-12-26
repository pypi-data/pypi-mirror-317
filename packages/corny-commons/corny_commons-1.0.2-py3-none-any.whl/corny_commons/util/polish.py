"""Functionality for conjugating words in Polish."""


def conjugate_numeric(
    num: int, word: str, suffix_sing: str = "ę", suffix_a: str = "y", suffix_b: str = ""
) -> str:
    """Inputs a number and base noun and returns the correctly conjugated string in Polish.

    Arguments:
        num -- the quantity, integer
        word -- the base noun, e.g. 'godzin' or 'minut'
        suffix_sing -- the suffix to use when the quantity is 1
        suffix_a -- the suffix to use when the quantity ends in a digit from 2 to 4
        suffix_b -- the suffix to use otherwise, as well as in the exception cases of 12 through 14
    """
    if num == 1:
        suffix = suffix_sing
    else:
        last_digit: int = int(str(num)[-1])
        if 1 < last_digit < 5 and not 12 <= num <= 14:
            suffix = suffix_a
        else:
            suffix = suffix_b
    return f"{num} {word}{suffix}"
