"""This module is for the exploratoy data analysis"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as mpatches

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
    pre_switz = switz[switz['Year'] <= 2011]
    post_switz = switz[switz['Year'] >= 2012]

    partners = df['Partner'].unique()

    for partner in partners:

        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), layout='constrained')
        fig.suptitle('Distributions')

        pre_df = df[(df['Partner'] == partner) & (df['Year'] <= 2011)]
        post_df = df[(df['Partner'] == partner) & (df['Year'] >= 2012)]
        bins = 20
        stat = 'count'

        sns.histplot(x=pre_df['LogRealValue'], stat=stat, bins=bins, kde=True, ax=ax[0][0])
        sns.histplot(x=pre_switz['LogRealValue'], stat=stat, bins=bins, kde=True, ax=ax[0][1])
        sns.histplot(x=post_df['LogRealValue'], stat=stat, bins=bins, kde=True, ax=ax[1][0])
        sns.histplot(x=post_switz['LogRealValue'], stat=stat, bins=bins, kde=True, ax=ax[1][1])

        ax[0][0].set_title('Pre TLC ' + partner)
        ax[0][1].set_title('Pre TLC Switzerland')
        ax[1][0].set_title('Post TLC ' + partner)
        ax[1][1].set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/unidistributions/simple/bins20/unisimb20_{partner}')
        plt.show()
        plt.close()

def unidistribution_complex():
    df = initialize()
    df = log_transform(df)

    switz = df.query('Partner == "Switzerland"')
    pre_switz = switz[switz['Year'] <= 2011]
    post_switz = switz[switz['Year'] >= 2012]

    partners = df['Partner'].unique()

    for partner in partners:

        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), layout='constrained')
        fig.suptitle('Distributions')

        pre_df = df[(df['Partner'] == partner) & (df['Year'] <= 2011)]
        post_df = df[(df['Partner'] == partner) & (df['Year'] >= 2012)]
        bins = 20
        stat = 'count'

        sns.histplot(x=pre_df['LogRealValue'], hue=pre_df['HSCode'], element='step', stat=stat, bins=bins, kde=True, ax=ax[0][0])
        sns.histplot(x=pre_switz['LogRealValue'], hue=pre_switz['HSCode'], element='step', stat=stat, bins=bins, kde=True, ax=ax[0][1])
        sns.histplot(x=post_df['LogRealValue'], hue=post_df['HSCode'], element='step', stat=stat, bins=bins, kde=True, ax=ax[1][0])
        sns.histplot(x=post_switz['LogRealValue'], hue=post_switz['HSCode'], element='step', stat=stat, bins=bins, kde=True, ax=ax[1][1])

        ax[0][0].set_title('Pre TLC ' + partner)
        ax[0][1].set_title('Pre TLC Switzerland')
        ax[1][0].set_title('Post TLC ' + partner)
        ax[1][1].set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/unidistributions/complex/bins20/unicomb20_{partner}.png')
        plt.show()
        plt.close()

def bivariate_distribution():
    df = initialize()
    df = log_transform(df)

    switz = df.query('Partner == "Switzerland"')
    pre_switz = switz[switz['Year'] <= 2011]
    post_switz = switz[switz['Year'] >= 2012]

    partners = df['Partner'].unique()

    for partner in partners:

        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), layout='constrained')
        fig.suptitle('Heatmaps')

        pre_df = df[(df['Partner'] == partner) & (df['Year'] <= 2011)]
        post_df = df[(df['Partner'] == partner) & (df['Year'] >= 2012)]
        bins = 20
        stat = 'count'

        sns.histplot(x=pre_df['LogRealValue'], y=pre_df['HSCode'], cbar=True, stat=stat, bins=bins, ax=ax[0][0])
        sns.histplot(x=pre_switz['LogRealValue'], y=pre_switz['HSCode'], cbar=True, stat=stat, bins=bins, ax=ax[0][1])
        sns.histplot(x=post_df['LogRealValue'], y=post_df['HSCode'], cbar=True, stat=stat, bins=bins, ax=ax[1][0])
        sns.histplot(x=post_switz['LogRealValue'], y=post_switz['HSCode'], cbar=True, stat=stat, bins=bins, ax=ax[1][1])

        ax[0][0].set_title('Pre TLC ' + partner)
        ax[0][1].set_title('Pre TLC Switzerland')
        ax[1][0].set_title('Post TLC ' + partner)
        ax[1][1].set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/bidistributions/bins20/bidisb20_{partner}.png')
        plt.show()
        plt.close()

if __name__ == '__main__':
    print('Executing eda.py')