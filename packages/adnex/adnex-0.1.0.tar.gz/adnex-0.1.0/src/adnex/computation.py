""" Module for computing probabilities using the ADNEX model. """

import numpy as np
import pandas as pd

from adnex.variables import ADNEX_MODEL_OUTPUT_CATEGORIES, get_adnex_model_constants


def compute_probabilities(transformed_vars: pd.Series, with_ca125: bool) -> pd.Series:
    """
    Compute the outcome probabilities using the transformed predictors and the ADNEX coefficients.

    Parameters
    ----------
    transformed_vars : pd.Series
        Series of transformed predictors indexed by short variable names.
    with_ca125 : bool
        Whether CA-125 was included in the model.

    Returns
    -------
    pd.Series
        Probabilities for each outcome class.
    """
    # Retrieve model constants
    constants = get_adnex_model_constants(with_ca125)

    # Ensure ordering
    transformed_vars = transformed_vars.reindex(constants.index)

    # Calculate z-values for each non-benign category
    z_values = constants.T @ transformed_vars

    # Compute exp(z) for each category
    exp_z_values = np.exp(z_values)

    # Prepend 1 for the benign category
    exp_z_values = np.insert(exp_z_values, 0, 1)

    # Compute probabilities
    probabilities = exp_z_values / exp_z_values.sum()

    probabilities_series = pd.Series(probabilities, index=ADNEX_MODEL_OUTPUT_CATEGORIES)

    return probabilities_series
