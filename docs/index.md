---
layout: default
---

# ** Disclaimer **

This is not an official product of the [Centers for Medicare and Medicaid
Services (CMS)][1], the [Department of Health and Human Services (HHS)][2],
or [RTI International][3].  This is an open source project to increase the
availability of their public risk adjustment models,

 - [CMS HCC Models][4]
 - [HHS HCC Models][5]


# Introduction

## CMS Model

> The CMS hierarchical condition categories (CMS-HCC) model, implemented in
2004, adjusts Medicare capitation payments to Medicare Advantage health care
plans for the health expenditure risk of their enrollees. Its intended use is
to pay plans appropriately for their expected relative costs. For example, MA
plans that disproportionately enroll the healthy are paid less than they would
have been if they had enrolled beneficiaries with the average risk profile,
while MA plans that care for the sickest patients are paid proportionately more
than if they had enrolled beneficiaries with the average risk profile.
>
> -- <cite>[Evaluation of the CMS-HCC Risk Adjustment Model][6]</cite>

## HHS Model

> Section 1343 of the Affordable Care Act (ACA) of 2010 provides for a program
of risk adjustment for all non-grandfathered plans in the individual and small
group market both inside and outside of the Marketplaces. The ACA directs the
Secretary, in consultation with the states, to establish criteria and methods to
be used in determining the actuarial risk of plans within a state. States
electing to operate a risk adjustment program, or the Department of Health and
Human Services (HHS) on behalf of states not electing to operate a risk
adjustment program,  will  assess  charges  to  plans  that experience lower
than average actuarial risk and use them to make payments to plans that have
higher than average actuarial risk.
>
> -- <cite>[Affordable Care Act Risk Adjustment: Overview, Context, and Challenges][7]</cite>



# Quick Start Guide

The base URL for the API is

 - `galtay.pythonanywhere.com/hcc_risk_models/api/v1.0`


## Overview of all models

 - `<base_url>/models`


Generating a `GET` request to the above URL will return brief model
descriptions,

```bash
curl -X GET galtay.pythonanywhere.com/hcc_risk_models/api/v1.0/models
```

```json
{
  "V2217_79_O1": "CMS-HCC 2017 Midyear Final Model, 79 HCC Variables",
  "V2216_79_O2": "CMS-HCC 2017 Initial Model, 79 HCC Variables",
  "V2216_79_L1": "CMS-HCC 2016 Midyear Final Model, 79 HCC Variables (not implemented yet)",
}
```

## Model details

 - `<base_url>/models/<model_name>`

Appending a model name will return details about the model,


```bash
curl -X GET galtay.pythonanywhere.com/hcc_risk_models/api/v1.0/models/V2216_79_O2
```

```json
{
  "model_name": "V2216_79_O2",
  "model_description": "CMS-HCC 2017 Initial Model, 79 HCC Variables",
  "model_segments": {
    "CFA": "Community Full Benefit Dual Aged",
    "CFD": "Community Full Benefit Dual Disabled",
    "CNA": "Community NonDual Aged",
    "CND": "Community NonDual Disabled",
    "CPA": "Community Partial Benefit Dual Aged",
    "CPD": "Community Partial Benefit Dual Disabled",
    "INS": "Long Term Institutional",
    "NE": "New Enrollees",
    "SNPNE": "SNP New Enrollees"
  },
  "model_coefficients": {
    "CFA_F65_69": 0.425,
    "CFA_F70_74": 0.511,
    "CFA_F75_79": 0.611,
    ...
  },
  "icd_to_hcc_mappings": [
    {
      "assignment_type": "primary",
      "diag_code": "A0103",
      "diag_type": 0,
      "hcc_code": "115"
    },
    {
      "assignment_type": "primary",
      "diag_code": "A0104",
      "diag_type": 0,
      "hcc_code": "39"
    },
    ...
  ],
  "hcc_descriptions": {
    "HCC1": "HIV/AIDS",
    "HCC2": "Septicemia, Sepsis, Systemic Inflammatory Response Syndrome/Shock",
    "HCC6": "Opportunistic Infections",
    "..."
  },
}
```



## Evaluating a risk model.

 - `<base_url>/models/<model_name>/evaluate`

Generating a `POST` request to a model URL with `evaluate` appended to the end
will calculate risk scores.  Patient demographic and dianosis data must be sent
in the body of the request in JSON format.  The data should consist of a list
of patient objects.  Below is an example list with two patients,


```json
[
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
```

An example curl command using the data above is,

```bash
curl -X POST -H "Content-type: application/json" -i galtay.pythonanywhere.com/hcc_risk_models/api/v1.0/models/V2216_79_O2/evaluate -d '[{"pt_id": 1001, "sex": 1, "dob": "1930-8-21", "ltimcaid": 1, "nemcaid": 0, "orec": 2, "diagnoses": [{"diag_code": "A420", "diag_type": 0},{"diag_code": "A4150", "diag_type": 0}]}, {"pt_id": 1002, "sex": 2, "dob": "1927-7-12", "ltimcaid": 0, "nemcaid": 0, "orec": 1, "diagnoses": [{"diag_code": "G030", "diag_type": 0},{"diag_code": "C7410", "diag_type": 0}]}]'
```


This will return a risk adjustment JSON object,

```json
{
  "model_info": {
    "model_description": "CMS-HCC 2017 Initial Model, 79 HCC Variables",
    "model_name": "V2216_79_O2",
    "model_segments": {
      "CFA": "Community Full Benefit Dual Aged",
      "CFD": "Community Full Benefit Dual Disabled",
      "CNA": "Community NonDual Aged",
      "CND": "Community NonDual Disabled",
      "CPA": "Community Partial Benefit Dual Aged",
      "CPD": "Community Partial Benefit Dual Disabled",
      "INS": "Long Term Institutional",
      "NE": "New Enrollees",
      "SNPNE": "SNP New Enrollees"
    }
  },
  "patients": [
    {
      "demographic_data": {
        "age": 86,
        "dob": "1930-08-21",
        "ltimcaid": 1,
        "nemcaid": 0,
        "orec": 2,
        "sex": 1
      },
      "diagnoses_to_hccs": [
        {
          "assign_type": "primary",
          "cc": 115,
          "cc_description": "Pneumococcal Pneumonia, Empyema, Lung Abscess",
          "diag_code": "A420",
          "diag_description": "Pulmonary actinomycosis",
          "diag_type": 0,
          "hcc": 115
        },
        {
          "assign_type": "primary",
          "cc": 2,
          "cc_description": "Septicemia, Sepsis, Systemic Inflammatory Response Syndrome/Shock",
          "diag_code": "A4150",
          "diag_description": "Gram-negative sepsis, unspecified",
          "diag_type": 0,
          "hcc": 2
        }
      ],
      "pt_id": 1001,
      "risk_profiles": {
        "CFA": {
          "demographic_coefficients": {
            "M85_89": 1.0090000000000001
          },
          "diagnosis_coefficients": {
            "HCC115": 0.162,
            "HCC2": 0.596
          },
          "score": 1.767,
          "segment_description": "Community Full Benefit Dual Aged",
          "segment_name": "CFA"
        },
        "CFD": {
          "demographic_coefficients": {},
          "diagnosis_coefficients": {
            "HCC115": 0.049,
            "HCC2": 0.8109999999999999
          },
          "score": 0.86,
          "segment_description": "Community Full Benefit Dual Disabled",
          "segment_name": "CFD"
        },
        "CNA": {
          "demographic_coefficients": {
            "M85_89": 0.6940000000000001
          },
          "diagnosis_coefficients": {
            "HCC115": 0.221,
            "HCC2": 0.455
          },
          "score": 1.37,
          "segment_description": "Community NonDual Aged",
          "segment_name": "CNA"
        },
        "CND": {
          "demographic_coefficients": {},
          "diagnosis_coefficients": {
            "HCC115": 0.128,
            "HCC2": 0.532
          },
          "score": 0.66,
          "segment_description": "Community NonDual Disabled",
          "segment_name": "CND"
        },
        "CPA": {
          "demographic_coefficients": {
            "M85_89": 0.679
          },
          "diagnosis_coefficients": {
            "HCC115": 0.302,
            "HCC2": 0.409
          },
          "score": 1.3900000000000001,
          "segment_description": "Community Partial Benefit Dual Aged",
          "segment_name": "CPA"
        },
        "CPD": {
          "demographic_coefficients": {},
          "diagnosis_coefficients": {
            "HCC115": 0.22,
            "HCC2": 0.41700000000000004
          },
          "score": 0.637,
          "segment_description": "Community Partial Benefit Dual Disabled",
          "segment_name": "CPD"
        },
        "INS": {
          "demographic_coefficients": {
            "LTIMCAID": 0.062,
            "M85_89": 1.129
          },
          "diagnosis_coefficients": {
            "HCC115": 0.067,
            "HCC2": 0.34600000000000003
          },
          "score": 1.604,
          "segment_description": "Long Term Institutional",
          "segment_name": "INS"
        },
        "NE": {
          "demographic_coefficients": {
            "NMCAID_NORIGDIS_NEM85_89": 1.511
          },
          "diagnosis_coefficients": {},
          "score": 1.511,
          "segment_description": "New Enrollees",
          "segment_name": "NE"
        },
        "SNPNE": {
          "demographic_coefficients": {
            "NMCAID_NORIGDIS_NEM85_89": 2.0469999999999997
          },
          "diagnosis_coefficients": {},
          "score": 2.0469999999999997,
          "segment_description": "SNP New Enrollees",
          "segment_name": "SNPNE"
        }
      }
    },
    {
      "demographic_data": {
        "age": 89,
        "dob": "1927-07-12",
        "ltimcaid": 0,
        "nemcaid": 0,
        "orec": 1,
        "sex": 2
      },
      "diagnoses_to_hccs": [
        {
          "assign_type": "primary",
          "cc": 10,
          "cc_description": "Lymphoma and Other Cancers",
          "diag_code": "C7410",
          "diag_description": "Malignant neoplasm of medulla of unspecified adrenal gland",
          "diag_type": 0,
          "hcc": 10
        }
      ],
      "pt_id": 1002,
      "risk_profiles": {
        "CFA": {
          "demographic_coefficients": {
            "F85_89": 0.917,
            "OriginallyDisabled_Female": 0.172
          },
          "diagnosis_coefficients": {
            "HCC10": 0.713
          },
          "score": 1.802,
          "segment_description": "Community Full Benefit Dual Aged",
          "segment_name": "CFA"
        },
        "CFD": {
          "demographic_coefficients": {},
          "diagnosis_coefficients": {
            "HCC10": 0.7609999999999999
          },
          "score": 0.7609999999999999,
          "segment_description": "Community Full Benefit Dual Disabled",
          "segment_name": "CFD"
        },
        "CNA": {
          "demographic_coefficients": {
            "F85_89": 0.664,
            "OriginallyDisabled_Female": 0.244
          },
          "diagnosis_coefficients": {
            "HCC10": 0.677
          },
          "score": 1.585,
          "segment_description": "Community NonDual Aged",
          "segment_name": "CNA"
        },
        "CND": {
          "demographic_coefficients": {},
          "diagnosis_coefficients": {
            "HCC10": 0.6559999999999999
          },
          "score": 0.6559999999999999,
          "segment_description": "Community NonDual Disabled",
          "segment_name": "CND"
        },
        "CPA": {
          "demographic_coefficients": {
            "F85_89": 0.6779999999999999,
            "OriginallyDisabled_Female": 0.126
          },
          "diagnosis_coefficients": {
            "HCC10": 0.667
          },
          "score": 1.471,
          "segment_description": "Community Partial Benefit Dual Aged",
          "segment_name": "CPA"
        },
        "CPD": {
          "demographic_coefficients": {},
          "diagnosis_coefficients": {
            "HCC10": 0.5770000000000001
          },
          "score": 0.5770000000000001,
          "segment_description": "Community Partial Benefit Dual Disabled",
          "segment_name": "CPD"
        },
        "INS": {
          "demographic_coefficients": {
            "F85_89": 0.7490000000000001,
            "ORIGDS": 0.0
          },
          "diagnosis_coefficients": {
            "HCC10": 0.401
          },
          "score": 1.1500000000000001,
          "segment_description": "Long Term Institutional",
          "segment_name": "INS"
        },
        "NE": {
          "demographic_coefficients": {
            "NMCAID_ORIGDIS_NEF85_89": 1.167
          },
          "diagnosis_coefficients": {},
          "score": 1.167,
          "segment_description": "New Enrollees",
          "segment_name": "NE"
        },
        "SNPNE": {
          "demographic_coefficients": {
            "NMCAID_ORIGDIS_NEF85_89": 2.252
          },
          "diagnosis_coefficients": {},
          "score": 2.252,
          "segment_description": "SNP New Enrollees",
          "segment_name": "SNPNE"
        }
      }
    }
  ]
}
```



[1]: https://www.cms.gov
[2]: https://www.hhs.gov
[3]: https://www.rti.org
[4]: https://www.cms.gov/medicare/health-plans/medicareadvtgspecratestats/risk-adjustors.html
[5]: https://www.cms.gov/CCIIO/Resources/Regulations-and-Guidance
[6]: https://www.cms.gov/Medicare/Health-Plans/MedicareAdvtgSpecRateStats/downloads/evaluation_risk_adj_model_2011.pdf
[7]: https://www.cms.gov/mmrr/Downloads/MMRR2014_004_03_a02.pdf
