""" Functions for filtering and validating input data. """

import pandas as pd

from adnex.exceptions import MissingColumnsError, ValidationError
from adnex.validation.variables import (
    _validate_age,
    _validate_binary_predictors,
    _validate_max_lesion_diameter,
    _validate_max_solid_component,
    _validate_number_of_papillary_projections,
    _validate_s_ca_125,
)
from adnex.variables import REQUIRED_VARIABLES


def validate_input(row: pd.Series) -> None:
    """
    Validate input data for the ADNEX model.

    Checks:
    - No missing or NaN values.
    - Age in correct range.
    - CA-125 (if present) in correct range.
    - max lesion diameter, max solid component, and papillary projections in valid range.
    - Binary predictors are strictly 0 or 1.

    Parameters
    ----------
    row : pd.Series
        Input data row.

    Raises
    ------
    MissingColumnsError
        If required columns are missing.
    ValidationError
        If input validation fails.
    """

    missing_columns = REQUIRED_VARIABLES - set(row.index)
    if missing_columns:
        raise MissingColumnsError(missing_columns)

    # Check for missing values
    if row.isna().any():
        missing_vars = row.index[row.isna()].tolist()
        raise ValidationError(f'The following variables are missing (NaN): {missing_vars}')

    _validate_age(row['age'])
    _validate_max_lesion_diameter(row['max_lesion_diameter'])
    _validate_max_solid_component(row['max_solid_component'], max_lesion_diameter=row['max_lesion_diameter'])
    _validate_number_of_papillary_projections(row['number_of_papillary_projections'])
    _validate_binary_predictors(row)
    if 's_ca_125' in row.index:
        _validate_s_ca_125(row['s_ca_125'])
