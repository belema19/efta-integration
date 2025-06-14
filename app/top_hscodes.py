import pandas as pd
import numpy as np
import os
from initializer import filter_dataframe, COLS


PATH = '../data/processed-data/colombia/allhscodes/'
FILE_NAME = 'trade20012022.csv'


def get_df():

    cols = list(COLS.keys())
    df = pd.read_csv(PATH+FILE_NAME, usecols=cols)
    df.rename(columns=COLS, inplace=True)

    return df


def slice_hscode() -> pd.DataFrame:
    """Selects HSCode's first 4 digits"""

    df = get_df()

    df['HSCode'] = df['HSCode'].astype('str').str.slice(0, 4)

    return df 


def group_dataframe() -> pd.DataFrame:
    """Groups by Partner, HSCode and Year"""
    tmp = slice_hscode()
    df = filter_dataframe(dataframe=tmp, period='2011')
    df = df.groupby(['Partner', 'HSCode', 'Year'])['FobValue']\
        .sum().reset_index()
    return df


def make_region_col() -> pd.DataFrame:
    """Creates col Region"""
    df = group_dataframe()
    conditions = [(df['Partner'] == 'Switzerland'), (df['Partner'] == 'Norway'), (df['Partner'] == 'Iceland'), df['Partner'] == 'World']
    choices = ['EFTA', 'EFTA', 'EFTA', 'World']
    default = 'NO EFTA'
    df['Region'] = np.select(condlist=conditions, choicelist=choices, default=default) 
    return df


def top_hscodes() -> list[str]:
    """Finds EFTA top HS4 codes"""
    df = make_region_col()
    df = df.query('Region == "EFTA"')\
        .groupby('HSCode')['FobValue']\
        .sum().nlargest(5)
    ls_hscodes = list(df.index)
    return ls_hscodes