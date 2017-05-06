import os
import pandas


PATH_HERE = os.path.realpath(__file__)
DIR_HERE = os.path.split(PATH_HERE)[0]
DEFAULT_LONG_FNAME = os.path.join(DIR_HERE, 'CMS32_DESC_LONG_DX.txt')
DEFAULT_SHORT_FNAME = os.path.join(DIR_HERE, 'CMS32_DESC_SHORT_DX.txt')


class Icd9CmDefinitions:

    def __init__(self,
                 fname_long=DEFAULT_LONG_FNAME,
                 fname_short=DEFAULT_SHORT_FNAME):

        # read short descriptions
        short_defs = pandas.read_fwf(
            fname_short,
            header=None,
            colspecs=[(0,5), (6,500)],
            names=['code', 'short_description']
        )

        # read long descriptions
        long_defs = pandas.read_fwf(
            fname_long,
            header=None,
            colspecs=[(0,5), (6,500)],
            names=['code', 'long_description']
        )

        df = pandas.merge(short_defs, long_defs, on='code')
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
            })
        return icd_json


if __name__ == '__main__':

    icd9 = Icd9CmDefinitions()
