import os
import pandas


PATH_HERE = os.path.realpath(__file__)
DIR_HERE = os.path.split(PATH_HERE)[0]
DEFAULT_ORDER_FNAME = os.path.join(DIR_HERE, 'icd10cm_order_2017.txt')


class Icd10Definitions:

    def __init__(self, fname=DEFAULT_ORDER_FNAME):

        # read order file
        df = pandas.read_fwf(
            fname,
            header=None,
            colspecs=[(0,5), (6,13), (14,15), (16,76), (77,500)],
            names=['order_number', 'code', 'is_valid', 'short_description',
                   'long_description']
        )

        # set `code` as index
        df = df.set_index('code')
        self.df = df

    def return_short_description(self, code):
        return self.df.loc[code, 'short_description']

    def return_long_description(self, code):
        return self.df.loc[code, 'long_description']

    def return_json(self):
        icd_json = []
        for row in self.df.itertuples():
            icd_json.append({
                'code': row.Index,
                'short_description': row.short_description,
                'long_description': row.long_description,
                'is_valid': row.is_valid,
            })
        return icd_json

if __name__ == '__main__':

    icd10 = Icd10Definitions()
