"""This module is for the exploratoy data analysis"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DB = 'processed-data/main_df.csv'
DTYPES = {
    'Year': 'int16',
    'Partner': 'category',
    'Flow': 'category',
    'Region': 'category',
    'HSCode': 'category',
    'RealValue': 'float64'
}

def initialize():
    df = pd.read_csv(DB, dtype=DTYPES)
    return df

def log_transform(grouped_df:pd.DataFrame) -> pd.DataFrame:
    df = grouped_df
    df['LogRealValue'] = np.log1p(df['RealValue'])
    return df

def translate_log_transform(grouped_df:pd.DataFrame) -> dict:
    values = grouped_df['LogRealValue']
    ref_dic = {k: np.expm1(k) for k in range(1, 25)} 
    return ref_dic
    
def group_dataframe():
    df = initialize()
    grouped_df = df.groupby(['Year', 'Partner', 'HSCode'], observed=False)['RealValue']\
        .sum().reset_index()
    return grouped_df

# --- Distributions --- 
def unidistributions_simple():
    df = initialize()
    df = log_transform(df)
    switz = df.query('Partner == "Switzerland"')
    partners = df['Partner'].unique()
    for partner in partners:
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fig.suptitle('Distributions')
        country_df = df[df['Partner'] == partner]

        sns.histplot(x=country_df['LogRealValue'], stat='percent', bins=20, kde=True, ax=ax[0])
        sns.histplot(x=switz['LogRealValue'], stat='percent', bins=20, kde=True, ax=ax[1])
        ax[0].set_title(partner)
        ax[1].set_title('Switzerland')
        
        plt.tight_layout()
        plt.show()
        plt.savefig(f'images/unidistributions/simple/bins20/udsb20_{partner}.png')
        plt.close()

def unidistribution_complex():
    df = initialize()
    df = log_transform(df)
    switz = df.query('Partner == "Switzerland"')
    partners = df['Partner'].unique()
    for partner in partners:
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fig.suptitle('Distributions')
        country_df = df[df['Partner'] == partner]

        sns.histplot(x=country_df['LogRealValue'], hue=country_df['HSCode'], element='step', stat='percent', bins=20, kde=True, ax=ax[0])
        sns.histplot(x=switz['LogRealValue'], hue=switz['HSCode'], element='step', stat='percent', bins=20, kde=True, ax=ax[1])
        ax[0].set_title(partner)
        ax[1].set_title('Switzerland')
        
        plt.tight_layout()
        plt.show()
        plt.savefig(f'images/unidistributions/complex/bins20/udcb20_{partner}.png')
        plt.close()

def bivariate_distribution():
    df = initialize()
    df = log_transform(df)
    switz = df.query('Partner == "Switzerland"')
    partners = df['Partner'].unique()
    for partner in partners:
        fig, ax = plt.subplots(nrows=1, ncols=2)
        fig.suptitle('Distributions')
        country_df = df[df['Partner'] == partner]

        sns.histplot(x=country_df['LogRealValue'], y=country_df['HSCode'], cbar=True, ax=ax[0])
        sns.histplot(x=switz['LogRealValue'], y=switz['HSCode'], cbar=True, ax=ax[1])
        ax[0].set_title(partner)
        ax[1].set_title('Switzerland')
        
        plt.tight_layout()
        plt.show()
        plt.savefig(f'images/bidistributions/bidistribution_{partner}.png')
        plt.close()

if __name__ == '__main__':
    print('Executing eda.py')