"""This module is for cleaning and optimizing
    the main dataframe"""
from groups_selection import create_dataframe
from trade_deflator import deflated_dataframe
import pandas as pd
import numpy as np

DEST_PATH = 'processed-data/main_df.csv'

# Avoid repetition: use previously
# created "create_dataframe()" from
# groups_selection.py
def initialize_dataframe():
    """read and select the HS4 codes"""
    df = create_dataframe()
    df['HSCode'] = df['HSCode'].astype('str').str.slice(0, 4)
    df = df.query('HSCode in ["7108", "7112", "2709", "3212", "3004"]')
    return df

def filter_dataframe():
    """Filters by selected partners"""
    df = initialize_dataframe()
    partners = ['Switzerland', 'Norway','Iceland', 'World', 'USA',
                'Trinidad and Tobago', 'Spain', 'Peru', 'Netherlands',
                'Mexico', 'Italy', 'India', 'Germany', 'France', 'Costa Rica',
                'China', 'Brazil']
    df = df.query(f'Partner in {partners}')
    return df

def make_col_region():
    """Creates Region column"""
    df = filter_dataframe()
    conditons = [df['Partner'] == 'Switzerland', df['Partner'] == 'Norway',
                 df['Partner'] == 'Iceland', df['Partner'] == 'World']
    choices = ['EFTA', 'EFTA', 'EFTA', 'World']
    default = 'NO EFTA'

    df['Region'] = np.select(condlist=conditons, choicelist=choices, default=default)
    return df

def optimized_dataframe():
    """optimize dataframe memory usage"""
    df = make_col_region()
    int_columns = ['Year', 'HSCode']
    cat_cols = ['Flow', 'Partner', 'Region']

    for col in int_columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    for col in cat_cols:
        df[col] = df[col].astype('category')
       
    #df.memory_usage(deep=True)
    return df

# Here we created the deflator.py module,
# for creating the RealValue column
def save_main_df():
    df = deflated_dataframe()
    df.to_csv(DEST_PATH, index=False)

if __name__ == '__main__':
    print('Executing main.py')
    save_main_df()