""" Test cases for the adnex function. """

from unittest.mock import patch

import pytest

import adnex
from adnex.exceptions import ADNEXModelError


def test_adnex_model_with_nan_ca125(sample_input):
    """Test that adnex runs with NaN CA-125 value."""
    valid_input = sample_input.copy()
    valid_input = valid_input.drop('s_ca_125')
    valid_input['s_ca_125'] = None
    adnex.predict_risks(valid_input)


def test_adnex_model_output(sample_input, expected_output):
    """Test that adnex returns expected probabilities for valid input."""

    calculated_output = adnex.predict_risks(sample_input)

    for key in expected_output.index:
        expected_value = expected_output[key]
        calculated_value = calculated_output[key]

        assert calculated_value == pytest.approx(
            expected_value, abs=0.02
        ), f"Mismatch for '{key}': calculated {calculated_value}, expected {expected_value}"


def test_adnex_model_output_keys(sample_input):
    """Test that adnex returns all required probability keys."""
    probabilities = adnex.predict_risks(sample_input)
    required_keys = [
        'Benign',
        'Borderline',
        'Stage I cancer',
        'Stage II-IV cancer',
        'Metastatic cancer',
    ]
    for key in required_keys:
        assert key in probabilities.index, f"Missing key '{key}' in output probabilities."

    assert 'Malignant' not in probabilities.index, "Output probabilities should not contain 'Malignant'."


def test_adnex_model_output_sum(sample_input):
    """Test that the probabilities sum correctly."""
    probabilities = adnex.predict_risks(sample_input)
    risk_of_cancer = adnex.predict_cancer_risk(sample_input)

    # Malignant should be the sum of its subcategories
    assert risk_of_cancer == pytest.approx(
        probabilities['Borderline']
        + probabilities['Stage I cancer']
        + probabilities['Stage II-IV cancer']
        + probabilities['Metastatic cancer']
    ), 'Malignant probability does not match the sum of its subcategories.'


def test_adnex_unexpected_error(sample_input):
    # Mock the transformation function to raise an exception to simulate an unexpected error
    with patch('adnex.model.transform_input_variables') as mock_transform:
        mock_transform.side_effect = Exception('Unexpected error during transformation')

        # Check that the model raises an ADNEXModelError
        with pytest.raises(ADNEXModelError, match='An unexpected error occurred while processing the ADNEX model.'):
            adnex.predict_risks(sample_input)
