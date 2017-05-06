"""
 %MACRO V22I9ED1(AGE=, SEX=, ICD9= );
 %**********************************************************************
 ***********************************************************************
 1  MACRO NAME:  V22I9ED1
 2  PURPOSE:     age/sex edits on ICD9: some edits are mandatory,
                 others - are based on MCE list to check
                 if age or sex for a beneficiary is within the
                 range of acceptable age/sex, if not- CC is set to
                 -1.0 - invalid
 3  PARAMETERS:  AGE   - beneficiary age variable calculated by DOB
                         from a person level file
                 SEX   - beneficiary SEX variable in a person level file
                 ICD9  - diagnosis variable in a diagnosis file

 4  COMMENTS:    1. Age format AGEFMT9 and sex format SEXFMT9 are
                    parameters in the main macro. They have to
                    correspond to the years of data

                 2. If ICD9 code does not have any restriction on age
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

CHECK1 = set(['2860', '2861'])
CHECK2 = set(['4910', '4911', '49120', '49121', '49122', '4918',
              '4919', '4920',  '4928',  '496',  '5181', '5182'])
CHECK3 = set(['49320', '49321', '49322'])
DIAG_TYPE = 9

def icd9_edits(cc, age, sex, diag, sedits, hcc_formats):

    # /* Hemophilia for women */
    if sex == 2 and diag in CHECK1:
        cc = 48

    # /* emphysema/chronic bronchitis */
    elif age < 18 and diag in CHECK2:
        cc = 112

    # /* chronic obstructive asthma */
    elif age < 18 and diag in CHECK3:
        cc = -1

    if sedits:
        valid_age = hcc_formats.sedit_check_age(diag, age, DIAG_TYPE)
        valid_sex = hcc_formats.sedit_check_sex(diag, sex, DIAG_TYPE)
        valid = valid_age and valid_sex
        if not valid:
            cc = -1

    return cc
