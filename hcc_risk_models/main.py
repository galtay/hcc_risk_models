import argparse
from hcc_risk_models.v2217_79_O1 import risk_model as v2217_79_O1
from hcc_risk_models.v2216_79_O2 import risk_model as v2216_79_O2


model_v2217_79_O1 = v2217_79_O1.V2217_79_O1()
model_v2216_79_O2 = v2216_79_O2.V2216_79_O2()


VALID_MODEL_DESCRIPTIONS = {
    'V2217_79_O1': 'CMS-HCC 2017 Midyear Final Model, 79 HCC Variables',
    'V2216_79_O2': 'CMS-HCC 2017 Initial Model, 79 HCC Variables',
}


def evaluate_model(model, demographics, diagnoses, do_sedits=False, date_asof=None):
    """Evaluate a risk model for every person in the `demographics` DataFrame

        The demographics DataFrame has one row per person.  Different
        models require different column names in the DataFrame.

        The diagnoses DataFrame has one row per diagnosis. All models should
        provide a unique patient identifier, a diagnosis code, and a diagnosis
        type (i.e. ICD-9 or ICD-10)

          pt_id     - arbitrary unique identifier (e.g. HICN).
          diag_code - ICD-9 or ICD-10 diagnosis code with no periods
          diag_type - 9 for ICD-9 codes, 0 for ICD-10 codes

    """

    if model not in VALID_MODEL_DESCRIPTIONS:
        raise ValueError(
            'model must be one of: {}'.format(VALID_MODEL_DESCRIPTIONS.keys()))

    if model == 'V2217_79_O1':
        model = model_v2217_79_O1

    elif model == 'V2216_79_O2':
        model = model_v2216_79_O2

    else:
        raise ValueError('model must be one of {}'.format(
            list(VALID_MODEL_DESCRIPTIONS)))


    result = model.evaluate_risk(
        demographics, diagnoses, do_sedits=do_sedits, date_asof=date_asof)

    return result
