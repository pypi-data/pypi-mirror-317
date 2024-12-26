"""Functionality for converting USD to other currencies."""

# Standard library imports
import time

# Third-party imports
from corny_commons import file_manager
from corny_commons.util import web

SOURCE_URL = "https://open.er-api.com/v6/latest/USD"


def get_new_data() -> dict:
    """Makes a web request to the API and returns the new JSON data."""
    return web.make_request(SOURCE_URL).json()


def update_existing_cache() -> None:
    """Overwrites existing cache that has been updated on the API with the new data."""
    existing_data = file_manager.read_cache("exchange_rates")
    if not existing_data:
        # The cache does not exist
        return
    next_update_time: int = existing_data.get("time_next_update_unix", 0)
    if time.time() > next_update_time:
        file_manager.write_cache("exchange_rates", get_new_data())


def convert(value: float, into: str, frm: str = "USD", digits: int = 2) -> float:
    """Converts the specified value from USD to the given currency.

    Arguments:
        value -- the monetary value to convert.
        to -- the ISO code for the currency to convert to.
        frm -- the ISO code for the currency to convert from (defaults to USD).
        digits -- the number of digits the result should be rounded to (defaults to 2).
        If this is negative, the result won't be rounded."""
    rates: dict[str, int] = get_exchange_rates()
    exchange_rate_to = rates.get(into)
    exchange_rate_from = rates.get(frm)
    if not exchange_rate_to or not exchange_rate_from:
        raise ValueError(f"Unsupported currency: '{into}'")
    result = value * exchange_rate_to / exchange_rate_from
    if isinstance(digits, int) and digits >= 0:
        return round(result, digits)
    return result


def get_exchange_rates() -> dict:
    """Returns the currently cached exchange rate data."""
    update_existing_cache()
    return file_manager.get_cache("exchange_rates", False, get_new_data)[0].get("rates")


def get_currencies() -> list[str]:
    """Returns a list of ISO currency formats that can be used in the `convert()` function."""
    return list(get_exchange_rates().keys())


if __name__ == "__main__":
    try:
        while True:
            raw = input(
                "Type origin currency, target currency and conversion amount...\n> "
            )
            _frm, _to, _value = raw.split(" ", maxsplit=2)
            _result = convert(float(_value), _to, _frm, -1)
            print(f"{_frm} {_value} = {_to} {_result}")
    except KeyboardInterrupt:
        print("...\nGoodbye!")
