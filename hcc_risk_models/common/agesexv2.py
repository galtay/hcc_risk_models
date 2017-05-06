"""
Module to handle demographic dummy variables.

Inputs:

    The functions in this module use the following patient input,

        age (integer)  - patient age in years
        sex (integer)  - male=1, female=2
        orec (integer) - original reason for entitlement

    Note the Original Reason for Entitlement Codes (OREC) are,
    (https://www.resdac.org/cms-data/variables/Original-Reason-Entitlement-Code)

        0:  Old Age and Survivors Insurance (OASI)
        1:  Disability Insurance Benefits (DIB)
        2:  End Stage Renal Disease (ESRD)
        3:  Both DIB and ESRD


Outputs:

    A set of binary demographic dummy variables (0 or 1).

      create_disabl - patient disabled?
      create_origds - patient originally disabled?
      create_cell   - 24 dummy agesex variables for non "new_enrollee"
                      models (AGESEXV)
      create_necell - 32 dummy agesex variables for "new enrollee"
                      models (NE_AGESEXV)

"""
import re

AGESEXV = [
    'F0_34',  'F35_44', 'F45_54', 'F55_59', 'F60_64', 'F65_69',
    'F70_74', 'F75_79', 'F80_84', 'F85_89', 'F90_94', 'F95_GT',
    'M0_34',  'M35_44', 'M45_54', 'M55_59', 'M60_64', 'M65_69',
    'M70_74', 'M75_79', 'M80_84', 'M85_89', 'M90_94', 'M95_GT',
]

NE_AGESEXV = [
    'NEF0_34',  'NEF35_44', 'NEF45_54',  'NEF55_59',  'NEF60_64',
    'NEF65',    'NEF66',    'NEF67',     'NEF68',     'NEF69',
    'NEF70_74', 'NEF75_79', 'NEF80_84',  'NEF85_89',  'NEF90_94',
    'NEF95_GT',
    'NEM0_34',  'NEM35_44', 'NEM45_54', 'NEM55_59', 'NEM60_64',
    'NEM65',    'NEM66',    'NEM67',    'NEM68',    'NEM69',
    'NEM70_74', 'NEM75_79', 'NEM80_84', 'NEM85_89', 'NEM90_94',
    'NEM95_GT',
]

MAX_AGE = 1000

#: regular expression for agesex dummy variable names
PATTERN = re.compile(
    """
    (NE)?                    # optional 'NE' prefix
    (?P<sex>M|F)             # sex
    (?P<age_lo>\d{1,2})      # lower age limit
    (_                       # optional underscore
    (?P<age_hi>\d{1,2}|GT)   # optional upper age limit
    )?
    """, re.VERBOSE)


def _parse_agesex_var(x):
    """Parse an agesex string into sex and age limit integers.

    Args:
      x (string): e.g. "F0_34", "NEF65", "NEF95_GT", ...

    Returns:
      sex (int): male=1, female=2
      age_lo (int): minimum age for dummy variable
      age_hi (int): maximum age for dummy variable
    """
    m = re.match(PATTERN, x)
    sex = 1 if m.group('sex') == 'M' else 2
    age_lo = m.group('age_lo')
    age_hi = m.group('age_hi')
    if age_hi == 'GT':
        age_hi = MAX_AGE
    if age_hi is None:
        age_hi = age_lo
    return sex, int(age_lo), int(age_hi)


def create_cell(age, sex):
    """Create demographic variables for non "new enrollee" models (i.e. the
    dummy variables in AGESEXV)

    Args:
      age (int): patient age in years
      sex (int): male=1, female=2

    Returns:
      cell (dict): keys are elements of AGESEXV.  all values = 0 except
                   the agesex dummy variable that matches the patient input
    """
    cell = {varname: 0 for varname in AGESEXV}
    for varname in AGESEXV:
        dummy_sex, dummy_age_lo, dummy_age_hi = _parse_agesex_var(varname)
        if sex == dummy_sex and dummy_age_lo <= age <= dummy_age_hi:
            cell[varname] = 1
    return cell


def create_necell(age, sex):
    """Create demographic variables for "new enrollee" models (i.e. the
    dummy variables in NE_AGESEXV)

    Args:
      age (int): patient age in years
      sex (int): male=1, female=2

    Returns:
      necell (dict): keys are elements of NE_AGESEXV.  all values = 0 except
                     the agesex dummy variable that matches the patient input
    """
    necell = {varname: 0 for varname in NE_AGESEXV}
    for varname in NE_AGESEXV:
        dummy_sex, dummy_age_lo, dummy_age_hi = _parse_agesex_var(varname)
        if sex == dummy_sex and dummy_age_lo <= age <= dummy_age_hi:
            necell[varname] = 1
    return necell


def create_disabl(age, orec):
    """Return value of "disabl" (disabled) dummy variable

    Args:
      age (int): patient age in years
      orec (int): original reason for entitlement code

    Returns:
      disabl (int): disabled dummy variable
    """
    disabl = int(age < 65 and orec != 0)
    return disabl


def create_origds(disabl, orec):
    """Determine value of "origds" (originally disabled) dummy variable

    Args:
      disabl (int): disabled dummy variable (from create_disabl)
      orec (int): original reason for entitlement code

    Returns:
      origds (int): originally disabled dummy variable

    """
    disabl = int(disabl)
    orec = int(orec)
    origds = int(orec == 1 and disabl == 0)
    return origds


if __name__ == '__main__':

    age = 63
    orec = 1
    disabl = create_disabl(age, orec)

    disabl = 1
    orec = 3
    origds = create_origds(disabl, orec)

    age = 56
    sex = 1
    cell = create_cell(age, sex)

    age = 84
    sex = 2
    necell = create_necell(age, sex)
