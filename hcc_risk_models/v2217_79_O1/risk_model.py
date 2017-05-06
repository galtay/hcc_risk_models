"""
Model Class for V2217_79_O1
2017 Midyear Final Model, 79 HCC Variables
"""


import os
import json
import datetime

import pandas
from dateutil import relativedelta

from hcc_risk_models.icd_descriptions import icd10cm_descriptions_2017

from hcc_risk_models.common import agesexv2
from hcc_risk_models.common import v22h79l1
from hcc_risk_models.common import v22h79h1
from hcc_risk_models.common import v22i0ed1

from hcc_risk_models.common.formats import f2217o1p
from hcc_risk_models.v2217_79_O1 import regression_variables as rv



PATH_HERE = os.path.realpath(__file__)
DIR_HERE = os.path.split(PATH_HERE)[0]
COEFFICIENTS_FILE = os.path.join(DIR_HERE, '../common/coefficients/C2214O5P.csv')
FORMATS_FILE = os.path.join(DIR_HERE, '../common/formats/F2217O1P.csv')



class ResultEncoder(json.JSONEncoder):
    """A JSON encoder to handle numpy types"""
    def default(self, obj):
        if isinstance(obj, pandas.np.int64):
            return int(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)




class V2217_79_O1:

    SEGMENT_NAMES = ['CNA', 'CND', 'CFA', 'CFD',
                     'CPA', 'CPD', 'INS', 'NE',  'SNPNE']

    SEGMENT_DESCRIPTIONS = {
        'CNA':   'Community NonDual Aged',
        'CND':   'Community NonDual Disabled',
        'CFA':   'Community Full Benefit Dual Aged',
        'CFD':   'Community Full Benefit Dual Disabled',
        'CPA':   'Community Partial Benefit Dual Aged',
        'CPD':   'Community Partial Benefit Dual Disabled',
        'INS':   'Long Term Institutional',
        'NE':    'New Enrollees',
        'SNPNE': 'SNP New Enrollees',
    }

    SEGMENT_PREDICTORS = {
        'CNA':   rv.COMM_REGA,
        'CND':   rv.COMM_REGD,
        'CFA':   rv.COMM_REGA,
        'CFD':   rv.COMM_REGD,
        'CPA':   rv.COMM_REGA,
        'CPD':   rv.COMM_REGD,
        'INS':   rv.INST_REG,
        'NE':    rv.NE_REG,
        'SNPNE': rv.NE_REG
    }

    NAME = 'V2217_79_O1'
    DESCRIPTION = 'CMS-HCC 2017 Midyear Final Model, 79 HCC Variables'

    FORMATS = f2217o1p.HccFormats(FORMATS_FILE)
    COEFFICIENTS = pandas.read_csv(COEFFICIENTS_FILE).iloc[0]
    HCC_DESCRIPTIONS = v22h79l1.HCC_DESCRIPTIONS

    REQUIRED_DEMOGRAPHICS_COLUMNS = ['pt_id', 'sex', 'dob', 'ltimcaid', 'nemcaid', 'orec']
    REQUIRED_DIAGNOSES_COLUMNS = ['pt_id', 'diag_code', 'diag_type']

    JSON_ENCODER = ResultEncoder
    ICD10_DEFS = icd10cm_descriptions_2017.Icd10CmDefinitions()


    def __init__(self):
        pass

    def input_json_to_dataframes(self, input_json):
        """Transform API input JSON to DataFrames

        We expect a list of patient objects.  each patient object has the form,
          {
            "pt_id": 1001,
            "sex": 1,
            "dob": "1930-8-21",
            "ltimcaid": 1,
            "nemcaid": 0,
            "orec": 2,
            "diagnoses": [
              {"diag_code": "A420", "diag_type": 0},
              {"diag_code": "A4150", "diag_type": 0},
              ...
            ]
          }
        """
        demographics_keys = self.REQUIRED_DEMOGRAPHICS_COLUMNS
        demographics = {key: [] for key in demographics_keys}

        diagnoses_keys = self.REQUIRED_DIAGNOSES_COLUMNS
        diagnoses = {key: [] for key in diagnoses_keys}

        for blob in input_json:
            for key in self.REQUIRED_DEMOGRAPHICS_COLUMNS:
                demographics[key].append(blob[key])
                if key == 'pt_id':
                    pt_id = blob[key]

            for diag_obj in blob['diagnoses']:
                diagnoses['pt_id'].append(pt_id)
                for key in ['diag_code', 'diag_type']:
                    diagnoses[key].append(diag_obj[key])

        demographics = pandas.DataFrame(demographics)
        diagnoses = pandas.DataFrame(diagnoses)

        return demographics, diagnoses


    def validate_demographics(self, demographics):
        """Validate a `demographics` DataFrame"""
        missing_cols = set(self.REQUIRED_DEMOGRAPHICS_COLUMNS) - set(demographics.columns)
        if len(missing_cols) > 0:
            raise ValueError(
                'demographics DataFrame missing the following required columns {}'
                .format(list(missing_cols)))

        if demographics['pt_id'].nunique() != demographics.shape[0]:
            raise ValueError('demographics has duplicate pt_id values')


    def validate_diagnoses(self, diagnoses):
        """Validate a `diagnoses` DataFrame"""
        missing_cols = set(self.REQUIRED_DIAGNOSES_COLUMNS) - set(diagnoses.columns)
        if len(missing_cols) > 0:
            raise ValueError(
                'diagnoses DataFrame missing the following required columns {}'
                .format(list(missing_cols)))


    def evaluate_risk(self, demographics, diagnoses, do_sedits=True, date_asof=None):
        """Evaluate the risk model for every person in the `demographics` DataFrame

        The demographics DataFrame must have the following columns (one row per person),

          pt_id    - arbitrary unique identifier (e.g. HICN).
          sex      - 1=male, 2=female
          dob      - date of birth (year-month-day string or datetime object)
          ltimcaid - 1 if number of months in Medicaid in payment year > 0,
                     otherwise 0
          nemcaid  - 1 if a new Medicare enrollee and number of months in Medicaid
                     in payment year > 0, otherwise 0
          orec     - original reason for entitlement with the following values:
                       0 - old  age (OASI)
                       1 - disability (DIB)
                       2 – end stage renal disease (ESRD)
                       3 - both DIB AND ESRD


        The diagnoses DataFrame must have the following columns (one row per patient
        diagnosis)

          pt_id     - arbitrary unique identifier (e.g. HICN).
          diag_code - ICD-10 diagnosis code with no periods
          diag_type - 0 for ICD-10 codes

        """
        self.validate_demographics(demographics)
        self.validate_diagnoses(diagnoses)

        # set date_asof to Feb. 1 of current year if none is provided
        #--------------------------------------------------------------------
        if date_asof is None:
            date_asof = datetime.date(datetime.date.today().year, 2, 1)

        # convert dates of birth to datetime objects and reset indexes to pt_id
        #--------------------------------------------------------------------
        demographics['dob'] = demographics['dob'].apply(pandas.to_datetime)
        demographics = demographics.set_index('pt_id')
        diagnoses = diagnoses.set_index('pt_id')

        # loop over people
        #--------------------------------------------------------------------
        patients = []
        for row in demographics.itertuples():

            # put input demographic data into local variables
            #--------------------------------------------------------------------
            pt_id = row.Index
            dob = row.dob
            sex = int(row.sex)
            ltimcaid = int(row.ltimcaid)
            nemcaid = int(row.nemcaid)
            orec = int(row.orec)
            agef = relativedelta.relativedelta(date_asof, dob).years

            # create demographic predictor variables
            #--------------------------------------------------------------------
            demographic_preds, disabl = self.create_demographic_predictors(
                agef, sex, orec, ltimcaid, nemcaid)

            # create diagnosis predictor variables
            #--------------------------------------------------------------------
            if pt_id in diagnoses.index:
                diagnoses_for_pt = diagnoses.loc[pt_id]
                diags_to_hccs, diagnosis_preds = self.create_diagnosis_predictors(
                    diagnoses_for_pt, agef, sex, disabl, do_sedits)
            else:
                diags_to_hccs = []
                diagnosis_preds = {}

            # calculate segment risk scores for patient
            #--------------------------------------------------------------------
            risk_scores = {}
            flagged_demo_coeffs = {}
            flagged_diag_coeffs = {}

            # loop over risk segments
            for seg_name in self.SEGMENT_NAMES:
                risk_scores[seg_name] = 0
                flagged_demo_coeffs[seg_name] = {}
                flagged_diag_coeffs[seg_name] = {}

                # loop over predictor variables for segment
                for var in self.SEGMENT_PREDICTORS[seg_name]:
                    coef_var = '{}_{}'.format(seg_name, var)
                    coeff = self.COEFFICIENTS[coef_var]

                    if demographic_preds.get(var) == 1:
                        flagged_demo_coeffs[seg_name][var] = coeff
                        risk_scores[seg_name] += coeff

                    if diagnosis_preds.get(var) == 1:
                        flagged_diag_coeffs[seg_name][var] = coeff
                        risk_scores[seg_name] += coeff

            # construct a patient object and append to output patients
            #--------------------------------------------------------------------
            patient = {'pt_id': pt_id}
            patient['demographic_data'] = {
                'dob': dob.date().isoformat(),
                'sex': sex,
                'ltimcaid': ltimcaid,
                'nemcaid': nemcaid,
                'orec': orec,
                'age': agef}
            patient['diagnoses_to_hccs'] = diags_to_hccs

            # we want all the data for a given model segment to be grouped
            risk_profiles = {}
            for seg_name in self.SEGMENT_NAMES:
                risk_profile = {}
                risk_profile['score'] = risk_scores[seg_name]
                risk_profile['demographic_coefficients'] = flagged_demo_coeffs[seg_name]
                risk_profile['diagnosis_coefficients'] = flagged_diag_coeffs[seg_name]
                risk_profile['segment_name'] = seg_name
                risk_profile['segment_description'] = self.SEGMENT_DESCRIPTIONS[seg_name]
                risk_profiles[seg_name] = risk_profile
            patient['risk_profiles'] = risk_profiles

            patients.append(patient)

        # add model meta data to response
        #--------------------------------------------------------------------
        model_info = {
            'model_name': self.NAME,
            'model_description': self.DESCRIPTION,
            'model_segments': self.SEGMENT_DESCRIPTIONS,
        }

        # build final result
        #--------------------------------------------------------------------
        result = {
            'model_info': model_info,
            'patients': patients,
        }

        # lets do the encoding here
        result_str = json.dumps(result, cls=ResultEncoder)
        result_json = json.loads(result_str)

        return result_json


    def map_icd_to_ccs(self, agef, sex, diag_code, diag_type, do_sedits):
        """Map a single ICD diagnosis code to all of its condition categories"""
        diag_to_ccs = []

        # initial dummy value
        cc = 9999

        # check MCE edits
        cc = v22i0ed1.icd10_edits(cc, agef, sex, diag_code, do_sedits, self.FORMATS)

        # if the edits return a valid condition category, then append
        if cc != -1 and cc != 9999:
            diag_to_ccs.append(
                {'diag_code': diag_code, 'diag_type': diag_type,
                 'cc': cc, 'assign_type': 'mce'})

        # otherwise assign condition categories and extend
        elif cc == 9999:
            diag_to_ccs.extend(self.FORMATS.diag_to_ccs(diag_code, diag_type))

        return diag_to_ccs



    def create_diagnosis_predictors(self, diagnoses, agef, sex, disabl, do_sedits):
        """Calculate predictors based on diagnosis codes for one person"""

        preds = {}
        diags_to_hccs = []

        # loop over diagnoses and assign Condition Categories (CCs)
        #--------------------------------------------------------------------
        for irow, row in enumerate(diagnoses.itertuples()):

            diag_code = row.diag_code
            diag_type = row.diag_type
            diag_to_ccs = self.map_icd_to_ccs(agef, sex, diag_code, diag_type, do_sedits)
            diags_to_hccs.extend(diag_to_ccs)

        # impose the hierarchy
        #--------------------------------------------------------------------
        diags_to_hccs = v22h79h1.impose_hierarchy_2(diags_to_hccs)

        # add CC and diagnosis descriptions
        #--------------------------------------------------------------------
        for el in diags_to_hccs:
            el['cc_description'] = self.HCC_DESCRIPTIONS['HCC{}'.format(el['cc'])]
            el['diag_description'] = self.ICD10_DEFS.return_long_description(el['diag_code'])


        # add HCC variables to predictors
        #--------------------------------------------------------------------
        for hcc_str in self.HCC_DESCRIPTIONS:
            hcc_int = int(hcc_str[3:])
            # check if this HCC is flagged
            flagged = False
            for el in diags_to_hccs:
                if el['hcc'] == hcc_int:
                    flagged = True
            if flagged:
                preds[hcc_str] = 1
            else:
                preds[hcc_str] = 0

        # calculate interactions
        #--------------------------------------------------------------------

        # %*diagnostic categories;
        cancer          = max(preds['HCC8'], preds['HCC9'], preds['HCC10'],
                              preds['HCC11'], preds['HCC12'])
        diabetes        = max(preds['HCC17'], preds['HCC18'], preds['HCC19'])
        card_resp_fail  = max(preds['HCC82'], preds['HCC83'], preds['HCC84'])
        chf             = preds['HCC85']
        gCopdCF         = max(preds['HCC110'], preds['HCC111'], preds['HCC112'])
        renal           = max(preds['HCC134'], preds['HCC135'], preds['HCC136'],
                              preds['HCC137'])
        sepsis          = preds['HCC2']
        gSubstanceAbuse = max(preds['HCC54'], preds['HCC55'])
        gPsychiatric    = max(preds['HCC57'], preds['HCC58'])


        # %*community models interactions ;
        preds['HCC47_gCancer']                = preds['HCC47'] * cancer
        preds['HCC85_gDiabetesMellit']        = preds['HCC85'] * diabetes
        preds['HCC85_gCopdCF']                = preds['HCC85'] * gCopdCF
        preds['HCC85_gRenal']                 = preds['HCC85'] * renal
        preds['gRespDepandArre_gCopdCF']      = card_resp_fail * gCopdCF
        preds['HCC85_HCC96']                  = preds['HCC85'] * preds['HCC96']
        preds['gSubstanceAbuse_gPsychiatric'] = gSubstanceAbuse * gPsychiatric


        # %*institutional model;
        pressure_ulcer = max(preds['HCC157'], preds['HCC158'])  # /*10/19/2012*/

        preds['CHF_gCopdCF']                  = chf * gCopdCF
        preds['gCopdCF_CARD_RESP_FAIL']       = gCopdCF * card_resp_fail

        preds['SEPSIS_PRESSURE_ULCER']        = sepsis * pressure_ulcer
        preds['SEPSIS_ARTIF_OPENINGS']        = sepsis * preds['HCC188']
        preds['ART_OPENINGS_PRESSURE_ULCER']  = preds['HCC188'] * pressure_ulcer

        preds['DIABETES_CHF']                 = diabetes * chf
        preds['gCopdCF_ASP_SPEC_BACT_PNEUM']  = gCopdCF * preds['HCC114']
        preds['ASP_SPEC_BACT_PNEUM_PRES_ULC'] = preds['HCC114'] * pressure_ulcer
        preds['SEPSIS_ASP_SPEC_BACT_PNEUM']   = sepsis * preds['HCC114']
        preds['SCHIZOPHRENIA_gCopdCF']        = preds['HCC57'] * gCopdCF
        preds['SCHIZOPHRENIA_CHF']            = preds['HCC57'] * chf
        preds['SCHIZOPHRENIA_SEIZURES']       = preds['HCC57'] * preds['HCC79']

        preds['DISABLED_HCC85']          = disabl * preds['HCC85']
        preds['DISABLED_PRESSURE_ULCER'] = disabl * pressure_ulcer
        preds['DISABLED_HCC161']         = disabl * preds['HCC161']
        preds['DISABLED_HCC39']          = disabl * preds['HCC39']
        preds['DISABLED_HCC77']          = disabl * preds['HCC77']
        preds['DISABLED_HCC6']           = disabl * preds['HCC6']

        return diags_to_hccs, preds



    def create_demographic_predictors(self, agef, sex, orec, ltimcaid, nemcaid):
        """Calculate the demographic predictor variables."""
        preds = {}
        preds['LTIMCAID'] = ltimcaid

        disabl = agesexv2.create_disabl(agef, orec)
        origds = agesexv2.create_origds(disabl, orec)
        preds['ORIGDS'] = origds

        cell = agesexv2.create_cell(agef, sex)
        necell = agesexv2.create_necell(agef, sex)
        for k, v in cell.items():
            preds[k] = v
        for k, v in necell.items():
            preds[k] = v

        # interactions
        preds['OriginallyDisabled_Female'] = int(origds==1 and sex==2)
        preds['OriginallyDisabled_Male'] = int(origds==1 and sex==1)

        # new enrollee interactions
        ne_origds       = int(agef>=65 and orec==1)
        nmcaid_norigdis = int(nemcaid==0 and ne_origds==0)
        mcaid_norigdis  = int(nemcaid==1 and ne_origds==0)
        nmcaid_origdis  = int(nemcaid==0 and ne_origds==1)
        mcaid_origdis   = int(nemcaid==1 and ne_origds==1)

        for key in rv.NE_AGESEXV:
            preds['NMCAID_NORIGDIS_{}'.format(key)] = nmcaid_norigdis * preds[key]
        for key in rv.NE_AGESEXV:
            preds['MCAID_NORIGDIS_{}'.format(key)] = mcaid_norigdis * preds[key]
        for key in rv.ONE_AGESEXV:
            preds['NMCAID_ORIGDIS_{}'.format(key)] = nmcaid_origdis * preds[key]
        for key in rv.ONE_AGESEXV:
            preds['MCAID_ORIGDIS_{}'.format(key)] = mcaid_origdis * preds[key]

        return preds, disabl


    def return_icd_hcc_mappings(self):
        """Return JSON friendly mapping of diagnoses codes -> HCCs for this model"""
        all_mappings = self.FORMATS.return_diag_hcc_mappings()
        return all_mappings


    def return_model_description(self):
        """Return JSON friendly model description"""
        desc = {
            'model_name': self.NAME,
            'model_description': self.DESCRIPTION,
            'model_segments': self.SEGMENT_DESCRIPTIONS,
            'model_coefficients': self.COEFFICIENTS.to_dict(),
            'hcc_descriptions': self.HCC_DESCRIPTIONS,
            'icd_to_hcc_mappings': self.return_icd_hcc_mappings(),
        }
        return desc


if __name__ == '__main__':

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

    model = V2217_79_O1()
    result = model.evaluate_risk(demographics, diagnoses)
