"""
 %MACRO V22H79H1; /* HIERARCHIES */;
 %**********************************************************************
 ***********************************************************************

 1  MACRO NAME:      V22H79H1
 2  PURPOSE:         HCC HIERARCHIES: version 22 of HCCs
                     only 79 CMS HCCs are included

 **********************************************************************;
"""


# map priority of HCC codes
HCC_HIER_DICT = {
    8: [9 ,10 ,11 ,12],            # /*Neoplasm 1 */
    9: [10 ,11 ,12],               # /*Neoplasm 2 */
    10: [11 ,12],                  # /*Neoplasm 3 */
    11: [12],                      # /*Neoplasm 4 */
    17: [18 ,19],                  # /*Diabetes 1 */
    18: [19],                      # /*Diabetes 2 */
    27: [28 ,29 ,80],              # /*Liver 1 */
    28: [29],                      # /*Liver 2 */
    46: [48],                      # /*Blood 1 */
    54: [55],                      # /*SA1 */
    57: [58],                      # /*Psychiatric 1 */
    70: [71 ,72 ,103 ,104 ,169],   # /*Spinal 1 */
    71: [72 ,104 ,169],            # /*Spinal 2 */
    72: [169],                     # /*Spinal 3 */
    82: [83 ,84],                  # /*Arrest 1 */
    83: [84],                      # /*Arrest 2 */
    86: [87 ,88],                  # /*Heart 2 */
    87: [88],                      # /*Heart 3 */
    99: [100],                     # /*CVD 1 */
    103: [104],                    # /*CVD 5 */
    106: [107 ,108 ,161 ,189],     # /*Vascular 1 */
    107: [108],                    # /*Vascular 2 */
    110: [111 ,112],               # /*Lung 1 */
    111: [112],                    # /*Lung 2 */
    114: [115],                    # /*Lung 5 */
    134: [135 ,136 ,137],          # /*Kidney 3 */
    135: [136 ,137],               # /*Kidney 4 */
    136: [137],                    # /*Kidney 5 */
    157: [158 ,161],               # /*Skin 1 */
    158: [161],                    # /*Skin 2 */
    166: [80 ,167],                # /*Injury 1 */
}


def impose_hierarchy(CC):
    """Takes a condition category list (CC[5]=1 means condition category
    5 is flagged) and imposes the hierarchy defined in `HCC_HIER_DICT`
    """
    # first copy the CC array into the HCC array
    hcc = cc.copy()

    # now impose the hiearchy
    for itop, izeros in HCC_HIER_DICT.items():
        if hcc[itop] == 1 and cc[itop] == 1:
            for izero in izeros:
                hcc[izero] = 0

    return hcc


def impose_hierarchy_2(diags_to_hccs):
    """Impose the hierarchy on a list of HCC objects.  `diags_to_hccs` is
    a list of objects of the form,

       {
           'diag_code': diag_code,
           'diag_type': diag_type,
           'cc': cc,
           'assign_type': assign_type,
       }

    """
    # add initial Hierarchical Condition Categories
    # (HCCs) that are copies of the CCs
    for el in diags_to_hccs:
        el['hcc'] = el['cc']

    # now impose the hiearchy
    for itop, izeros in HCC_HIER_DICT.items():

        # do we have this itop?
        have_itop = False
        for d2h in diags_to_hccs:
            if d2h['cc'] == itop:
                have_itop = True

        # if we do, reset all the izeros
        if have_itop:
            for izero in izeros:
                for d2h in diags_to_hccs:
                    if d2h['cc'] == izero:
                        d2h['hcc'] = 0

    return diags_to_hccs




if __name__ == '__main__':

    CC = [0] * (201 + 1)  # all zeros
    CC[17] = CC[18] = CC[19] = 1
    HCC = impose_hierarchy(CC)


    diags_to_hccs = [
        {'diag_code': 'DUMMY', 'diag_type': 'DUMMY',
         'assign_type': 'DUMMY', 'cc': 17},
        {'diag_code': 'DUMMY', 'diag_type': 'DUMMY',
         'assign_type': 'DUMMY', 'cc': 18},
        {'diag_code': 'DUMMY', 'diag_type': 'DUMMY',
         'assign_type': 'DUMMY', 'cc': 19},
    ]
    diags_to_hccs = impose_hierarchy_2(diags_to_hccs)
