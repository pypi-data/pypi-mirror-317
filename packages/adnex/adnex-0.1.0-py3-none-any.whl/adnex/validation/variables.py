""" Functions for validation of input variables. """

import typing

import pandas as pd

from adnex.constraints import MAX_AGE, MAX_CA_125, MAXIMAL_LESION_DIAMETER, MIN_AGE, VALID_PAPILLARY_PROJECTIONS
from adnex.exceptions import ValidationError
from adnex.validation.asserts import (
    _ensure_binary,
    _ensure_in_range,
    _ensure_integer,
    _ensure_non_negative,
    _ensure_upper_bounded,
)
from adnex.validation.utils import _is_less_than_or_equal_to_max


def _validate_age(age: object) -> None:
    var_name = 'age'
    _ensure_integer(age, var_name=var_name)
    age = int(typing.cast(int, age))
    _ensure_non_negative(age, var_name=var_name)
    _ensure_in_range(age, min_value=MIN_AGE, max_value=MAX_AGE, var_name=var_name)


def _validate_max_lesion_diameter(max_lesion_diameter: object) -> None:
    var_name = 'max_lesion_diameter'
    _ensure_integer(max_lesion_diameter, var_name=var_name)
    max_lesion_diameter = int(typing.cast(int, max_lesion_diameter))
    _ensure_non_negative(max_lesion_diameter, var_name=var_name)
    _ensure_upper_bounded(max_lesion_diameter, max_value=MAXIMAL_LESION_DIAMETER, var_name=var_name)


def _validate_max_solid_component(max_solid_component: object, max_lesion_diameter: int) -> None:
    var_name = 'max_solid_component'
    _ensure_integer(max_solid_component, var_name=var_name)
    max_solid_component = int(typing.cast(int, max_solid_component))
    _ensure_non_negative(max_solid_component, var_name=var_name)

    if not _is_less_than_or_equal_to_max(max_solid_component, max_value=max_lesion_diameter):
        raise ValidationError(
            f'{var_name}={max_solid_component} cannot exceed max_lesion_diameter={max_lesion_diameter}.'
        )


def _validate_s_ca_125(s_ca_125: object) -> None:
    var_name = 's_ca_125'
    _ensure_integer(s_ca_125, var_name=var_name)
    s_ca_125 = int(typing.cast(int, s_ca_125))
    _ensure_non_negative(s_ca_125, var_name=var_name)
    _ensure_upper_bounded(s_ca_125, max_value=MAX_CA_125, var_name=var_name)


def _validate_number_of_papillary_projections(number_of_papillary_projections: object) -> None:
    var_name = 'number_of_papillary_projections'
    _ensure_integer(number_of_papillary_projections, var_name=var_name)
    number_of_papillary_projections = int(typing.cast(int, number_of_papillary_projections))
    _ensure_non_negative(number_of_papillary_projections, var_name=var_name)

    if number_of_papillary_projections not in VALID_PAPILLARY_PROJECTIONS:
        raise ValidationError(
            f'{var_name}={number_of_papillary_projections} is invalid. Must be 0, 1, 2, 3, or 4 (4 means > 3).'
        )


def _validate_binary_predictors(row: pd.Series) -> None:
    binary_vars = ['more_than_10_locules', 'acoustic_shadows_present', 'ascites_present', 'is_oncology_center']
    for var in binary_vars:
        _ensure_binary(row[var], var)
