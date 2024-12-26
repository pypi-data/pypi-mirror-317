""" Module for transforming input variables to the ADNEX model predictors. """

import numpy as np
import pandas as pd


def transform_input_variables(row: pd.Series) -> pd.Series:
    """
    Transform the input variables to the ADNEX model predictors.

    Parameters
    ----------
    row : pd.Series
        A pandas Series containing the necessary predictors with the expected column names.

    Returns
    -------
    pd.Series
        A pandas Series with the transformed predictors indexed by short variable names.
    """
    ratio = row['max_solid_component'] / row['max_lesion_diameter']

    transformed = {
        'constant': 1,
        'A': row['age'],
        'Log2(C)': np.log2(row['max_lesion_diameter']),
        'D/C': ratio,
        'D/C^2': ratio**2,
        'E': row['more_than_10_locules'],
        'F': row['number_of_papillary_projections'],
        'G': row['acoustic_shadows_present'],
        'H': row['ascites_present'],
        'I': row['is_oncology_center'],
    }

    if 's_ca_125' in row.index:
        transformed['Log2(B)'] = np.log2(row['s_ca_125'])

    return pd.Series(transformed)
