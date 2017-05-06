import hcc_risk_models as hrm


# Validate model codes for V2216_79_O2 (CMS-HCC Final 2017)
#======================================================================

# get the codes used in the risk model
model = hrm.v2217_79_O1.risk_model.V2217_79_O1()
model_code_objs = model.FORMATS.return_diag_hcc_mappings()

# get ICD-10-CM subset
model_codes_0 = set([
    el['diag_code'] for el in model_code_objs if el['diag_type']==0])


# check ICD-10
icd10cm_2017 = hrm.icd_descriptions.icd10cm_descriptions_2017.Icd10CmDefinitions()
code_descriptions = set(icd10cm_2017.df.index.values)
set_diff = model_codes_0 - code_descriptions
assert(len(set_diff)==0)



# Validate model codes for V2216_79_O2 (CMS-HCC Initial 2017)
#======================================================================

# get the codes used in the risk model
model = hrm.v2216_79_O2.risk_model.V2216_79_O2()
model_code_objs = model.FORMATS.return_diag_hcc_mappings()

# get ICD-10-CM subset
model_codes_0 = set([
    el['diag_code'] for el in model_code_objs if el['diag_type']==0])

# get ICD-9-CM subset
model_codes_9 = set([
    el['diag_code'] for el in model_code_objs if el['diag_type']==9])

# check ICD-10
icd10cm_2016 = hrm.icd_descriptions.icd10cm_descriptions_2016.Icd10CmDefinitions()
code_descriptions = set(icd10cm_2016.df.index.values)
set_diff = model_codes_0 - code_descriptions
assert(len(set_diff)==0)

# check ICD-9
icd9cm_v32 = hrm.icd_descriptions.icd9cm_descriptions_v32.Icd9CmDefinitions()
code_descriptions = set(icd9cm_v32.df.index.values)
set_diff = model_codes_9 - code_descriptions
assert(len(set_diff)==0)
