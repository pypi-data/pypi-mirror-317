""" This module contains the main function to apply the ADNEX model to a single patient data row. """

import pandas as pd

from adnex.computation import compute_probabilities
from adnex.exceptions import ADNEXModelError, MissingColumnsError, ValidationError
from adnex.transformation import transform_input_variables
from adnex.validation.core import validate_input
from adnex.validation.utils import has_ca125
from adnex.variables import ADNEX_MODEL_VARIABLES


def predict_risks(row: pd.Series) -> pd.Series:
    """
    Apply the ADNEX model to a single patient data row.

    Parameters
    ----------
    row : pd.Series
        A pandas Series containing the necessary predictors with the expected column names.

    Raises
    ------
    MissingColumnsError
        If required columns are missing or input validation
    ValidationError
        If input validation fails.
    ADNEXModelError
        If an unexpected error occurs during model computation.

    Returns
    -------
    pd.Series
        A pandas Series with probabilities for each outcome category:
        ['Benign', 'Borderline', 'Stage I cancer', 'Stage II-IV cancer', 'Metastatic cancer'].
    """
    try:
        with_ca125 = has_ca125(row)

        # Keep only necessary columns
        variables_to_use = list(ADNEX_MODEL_VARIABLES.values())
        filtered_row = row.drop(index=row.index.difference(variables_to_use))

        # Adjust the variables to use based on the presence of CA-125
        if not with_ca125 and 's_ca_125' in filtered_row:
            filtered_row = filtered_row.drop('s_ca_125')

        # Validate the input data
        validate_input(filtered_row)

        # Transform the input variables
        transformed_vars = transform_input_variables(filtered_row)

        # Compute probabilities
        probabilities = compute_probabilities(transformed_vars, with_ca125)

        return probabilities

    except (MissingColumnsError, ValidationError):
        raise  # Re-raise the same exception to preserve specificity

    except Exception as e:
        raise ADNEXModelError('An unexpected error occurred while processing the ADNEX model.') from e


def predict_cancer_risk(row: pd.Series) -> float:
    """
    Apply the ADNEX model to a single patient data row and return the risk of cancer.

    The risk of cancer is defined as the sum of the probabilities of the non-benign categories:
    'Borderline', 'Stage I cancer', 'Stage II-IV cancer', 'Metastatic cancer'.


    Parameters
    ----------
    row : pd.Series
        A pandas Series containing the necessary predictors with the expected column names.

    Returns
    -------
    float
        The risk of cancer as a float value between 0 and 1.
    """
    probabilities = predict_risks(row)

    return probabilities.sum() - probabilities['Benign']
