"""This module is for needed common operations"""
import pandas as pd
import numpy as np

DEFAULT = '../data/processed-data/main_df.csv'

COLS = {
    'refPeriodId': 'Year',
    'reporterDesc': 'Flow',
    'isOriginalClassification': 'HSCode',
    'partnerISO': 'Partner',
    'fobvalue': 'FobValue' 
}

DTYPES = {
    'Year': 'int16',
    'Partner': 'category',
    'Flow': 'category',
    'HSCode': 'category',
    'FobValue': 'float64'
}


def initialize(path=None):

    if not path:
        path = DEFAULT
    else: path = path

    df = pd.read_csv(path, encoding='latin1')

    return df


def format_dataframe(dataframe:pd.DataFrame, format='all', dtypes:dict={}, cols:dict={}) -> pd.DataFrame:

    df = dataframe

    if not dtypes:

        dtypes = DTYPES

    else: dtypes = dtypes

    if not cols:

        cols = COLS

    else: cols = cols

    match format:

        case 'all':

            df.rename(columns=cols, inplace=True)
            df = df.astype(dtypes)
            return df

        case 'cols':

            df.rename(columns=cols, inplace=True)
            return df

        case 'dtypes':

            df.astype(dtypes)
            return df
        
        case _:

            raise ValueError(f'Argument {format} not valid. Try: dtypes, cols, all')


def filter_dataframe(dataframe:pd.DataFrame=pd.DataFrame()\
                     , period:str='all'\
                     , partners:list[str]=[]\
                     ) -> pd.DataFrame:
    df = dataframe

    match period:
        case '2011':
            df = df.query('Year <= 2011')
        case '2022':
            df = df.query('Year >= 2012')
        case 'all':
            ...
        case _:
            raise ValueError('incorrect input on period arg')

    if partners:
        df = df.query(f'Partner in {partners}')
    else:
        print('partner arg was not passed. Filterng for all partners...')

    return df

def total_growth():

    df = filter_dataframe(period='2022')
    groups = df.groupby(['Year', 'Partner'], observed=False)['RealValue']\
        .sum()

    tw = groups.reset_index()
    tw = tw.query('Year == 2012 or Year == 2022')

    ptc = tw.groupby(['Year', 'Partner'], observed=False)['RealValue'].sum().pct_change(periods=17).fillna(0)
    ptc *= 100

    tw['PctChange'] = ptc.values

    return tw


def avg_growth():

    df = filter_dataframe(period='2022')
    groups = df.groupby(['Year', 'Partner'], observed=False)['RealValue']\
        .sum()

    pct_changes = groups.pct_change(periods=17).fillna(0)
    pct_changes = pct_changes.reset_index()

    groups = groups.reset_index()
    groups['PctChange'] = pct_changes['RealValue']

    avg_growth = groups.groupby('Partner', observed=False)['PctChange'].mean()
    avg_growth *= 100


    return avg_growth


if __name__ == "__main__":
   ... 