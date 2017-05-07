import pandas
import hcc_risk_models as hrm


def model_2017_final():

    model = 'V2217_79_O1'

    demographics = pandas.DataFrame({
        'pt_id': [1001, 1002],
        'sex': [1, 2],
        'dob': ['1930-8-21', '1927-7-12'],
        'ltimcaid': [1, 0],
        'nemcaid': [0, 0],
        'orec': [2, 1],
    })

    diagnoses = pandas.DataFrame({
        'pt_id': [1001, 1001, 1002, 1002],
        'diag_code': ['A420', 'A4150', 'G030', 'C7410'],
        'diag_type': [0, 0, 0, 0],
    })

    result = hrm.evaluate_model(model, demographics, diagnoses)
    return result


def model_2017_midyear():

    model = 'V2216_79_O2'

    demographics = pandas.DataFrame({
        'pt_id': [1001, 1002],
        'sex': [1, 2],
        'dob': ['1930-8-21', '1927-7-12'],
        'ltimcaid': [1, 0],
        'nemcaid': [0, 0],
        'orec': [2, 1],
    })

    diagnoses = pandas.DataFrame({
        'pt_id': [1001, 1001, 1002, 1002],
        'diag_code': ['A420', 'A4150', 'G030', 'C7410'],
        'diag_type': [0, 0, 0, 0],
    })

    result = hrm.evaluate_model(model, demographics, diagnoses)
    return result


if __name__ == '__main__':
    results_v2217_79_O1 = model_2017_final()
    results_v2216_79_O2 = model_2017_midyear()
