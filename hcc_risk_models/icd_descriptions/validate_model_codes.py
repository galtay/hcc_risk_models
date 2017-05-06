import cms_hcc_risk_models
from cms_hcc_risk_models.icd_descriptions import icd10cm_descriptions_2016
from cms_hcc_risk_models.icd_descriptions import icd9cm_descriptions_v32


# Validate model codes for V2216_79_O2
#======================================================================

# get the codes used in the risk model
model = cms_hcc_risk_models.v2216_79_O2.risk_model.V2216_79_O2()
model_code_objs = model.FORMATS.return_diag_hcc_mappings()

# get ICD-10-CM subset
model_codes_0 = set([
    el['diag_code'] for el in model_code_objs if el['diag_type']==0])

# get ICD-9-CM subset
model_codes_9 = set([
    el['diag_code'] for el in model_code_objs if el['diag_type']==9])

# check ICD-10
icd10cm_2016 = icd10cm_descriptions_2016.Icd10CmDefinitions()
code_descriptions = set(icd10cm_2016.df.index.values)
set_diff = model_codes_0 - code_descriptions
assert(len(set_diff)==0)

# check ICD-9
icd9cm_v32 = icd9cm_descriptions_v32.Icd9CmDefinitions()
code_descriptions = set(icd9cm_v32.df.index.values)
set_diff = model_codes_9 - code_descriptions
assert(len(set_diff)==0)
