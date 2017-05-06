"""
Handles regression coefficients.
"""

import os
import pandas


DESCRIPTIONS = {
    'C2110H2R': 'coefficients for 3 regression models developed using CY2006/2007 data and CMS denominator 8,034.71 (1/18/2010)',
    'C1209J2Y': 'coefficients for 4 regression models developed using CY2008/2009 data and CMS denominator 9,004.65 (1/8/2012)',
    'C2211L4P': 'coefficients for 4 regression models developed using CY2010/2011 data and CMS denominator 9,276.26 (3/22/2013)',
    'C2214O5P': 'coefficients for 9 regression models developed using CY2013/2014 data and CMS denominator 9,185.29 (3/6/2016)',
}

DENOMINATORS = {
    'C2110H2R': 8034.71,
    'C1209J2Y': 9004.65,
    'C2211L4P': 9276.26,
    'C2214O5P': 9185.29,
}



class Coefficients:

    def __init__(self, fname):
        # get coefficients label
        label = os.path.split(fname)[-1].split('.')[0]

        # put the coefficients into a pandas Series
        df = pandas.read_csv(fname).loc[0]
        self.df = df

        self.cms_denominator = DENOMINATORS[label]
        self.description = DESCRIPTIONS[label]

    def __getitem__(self, key):
        return self.df[key]

    def to_json(self):
        result = {
            'description': self.description,
            'cms_denominator': self.cms_denominator,
            'values': self.df.to_dict(),
        }
        return result

if __name__ == '__main__':

    fname = 'C2211L4P.csv'
    coeffs = Coefficients(fname)
