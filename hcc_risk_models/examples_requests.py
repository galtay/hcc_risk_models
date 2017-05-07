import json
import requests

base_url = 'https://galtay.pythonanywhere.com/hcc_risk_models/api/v1.0/models'

url = base_url
print('url: ', url)
result_models = requests.get(url)
print('result_models: ', json.dumps(result_models.json(), indent=2))
print()

model = 'V2217_79_O1'
url = '{}/{}'.format(base_url, model)
print('url: ', url)
result_model = requests.get(url)
print('result_model (keys): ', result_model.json().keys())
print


patients = [
    {
        "pt_id": 1001,
        "sex": 1,
        "dob": "1930-8-21",
        "ltimcaid": 1,
        "nemcaid": 0,
        "orec": 2,
        "diagnoses": [
            {
                "diag_code": "A420",
                "diag_type": 0
            },
            {
                "diag_code": "A4150",
                "diag_type": 0
            }
        ]
    },
    {
        "pt_id": 1002,
        "sex": 2,
        "dob": "1927-7-12",
        "ltimcaid": 0,
        "nemcaid": 0,
        "orec": 1,
        "diagnoses": [
            {
                "diag_code": "G030",
                "diag_type": 0
            },
            {
                "diag_code": "C7410",
                "diag_type": 0
            }
        ]
    }
]


url = '{}/{}/evaluate'.format(base_url, model)
print('url: ', url)
result_risk = requests.post(url, json=patients)
