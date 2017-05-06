INPUTVARS = ['SEX', 'DOB', 'LTIMCAID', 'NEMCAID', 'OREC']

DEMVARS = [
    'AGEF', 'ORIGDS', 'DISABL',
    'F0_34',  'F35_44', 'F45_54', 'F55_59', 'F60_64', 'F65_69',
    'F70_74', 'F75_79', 'F80_84', 'F85_89', 'F90_94', 'F95_GT',
    'M0_34',  'M35_44', 'M45_54', 'M55_59', 'M60_64', 'M65_69',
    'M70_74', 'M75_79', 'M80_84', 'M85_89', 'M90_94', 'M95_GT',
    'NEF0_34',  'NEF35_44', 'NEF45_54', 'NEF55_59', 'NEF60_64',
    'NEF65',    'NEF66',    'NEF67',    'NEF68',    'NEF69',
    'NEF70_74', 'NEF75_79', 'NEF80_84', 'NEF85_89', 'NEF90_94',
    'NEF95_GT',
    'NEM0_34',  'NEM35_44', 'NEM45_54', 'NEM55_59', 'NEM60_64',
    'NEM65',    'NEM66',    'NEM67',    'NEM68',    'NEM69',
    'NEM70_74', 'NEM75_79', 'NEM80_84', 'NEM85_89', 'NEM90_94',
    'NEM95_GT',
]


SCOREVARS = [
    'SCORE_COMMUNITY_NA', 'SCORE_COMMUNITY_ND',
    'SCORE_COMMUNITY_FBA', 'SCORE_COMMUNITY_FBD',
    'SCORE_COMMUNITY_PBA', 'SCORE_COMMUNITY_PBD',
    'SCORE_INSTITUTIONAL', 'SCORE_NEW_ENROLLEE',
    'SCORE_SNP_NEW_ENROLLEE',
]


N_CC=201  # max # of HCCs

CC_NUMS = [
    1,   2,   6,   8,   9,   10,  11,  12,
    17,  18,  19,  21,  22,  23,  27,  28,
    29,  33,  34,  35,  39,  40,  46,  47,
    48,            54,  55,  57,  58,  70,
    71,  72,  73,  74,  75,  76,  77,  78,
    79,  80,  82,  83,  84,  85,  86,  87,
    88,  96,  99,  100, 103, 104, 106, 107,
    108, 110, 111, 112, 114, 115, 122, 124,
    134, 135, 136, 137,
    157, 158,           161, 162, 166, 167,
    169, 170, 173, 176, 186, 188, 189,
]

HCCV22_list79 = ['HCC{}'.format(num) for num in CC_NUMS]
CCV22_list79 = ['CC{}'.format(num) for num in CC_NUMS]


# %* age/sex variables for Insititutional regression;
AGESEXV = [
    'F0_34','F35_44','F45_54','F55_59','F60_64','F65_69',
    'F70_74','F75_79','F80_84','F85_89','F90_94','F95_GT',
    'M0_34','M35_44','M45_54','M55_59','M60_64','M65_69',
    'M70_74','M75_79','M80_84','M85_89','M90_94','M95_GT',
]


# %*age/sex variables for non-ORIGDS New Enrollee and SNP New Enrollee interactions;
NE_AGESEXV = [
    'NEF0_34',   'NEF35_44',  'NEF45_54',  'NEF55_59',  'NEF60_64',
    'NEF65',     'NEF66',     'NEF67',     'NEF68',     'NEF69',
    'NEF70_74',  'NEF75_79',  'NEF80_84',
    'NEF85_89',  'NEF90_94',  'NEF95_GT',
    'NEM0_34',   'NEM35_44',  'NEM45_54',  'NEM55_59',  'NEM60_64',
    'NEM65',     'NEM66',     'NEM67',     'NEM68',     'NEM69',
    'NEM70_74',  'NEM75_79',  'NEM80_84',
    'NEM85_89',  'NEM90_94',  'NEM95_GT',
]


# %* age/sex variables for Community Aged regression;
AGESEXVA = [
    'F65_69','F70_74','F75_79','F80_84','F85_89','F90_94','F95_GT',
    'M65_69','M70_74','M75_79','M80_84','M85_89','M90_94','M95_GT',
]

# %* age/sex variables for Community Disabled regression;
AGESEXVD = [
    'F0_34','F35_44','F45_54','F55_59','F60_64',
    'M0_34','M35_44','M45_54','M55_59','M60_64',
]

# %* diagnostic categories necessary to create interaction variables;
DIAG_CAT = [
    'CANCER','DIABETES','CHF','CARD_RESP_FAIL','gCopdCF','RENAL',
    'SEPSIS','PRESSURE_ULCER','gSubstanceAbuse','gPsychiatric'
]

# %*orig disabled interactions for Community Aged regressions;
ORIG_INT = ['OriginallyDisabled_Female', 'OriginallyDisabled_Male']

# %*interaction variables for Community Aged regressions;
INTERRACC_VARSA = [
    'HCC47_gCancer', 'HCC85_gDiabetesMellit', 'HCC85_gCopdCF', 'HCC85_gRenal',
    'gRespDepandArre_gCopdCF', 'HCC85_HCC96',
]

# %*interaction variables for Community Disabled regressions;
INTERRACC_VARSD = [
    'HCC47_gCancer', 'HCC85_gDiabetesMellit', 'HCC85_gCopdCF', 'HCC85_gRenal',
    'gRespDepandArre_gCopdCF', 'HCC85_HCC96', 'gSubstanceAbuse_gPsychiatric',
]

# %*variables for Community Aged regressions ;
COMM_REGA = AGESEXVA + ORIG_INT + HCCV22_list79 + INTERRACC_VARSA

# %*variables for Community Disabled regressions ;
COMM_REGD = AGESEXVD + HCCV22_list79 + INTERRACC_VARSD


# %*interaction variables for Institutional regression;
INTERRACI_VARS = [
    'DISABLED_HCC85',       'DISABLED_PRESSURE_ULCER',
    'DISABLED_HCC161',      'DISABLED_HCC39',
    'DISABLED_HCC77',       'DISABLED_HCC6',
    'CHF_gCopdCF',
    'gCopdCF_CARD_RESP_FAIL',
    'SEPSIS_PRESSURE_ULCER',
    'SEPSIS_ARTIF_OPENINGS',
    'ART_OPENINGS_PRESSURE_ULCER',
    'DIABETES_CHF',
    'gCopdCF_ASP_SPEC_BACT_PNEUM',
    'ASP_SPEC_BACT_PNEUM_PRES_ULC',
    'SEPSIS_ASP_SPEC_BACT_PNEUM',
    'SCHIZOPHRENIA_gCopdCF',
    'SCHIZOPHRENIA_CHF',
    'SCHIZOPHRENIA_SEIZURES',
]


# %*variables for Institutional regression;
INST_REG = AGESEXV + ['LTIMCAID', 'ORIGDS'] + INTERRACI_VARS + HCCV22_list79


# %*age/sex variables for ORIGDS New Enrollee and SNP New Enrollee interactions;
ONE_AGESEXV = [
    'NEF65',     'NEF66',     'NEF67',     'NEF68',     'NEF69',
    'NEF70_74',  'NEF75_79',  'NEF80_84',
    'NEF85_89',  'NEF90_94',  'NEF95_GT',
    'NEM65',     'NEM66',     'NEM67',     'NEM68',     'NEM69',
    'NEM70_74',  'NEM75_79',  'NEM80_84',
    'NEM85_89',  'NEM90_94',  'NEM95_GT',
]


# %*variables for New Enrollee and SNP New Enrollee regression;
NE_REG = [
    'NMCAID_NORIGDIS_NEF0_34',       'NMCAID_NORIGDIS_NEF35_44',
    'NMCAID_NORIGDIS_NEF45_54',      'NMCAID_NORIGDIS_NEF55_59',
    'NMCAID_NORIGDIS_NEF60_64',      'NMCAID_NORIGDIS_NEF65',
    'NMCAID_NORIGDIS_NEF66',         'NMCAID_NORIGDIS_NEF67',
    'NMCAID_NORIGDIS_NEF68',         'NMCAID_NORIGDIS_NEF69',
    'NMCAID_NORIGDIS_NEF70_74',      'NMCAID_NORIGDIS_NEF75_79',
    'NMCAID_NORIGDIS_NEF80_84',      'NMCAID_NORIGDIS_NEF85_89',
    'NMCAID_NORIGDIS_NEF90_94',      'NMCAID_NORIGDIS_NEF95_GT',

    'NMCAID_NORIGDIS_NEM0_34',       'NMCAID_NORIGDIS_NEM35_44',
    'NMCAID_NORIGDIS_NEM45_54',      'NMCAID_NORIGDIS_NEM55_59',
    'NMCAID_NORIGDIS_NEM60_64',      'NMCAID_NORIGDIS_NEM65',
    'NMCAID_NORIGDIS_NEM66',         'NMCAID_NORIGDIS_NEM67',
    'NMCAID_NORIGDIS_NEM68',         'NMCAID_NORIGDIS_NEM69',
    'NMCAID_NORIGDIS_NEM70_74',      'NMCAID_NORIGDIS_NEM75_79',
    'NMCAID_NORIGDIS_NEM80_84',      'NMCAID_NORIGDIS_NEM85_89',
    'NMCAID_NORIGDIS_NEM90_94',      'NMCAID_NORIGDIS_NEM95_GT',

    'MCAID_NORIGDIS_NEF0_34',        'MCAID_NORIGDIS_NEF35_44',
    'MCAID_NORIGDIS_NEF45_54',       'MCAID_NORIGDIS_NEF55_59',
    'MCAID_NORIGDIS_NEF60_64',       'MCAID_NORIGDIS_NEF65',
    'MCAID_NORIGDIS_NEF66',          'MCAID_NORIGDIS_NEF67',
    'MCAID_NORIGDIS_NEF68',          'MCAID_NORIGDIS_NEF69',
    'MCAID_NORIGDIS_NEF70_74',       'MCAID_NORIGDIS_NEF75_79',
    'MCAID_NORIGDIS_NEF80_84',       'MCAID_NORIGDIS_NEF85_89',
    'MCAID_NORIGDIS_NEF90_94',       'MCAID_NORIGDIS_NEF95_GT',

    'MCAID_NORIGDIS_NEM0_34',        'MCAID_NORIGDIS_NEM35_44',
    'MCAID_NORIGDIS_NEM45_54',       'MCAID_NORIGDIS_NEM55_59',
    'MCAID_NORIGDIS_NEM60_64',       'MCAID_NORIGDIS_NEM65',
    'MCAID_NORIGDIS_NEM66',          'MCAID_NORIGDIS_NEM67',
    'MCAID_NORIGDIS_NEM68',          'MCAID_NORIGDIS_NEM69',
    'MCAID_NORIGDIS_NEM70_74',       'MCAID_NORIGDIS_NEM75_79',
    'MCAID_NORIGDIS_NEM80_84',       'MCAID_NORIGDIS_NEM85_89',
    'MCAID_NORIGDIS_NEM90_94',       'MCAID_NORIGDIS_NEM95_GT',

    'NMCAID_ORIGDIS_NEF65',          'NMCAID_ORIGDIS_NEF66',
    'NMCAID_ORIGDIS_NEF67',          'NMCAID_ORIGDIS_NEF68',
    'NMCAID_ORIGDIS_NEF69',          'NMCAID_ORIGDIS_NEF70_74',
    'NMCAID_ORIGDIS_NEF75_79',       'NMCAID_ORIGDIS_NEF80_84',
    'NMCAID_ORIGDIS_NEF85_89',       'NMCAID_ORIGDIS_NEF90_94',
    'NMCAID_ORIGDIS_NEF95_GT',

    'NMCAID_ORIGDIS_NEM65',          'NMCAID_ORIGDIS_NEM66',
    'NMCAID_ORIGDIS_NEM67',          'NMCAID_ORIGDIS_NEM68',
    'NMCAID_ORIGDIS_NEM69',          'NMCAID_ORIGDIS_NEM70_74',
    'NMCAID_ORIGDIS_NEM75_79',       'NMCAID_ORIGDIS_NEM80_84',
    'NMCAID_ORIGDIS_NEM85_89',       'NMCAID_ORIGDIS_NEM90_94',
    'NMCAID_ORIGDIS_NEM95_GT',

    'MCAID_ORIGDIS_NEF65',           'MCAID_ORIGDIS_NEF66',
    'MCAID_ORIGDIS_NEF67',           'MCAID_ORIGDIS_NEF68',
    'MCAID_ORIGDIS_NEF69',           'MCAID_ORIGDIS_NEF70_74',
    'MCAID_ORIGDIS_NEF75_79',        'MCAID_ORIGDIS_NEF80_84',
    'MCAID_ORIGDIS_NEF85_89',        'MCAID_ORIGDIS_NEF90_94',
    'MCAID_ORIGDIS_NEF95_GT',

    'MCAID_ORIGDIS_NEM65',           'MCAID_ORIGDIS_NEM66',
    'MCAID_ORIGDIS_NEM67',           'MCAID_ORIGDIS_NEM68',
    'MCAID_ORIGDIS_NEM69',           'MCAID_ORIGDIS_NEM70_74',
    'MCAID_ORIGDIS_NEM75_79',        'MCAID_ORIGDIS_NEM80_84',
    'MCAID_ORIGDIS_NEM85_89',        'MCAID_ORIGDIS_NEM90_94',
    'MCAID_ORIGDIS_NEM95_GT',
]
