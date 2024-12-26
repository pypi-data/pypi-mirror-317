""" Functions for asserting the validity of input variables. """

from adnex.exceptions import ValidationError
from adnex.validation.utils import _in_range, _is_binary, _is_integer, _is_less_than_or_equal_to_max, _is_non_negative


def _ensure_integer(value: object, var_name: str) -> None:
    if not _is_integer(value):
        raise ValidationError(f"Invalid type for '{var_name}': expected integer, got {type(value).__name__}.")


def _ensure_non_negative(value: int, var_name: str) -> None:
    if not _is_non_negative(value):
        raise ValidationError(f'{var_name}={value} cannot be negative.')


def _ensure_binary(value: int, var_name: str) -> None:
    if not _is_binary(value):
        raise ValidationError(f"Invalid value for '{var_name}': expected 0 or 1, got {value}.")


def _ensure_upper_bounded(value: int, max_value: int, var_name: str) -> None:
    if not _is_less_than_or_equal_to_max(value, max_value=max_value):
        raise ValidationError(f'{var_name}={value} is out of range. Must not exceed {max_value}.')


def _ensure_in_range(value: int, min_value: int, max_value: int, var_name: str) -> None:
    if not _in_range(value, min_value=min_value, max_value=max_value):
        raise ValidationError(f'{var_name}={value} is out of range. Must be between {min_value} and {max_value}.')
