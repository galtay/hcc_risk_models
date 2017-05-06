"""
Handle the "formats" file that has all the data in the HCC model except
the regression coefficients.
"""
import os
import pandas


PATH_HERE = os.path.realpath(__file__)
DIR_HERE = os.path.split(PATH_HERE)[0]
DEFAULT_FNAME = os.path.join(DIR_HERE, 'F2217O1P.csv')

icd10_map_primary = 'I011722AS1Y16Y17PC'
icd10_map_duplicate = 'I011722AS2Y16Y17PC'
icd10_map_secondary = 'I011722AS3Y16Y17PC'

age_mce = 'IAGEHYBCY16MCE'
sex_mce = 'ISEXHYBCY16MCE'


class HccFormats:

    def __init__(self, fname=DEFAULT_FNAME):
        """Read CSV version of formats catalog file"""
        self.fname = fname
        self.df = pandas.read_csv(fname)
        self.parse_tables()

    def parse_tables(self):
        """Split the single DataFrame into tables (e.g. AGEL, AGEU, ...)"""
        self.tables = {}
        for fmtname in self.df['FMTNAME'].unique():
            tbl = self.df[self.df['FMTNAME']==fmtname]
            tbl = tbl.set_index('START')
            self.tables[fmtname] = tbl.copy()

    def validate_diag_type(self, diag_type, valid_diag_types):
        """Assert the diag_type is valid"""
        if diag_type not in valid_diag_types:
            raise ValueError('diag_type must be in {}'.format(valid_diag_types))

    def sedit_check_age(self, diag_code, age, diag_type):
        """Check MCE age restrictions on diagnosis code"""
        self.validate_diag_type(diag_type, [0])
        df = self.tables[age_mce]

        valid = True
        if diag_code in df.index:
            _tage = str(int(df.loc[diag_code]['LABEL']))
            age_lo = int(self.tables['AGEL'].loc[_tage]['LABEL'])
            age_hi = int(self.tables['AGEU'].loc[_tage]['LABEL'])
            if age < age_lo or age > age_hi:
                valid = False
        return valid

    def sedit_check_sex(self, diag_code, sex, diag_type):
        """Check MCE sex restrictions on diagnosis code"""
        self.validate_diag_type(diag_type, [0])
        df = self.tables[sex_mce]

        valid = True
        if diag_code in df.index:
            _tsex = int(df.loc[diag_code]['LABEL'])
            if _tsex != sex:
                valid = False
        return valid

    def cc_pri_assignment(self, diag_code, diag_type):
        """Primary diagnosis to condition category assignment"""
        self.validate_diag_type(diag_type, [0])
        df = self.tables[icd10_map_primary]
        cc = -1
        if diag_code in df.index:
            cc = int(df.loc[diag_code]['LABEL'])
        return cc

    def cc_dup_assignment(self, diag_code, diag_type):
        """Duplicate diagnosis to condition category assignment"""
        self.validate_diag_type(diag_type, [0])
        df = self.tables[icd10_map_duplicate]
        cc = -1
        if diag_code in df.index:
            cc = int(df.loc[diag_code]['LABEL'])
        return cc

    def cc_sec_assignment(self, diag_code, diag_type):
        """Secondary diagnosis to condition category assignment"""
        self.validate_diag_type(diag_type, [0])
        df = self.tables[icd10_map_secondary]
        cc = -1
        if diag_code in df.index:
            cc = int(df.loc[diag_code]['LABEL'])
        return cc

    def diag_to_ccs(self, diag_code, diag_type):
        """Diagnosis diagnosis to condition category assignment"""
        # create a list of dicts where each dict represents a condition category
        ccs = []
        if diag_type == 0:
            cc = self.cc_pri_assignment(diag_code, diag_type)
            if cc != -1:
                ccs.append({'cc': cc, 'assign_type': 'primary'})
            cc = self.cc_dup_assignment(diag_code, diag_type)
            if cc != -1:
                ccs.append({'cc': cc, 'assign_type': 'duplicate'})
            cc = self.cc_sec_assignment(diag_code, diag_type)
            if cc != -1:
                ccs.append({'cc': cc, 'assign_type': 'secondary'})
        else:
            raise ValueError('diag_type must be in [0]')

        # add common values to each dict
        ccs = [
            {'diag_code': diag_code, 'diag_type': diag_type,
             'cc': el['cc'], 'assign_type': el['assign_type']}
             for el in ccs]
        return ccs


    def return_diag_hcc_mappings(self):
        """Return a json friendly list of all mappings between ICD diagnosis
        codes and HCCs
        """
        all_mappings = []

        icd10_tables = [
            ('primary', self.tables[icd10_map_primary]),
            ('duplicate', self.tables[icd10_map_duplicate]),
            ('secondary', self.tables[icd10_map_secondary]),
        ]
        for assign_type, table in icd10_tables:
            for tup in table.itertuples():
                # little bit of cleanup (one row has "**OTHER**" for diag code)
                if tup.Index == '**OTHER**':
                    continue
                dh_mapping = {
                    'assignment_type': assign_type,
                    'diag_code': tup.Index,
                    'diag_type': 0,
                    'hcc_code': tup.LABEL,
                }
                all_mappings.append(dh_mapping)

        return all_mappings




if __name__ == '__main__':

    hcc_formats = HccFormats()

    # a few age tests
    diag_code = 'C9332'
    diag_type = 0
    age = 65
    assert(hcc_formats.sedit_check_age(diag_code, age, diag_type) is False)
    age = 3
    assert(hcc_formats.sedit_check_age(diag_code, age, diag_type) is True)

    # a few sex tests
    diag_code = 'C50321'
    diag_type = 0
    sex = 2
    assert(hcc_formats.sedit_check_sex(diag_code, sex, diag_type) is False)
    sex = 1
    assert(hcc_formats.sedit_check_sex(diag_code, sex, diag_type) is True)
