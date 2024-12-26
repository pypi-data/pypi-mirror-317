# fmt: off
# pylint: disable=line-too-long

"""
This module defines the ADNEX model variables and constants.
"""

import pandas as pd

ADNEX_MODEL_VARIABLES = {
    'A': 'age',
    'B': 's_ca_125',
    'C': 'max_lesion_diameter',
    'D': 'max_solid_component',
    'E': 'more_than_10_locules',
    'F': 'number_of_papillary_projections',
    'G': 'acoustic_shadows_present',
    'H': 'ascites_present',
    'I': 'is_oncology_center',
}

REQUIRED_VARIABLES = set(ADNEX_MODEL_VARIABLES.values()) - {'s_ca_125'}


ADNEX_MODEL_CONSTANTS_WITH_CA125 = pd.DataFrame(
    {
        'z_1': [-7.577663, 0.004506, 0.111642, 0.372046, 6.967853, -5.65588, 1.375079, 0.604238, -2.04157, 0.971061, 0.953043],
        'z_2': [-12.276041, 0.017260, 0.197249, 0.873530, 9.583053, -5.83319, 0.791873, 0.400369, -1.87763, 0.452731, 0.452484],
        'z_3': [-14.915830, 0.051239, 0.765456, 0.430477, 10.37696, -5.70975, 0.273692, 0.389874, -2.35516, 1.348408, 0.459021],
        'z_4': [-11.909267, 0.033601, 0.276166, 0.449025, 6.644939, -2.30330, 0.899980, 0.215645, -2.49845, 1.636407, 0.808887],
    },
    index=['constant', 'A', 'Log2(B)', 'Log2(C)', 'D/C', 'D/C^2', 'E', 'F', 'G', 'H', 'I']
)

ADNEX_MODEL_CONSTANTS_WITHOUT_CA125 = pd.DataFrame(
    {
        'z_1': [-7.412534, 0.003489, 0.430701, 7.117925, -5.74135, 1.343699, 0.607211, -2.11885, 1.167767, 0.983227],
        'z_2': [-12.201607, 0.017607, 0.98728, 10.07145, -6.17742, 0.763081, 0.410449, -1.98073, 0.77054, 0.543677],
        'z_3': [-12.826207, 0.045172, 0.759002, 11.83296, -6.64336, 0.316444, 0.390959, -2.94082, 2.691276, 0.929483],
        'z_4': [-11.424379, 0.033407, 0.560396, 7.264105, -2.77392, 0.983394, 0.199164, -2.63702, 2.185574, 0.906249],
    },
    index=['constant', 'A', 'Log2(C)', 'D/C', 'D/C^2', 'E', 'F', 'G', 'H', 'I']
)

ADNEX_MODEL_OUTPUT_CATEGORIES = ['Benign', 'Borderline', 'Stage I cancer', 'Stage II-IV cancer', 'Metastatic cancer']


def get_adnex_model_constants(with_ca125: bool) -> pd.DataFrame:
    """
    Retrieve the ADNEX model coefficients for categories other than benign.

    Parameters
    ----------
    with_ca125 : bool
        Whether to use the model including CA-125.

    Returns
    -------
    pd.DataFrame
        The constants DataFrame for the selected model variant.
    """
    return ADNEX_MODEL_CONSTANTS_WITH_CA125 if with_ca125 else ADNEX_MODEL_CONSTANTS_WITHOUT_CA125
