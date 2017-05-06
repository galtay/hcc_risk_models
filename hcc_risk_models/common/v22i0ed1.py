"""
 %MACRO V22I0ED1(AGE=, SEX=, ICD10= );
 %**********************************************************************
 ***********************************************************************
 1  MACRO NAME:  V22I0ED1
 2  PURPOSE:     age/sex edits on ICD10: some edits are mandatory,
                 others - are based on MCE list to check
                 if age or sex for a beneficiary is within the
                 range of acceptable age/sex, if not- CC is set to
                 -1.0 - invalid
 3  PARAMETERS:  AGE   - beneficiary age variable calculated by DOB
                         from a person level file
                 SEX   - beneficiary SEX variable in a person level file
                 ICD10  - diagnosis variable in a diagnosis file

 4  COMMENTS:    1. Age format AGEFMT0 and sex format SEXFMT0 are
                    parameters in the main macro. They have to
                    correspond to the years of data

                 2. If ICD10 code does not have any restriction on age
                    or sex then the corresponding format puts it in "-1"

                 3. AGEL format sets lower limits for age
                    AGEU format sets upper limit for age
                    for specific edit categories:
                    "0"= "0 newborn (age 0)      "
                    "1"= "1 pediatric (age 0 -17)"
                    "2"= "2 maternity (age 12-55)"
                    "3"= "3 adult (age 14+)      "

                 4. SEDITS - parameter for the main macro
 **********************************************************************;
"""

CHECK1 = set(['D66', 'D67'])
CHECK2 = set(['J410', 'J411', 'J418', 'J42',  'J430', 'J431', 'J432',
              'J438', 'J439', 'J440', 'J441', 'J449', 'J982', 'J983'])

CHECK3 = set(['49320', '49321', '49322'])
DIAG_TYPE = 0

def icd10_edits(cc, age, sex, diag, sedits, hcc_formats):

    if sex == 2 and diag in CHECK1:
        cc = 48

    elif age < 18 and diag in CHECK2:
        cc = 112

    if sedits:
        valid_age = hcc_formats.sedit_check_age(diag, age, DIAG_TYPE)
        valid_sex = hcc_formats.sedit_check_sex(diag, sex, DIAG_TYPE)
        valid = valid_age and valid_sex
        if not valid:
            cc = -1

    return cc
