""" Tests for data processing functions. """

import numpy as np
import pandas as pd
import pytest

from adnex.computation import compute_probabilities
from adnex.transformation import transform_input_variables
from adnex.variables import ADNEX_MODEL_OUTPUT_CATEGORIES


def test_transform_input_variables_with_ca125():
    input_data = {
        'age': 50,
        's_ca_125': 100,
        'max_lesion_diameter': 50,
        'max_solid_component': 25,
        'more_than_10_locules': 1,
        'number_of_papillary_projections': 2,
        'acoustic_shadows_present': 0,
        'ascites_present': 1,
        'is_oncology_center': 0,
    }
    row = pd.Series(input_data)
    transformed = transform_input_variables(row)
    assert 'Log2(B)' in transformed.index
    assert transformed['Log2(B)'] == np.log2(100)
    assert transformed['Log2(C)'] == np.log2(50)
    assert transformed['D/C'] == 25 / 50
    assert transformed['constant'] == 1


def test_transform_input_variables_without_ca125():
    input_data = {
        'age': 50,
        # no s_ca_125
        'max_lesion_diameter': 50,
        'max_solid_component': 25,
        'more_than_10_locules': 1,
        'number_of_papillary_projections': 2,
        'acoustic_shadows_present': 0,
        'ascites_present': 1,
        'is_oncology_center': 0,
    }
    row = pd.Series(input_data)
    transformed = transform_input_variables(row)
    assert 'Log2(B)' not in transformed.index
    assert transformed['Log2(C)'] == np.log2(50)


def test_compute_probabilities():
    # Minimal test to ensure probabilities sum to 1
    # We provide a sample transformed_vars that aligns with the expected coefficients
    # In practice, use real transformations from a valid input.

    # For a real test, you'd integrate with transform_input_variables results.
    # Here we assume the model variables are correct and with_ca125=True as example.
    transformed_vars = pd.Series(
        {
            'constant': 1,
            'A': 50,
            'Log2(B)': np.log2(100),
            'Log2(C)': np.log2(50),
            'D/C': 0.5,
            'D/C^2': 0.5**2,
            'E': 1,
            'F': 2,
            'G': 0,
            'H': 1,
            'I': 0,
        }
    )

    probabilities = compute_probabilities(transformed_vars, with_ca125=True)
    assert isinstance(probabilities, pd.Series)
    assert pytest.approx(probabilities.sum()) == 1.0
    for category in ADNEX_MODEL_OUTPUT_CATEGORIES:
        assert category in probabilities.index
