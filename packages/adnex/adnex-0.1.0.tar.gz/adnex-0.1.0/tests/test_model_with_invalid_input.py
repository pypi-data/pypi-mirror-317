""" Test cases for the adnex function. """

import pytest

import adnex
from adnex.exceptions import MissingColumnsError, ValidationError
from adnex.validation.variables import MAX_AGE, MAX_CA_125, MIN_AGE


def test_adnex_model_missing_required_columns(sample_input):
    """Test that MissingColumnsError is raised when required columns are missing."""
    # Remove multiple required columns
    input_data = sample_input.drop(labels=['age', 'max_lesion_diameter'])

    with pytest.raises(MissingColumnsError) as excinfo:
        adnex.predict_risks(input_data)

    assert 'missing required columns' in str(excinfo.value), 'MissingColumnsError not raised for missing columns.'


def test_adnex_model_invalid_age_type(sample_input):
    """Test that ValidationError is raised when age is not an integer."""
    var_name = 'age'
    input_data = sample_input.copy()
    age = input_data[var_name]
    del input_data[var_name]
    input_data[var_name] = age.astype(str)

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f"Invalid type for '{var_name}': expected integer, got str_." in str(
        excinfo.value
    ), f'ValidationError not raised for non-integer {var_name}.'


def test_adnex_model_age_out_of_range(sample_input):
    """Test that ValidationError is raised when age is out of valid range."""
    var_name = 'age'
    value = MAX_AGE + 1
    input_data = sample_input.copy()
    input_data[var_name] = value

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f'{var_name}={value} is out of range. Must be between {MIN_AGE} and {MAX_AGE}.' in str(
        excinfo.value
    ), 'ValidationError not raised for age out of range.'


def test_adnex_model_invalid_ca_125_type(sample_input):
    """Test that ValidationError is raised when CA-125 is not and integer."""
    var_name = 's_ca_125'
    input_data = sample_input.copy()
    del input_data[var_name]
    input_data[var_name] = 'sixty-eight'  # Invalid type

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f"Invalid type for '{var_name}': expected integer, got str." in str(
        excinfo.value
    ), f'ValidationError not raised for non-integer {var_name}.'


def test_adnex_model_ca_125_out_of_range(sample_input):
    """Test that ValidationError is raised when s_ca_125 is out of valid range."""
    var_name = 's_ca_125'
    value = MAX_CA_125 + 1
    input_data = sample_input.copy()
    input_data[var_name] = value  # Invalid CA-125

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f'{var_name}={value} is out of range. Must not exceed {MAX_CA_125}.' in str(
        excinfo.value
    ), f'ValidationError not raised for {var_name} out of range.'


def test_adnex_model_ca_125_negative(sample_input):
    """Test that ValidationError is raised when s_ca_125 is negative."""
    var_name = 's_ca_125'
    value = -1
    input_data = sample_input.copy()
    input_data[var_name] = value  # Invalid negative CA-125

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f'{var_name}={value} cannot be negative.' in str(
        excinfo.value
    ), f'ValidationError not raised for negative {var_name}.'


def test_adnex_model_invalid_papillary_projections(sample_input):
    """Test that ValidationError is raised when number_of_papillary_projections is invalid."""
    var_name = 'number_of_papillary_projections'
    value = 5
    input_data = sample_input.copy()
    input_data[var_name] = value  # Invalid value (should be 0-4)

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f'{var_name}={value} is invalid. Must be 0, 1, 2, 3, or 4 (4 means > 3).' in str(
        excinfo.value
    ), f'ValidationError not raised for invalid {var_name}.'


def test_adnex_model_invalid_binary_variable(sample_input):
    """Test that ValidationError is raised when a binary variable has an invalid value."""
    var_name = 'ascites_present'
    value = 2
    input_data = sample_input.copy()
    input_data[var_name] = value  # Invalid binary value

    with pytest.raises(ValidationError) as excinfo:
        adnex.predict_risks(input_data)

    assert f"Invalid value for '{var_name}': expected 0 or 1, got {value}." in str(
        excinfo.value
    ), 'ValidationError not raised for invalid binary predictor value.'
