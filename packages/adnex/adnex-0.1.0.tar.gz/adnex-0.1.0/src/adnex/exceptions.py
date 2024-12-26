""" Custom exceptions for the ADNEX model. """

from typing import Set


class ADNEXModelError(Exception):
    """Base exception for ADNEX model errors."""


class ValidationError(ADNEXModelError):
    """Exception raised for input validation errors."""


class MissingColumnsError(ADNEXModelError):
    """Exception raised when required columns are missing."""

    def __init__(self, missing_columns: Set[str]) -> None:
        message_template = 'The input row is missing required columns: {}.'
        # Sort the missing columns for consistent orderin
        if len(missing_columns) > 1:
            sorted_missing = sorted(missing_columns)
            missing_cols_str = '{' + ', '.join(f"'{col}'" for col in sorted_missing) + '}'
            message = message_template.format(missing_cols_str)
        else:
            message = message_template.format(f"'{list(missing_columns)[0]}'")

        super().__init__(message)
