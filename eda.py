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
    
def group_dataframe(groups:list[str]) -> pd.Series:
    df = initialize()
    grouped_df = df.groupby(groups, observed=False)['RealValue']\
        .sum()
    return grouped_df

def get_pct_change(grouped_df:pd.Series, periods:int) -> pd.Series:
    s = grouped_df
    s = s.pct_change(periods=periods).fillna(0)
    return s




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



# --- Tendencias ---
def simple_total_tendencies():
    df = group_dataframe(['Year', 'Partner', 'HSCode', 'Flow'])
    df = df.reset_index()
    df = log_transform(df)

    switz = df.query('Partner == "Switzerland"')
    pre_switz = switz[switz['Year'] <= 2011]
    post_switz = switz[switz['Year'] >= 2012]

    partners = df['Partner'].unique()

    for partner in partners:

        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), layout='constrained')
        fig.suptitle('Tendencies')

        pre_df = df[(df['Partner'] == partner) & (df['Year'] <= 2011)]
        post_df = df[(df['Partner'] == partner) & (df['Year'] >= 2012)]

        sns.lineplot(x=pre_df['Year'], y=pre_df['LogRealValue'], ax=ax[0][0])
        sns.lineplot(x=pre_switz['Year'], y=pre_switz['LogRealValue'], ax=ax[0][1])
        sns.lineplot(x=post_df['Year'], y=post_df['LogRealValue'], ax=ax[1][0])
        sns.lineplot(x=post_switz['Year'], y=post_switz['LogRealValue'], ax=ax[1][1])

        ax[0][0].set_title('Pre TLC ' + partner)
        ax[0][1].set_title('Pre TLC Switzerland')
        ax[1][0].set_title('Post TLC ' + partner)
        ax[1][1].set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/tendencies/simple/total/tensimtot_{partner}.png')
        plt.show()
        plt.close()

def simple_flow_tendencies():
    df = group_dataframe(['Year', 'Partner', 'HSCode', 'Flow'])
    df = df.reset_index()
    df = log_transform(df)

    switz = df.query('Partner == "Switzerland"')
    pre_switz = switz[switz['Year'] <= 2011]
    post_switz = switz[switz['Year'] >= 2012]

    partners = df['Partner'].unique()

    for partner in partners:

        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), layout='constrained')
        fig.suptitle('Tendencies')

        pre_df = df[(df['Partner'] == partner) & (df['Year'] <= 2011)]
        post_df = df[(df['Partner'] == partner) & (df['Year'] >= 2012)]

        sns.lineplot(x=pre_df['Year'], y=pre_df['LogRealValue'], hue=pre_df['Flow'], ax=ax[0][0])
        sns.lineplot(x=pre_switz['Year'], y=pre_switz['LogRealValue'], hue=pre_switz['Flow'], ax=ax[0][1])
        sns.lineplot(x=post_df['Year'], y=post_df['LogRealValue'], hue=post_df['Flow'], ax=ax[1][0])
        sns.lineplot(x=post_switz['Year'], y=post_switz['LogRealValue'], hue=post_switz['Flow'], ax=ax[1][1])

        ax[0][0].set_title('Pre TLC ' + partner)
        ax[0][1].set_title('Pre TLC Switzerland')
        ax[1][0].set_title('Post TLC ' + partner)
        ax[1][1].set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/tendencies/simple/flow/tensimflo_{partner}.png')
        plt.show()
        plt.close()

def complex_total_tendencies():
    df = group_dataframe(['Year', 'Partner', 'HSCode', 'Flow'])
    df = df.reset_index()
    df = log_transform(df)

    switz = df.query('Partner == "Switzerland"')
    pre_switz = switz[switz['Year'] <= 2011]
    post_switz = switz[switz['Year'] >= 2012]

    partners = df['Partner'].unique()

    for partner in partners:

        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 12), layout='constrained')
        fig.suptitle('Tendencies')

        pre_df = df[(df['Partner'] == partner) & (df['Year'] <= 2011)]
        post_df = df[(df['Partner'] == partner) & (df['Year'] >= 2012)]

        sns.barplot(x=pre_df['Year'], y=pre_df['LogRealValue'], hue=pre_df['HSCode'], errorbar=None, ax=ax[0][0])
        sns.barplot(x=pre_switz['Year'], y=pre_switz['LogRealValue'], hue=pre_switz['HSCode'], errorbar=None, ax=ax[0][1])
        sns.barplot(x=post_df['Year'], y=post_df['LogRealValue'], hue=post_df['HSCode'], errorbar=None, ax=ax[1][0])
        sns.barplot(x=post_switz['Year'], y=post_switz['LogRealValue'], hue=post_switz['HSCode'], errorbar=None, ax=ax[1][1])

        ax[0][0].set_title('Pre TLC ' + partner)
        ax[0][1].set_title('Pre TLC Switzerland')
        ax[1][0].set_title('Post TLC ' + partner)
        ax[1][1].set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/tendencies/complex/total/tencomtot_{partner}.png')
        plt.show()
        plt.close()

def complex_flow_tendencies():
    df = group_dataframe(['Year', 'Partner', 'HSCode', 'Flow'])
    df = df.reset_index()
    df = log_transform(df)

    switz = df.query('Partner == "Switzerland"')
    pre_mswitz = switz[(switz['Flow'] == 'M') & (switz['Year'] <= 2011)]
    pre_xswitz = switz[(switz['Flow'] == 'X') & (switz['Year'] <= 2011)]
    post_mswitz = switz[(switz['Flow'] == 'M') & (switz['Year'] >= 2012)]
    post_xswitz = switz[(switz['Flow'] == 'X') & (switz['Year'] >= 2012)]

    partners = df['Partner'].unique()

    for partner in partners:

        # Instanties figure and subfigures with axes
        fig = plt.figure(figsize=(24, 16), layout='constrained')
        fig.suptitle('Tendencies')

        fig_up, fig_down = fig.subfigures(nrows=2, ncols=1)
        axs_up = fig_up.subplots(nrows=2, ncols=2)
        axs_down = fig_down.subplots(nrows=2, ncols=2)

        fig_up.suptitle('Imports')
        fig_down.suptitle('Exports')

        # filters dataframes
        pre_mdf = df[(df['Partner'] == partner) & (df['Flow'] == 'M') & (df['Year'] <= 2011)]
        pre_xdf = df[(df['Partner'] == partner) & (df['Flow'] == 'X') & (df['Year'] <= 2011)]
        post_mdf = df[(df['Partner'] == partner) & (df['Flow'] == 'M') & (df['Year'] >= 2012)]
        post_xdf = df[(df['Partner'] == partner) & (df['Flow'] == 'X') & (df['Year'] >= 2012)]

        # Create artists for each axe
        ## Imports
        au00 = axs_up[0][0]
        gu1 = sns.barplot(x=pre_mdf['Year'], y=pre_mdf['LogRealValue'], hue=pre_mdf['HSCode'], errorbar=None, ax=au00)

        au01 = axs_up[0][1]
        gu2 = sns.barplot(x=pre_mswitz['Year'], y=pre_mswitz['LogRealValue'], hue=pre_mswitz['HSCode'], errorbar=None, ax=au01)

        au10 = axs_up[1][0]
        gu3 = sns.barplot(x=post_mdf['Year'], y=post_mdf['LogRealValue'], hue=post_mdf['HSCode'], errorbar=None, ax=au10)

        au11 = axs_up[1][1]
        gu4 = sns.barplot(x=post_mswitz['Year'], y=post_mswitz['LogRealValue'], hue=post_mswitz['HSCode'], errorbar=None, ax=au11)

        ## Exports
        ad00 = axs_down[0][0]
        gd1 = sns.barplot(x=pre_xdf['Year'], y=pre_xdf['LogRealValue'], hue=pre_xdf['HSCode'], errorbar=None, ax=ad00)

        ad01 = axs_down[0][1]
        gd2 = sns.barplot(x=pre_xswitz['Year'], y=pre_xswitz['LogRealValue'], hue=pre_xswitz['HSCode'], errorbar=None, ax=ad01)

        ad10 = axs_down[1][0] 
        gd3 = sns.barplot(x=post_xdf['Year'], y=post_xdf['LogRealValue'], hue=post_xdf['HSCode'], errorbar=None, ax=ad10)

        ad11 = axs_down[1][1]
        gd4 = sns.barplot(x=post_xswitz['Year'], y=post_xswitz['LogRealValue'], hue=post_xswitz['HSCode'], errorbar=None, ax=ad11)

        # Axes titles
        au00.set_title('Pre TLC ' + partner)
        au01.set_title('Pre TLC Switzerland')
        au10.set_title('Post TLC ' + partner)
        au11.set_title('Post TLC Switzerland')

        ad00.set_title('Pre TLC ' + partner)
        ad01.set_title('Pre TLC Switzerland')
        ad10.set_title('Post TLC ' + partner)
        ad11.set_title('Post TLC Switzerland')
        
        plt.savefig(f'images/tendencies/complex/flow/tencomflo_{partner}.png')
        plt.show()
        plt.close()
    
    

# Growth Rates
def simple_growth_rate():

    s = group_dataframe(['Year', 'Partner'])
    pct_change = get_pct_change(s, 17).reset_index()
    pct_change.rename(columns={'RealValue': 'GrowthRate'}, inplace=True)
    
    switz = pct_change.query('Partner == "Switzerland"')
    pre_switz = switz.query('Year <= 2011')
    post_switz = switz.query('Year >= 2012')
    
    partners = pct_change['Partner'].unique()

    for partner in partners:

        pre_df = pct_change.query(f'(Partner == "{partner}") & (Year <= 2011)')
        post_df = pct_change.query(f'(Partner == "{partner}") & (Year >= 2012)')

        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(20, 12), layout='constrained')
        fig.suptitle('Growth Rates')

        ax00, ax01, ax10, ax11 = axs.flat

        sns.lineplot(x=pre_df['Year'], y=pre_df['GrowthRate'], errorbar=None, ax=ax00)
        sns.lineplot(x=pre_switz['Year'], y=pre_switz['GrowthRate'], errorbar=None, ax=ax01)

        sns.lineplot(x=post_df['Year'], y=post_df['GrowthRate'], errorbar=None, ax=ax10)
        sns.lineplot(x=post_switz['Year'], y=post_switz['GrowthRate'], errorbar=None, ax=ax11)

        ax00.set_title(f'Pre TLC {partner}')
        ax10.set_title(f'Post TLC {partner}')

        ax01.set_title('Pre TLC Switzerland')
        ax11.set_title('Post TLC Switzerland')

        plt.savefig(f'images/growth-rates/simple/groratsim_{partner}.png')
        plt.show()
        plt.close()

def complex_growth_rate():

    s = group_dataframe(['Year', 'Partner', 'HSCode'])
    pct_change = get_pct_change(s, 85).reset_index()
    pct_change.replace([np.inf, -np.inf], 0, inplace=True)
    pct_change.rename(columns={'RealValue': 'GrowthRate'}, inplace=True)
    
    switz = pct_change.query('Partner == "Switzerland"')
    pre_switz = switz.query('Year <= 2011')
    post_switz = switz.query('Year >= 2012')
    
    partners = pct_change['Partner'].unique()

    for partner in partners:

        pre_df = pct_change.query(f'(Partner == "{partner}") & (Year <= 2011)')
        post_df = pct_change.query(f'(Partner == "{partner}") & (Year >= 2012)')

        fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(20, 12), layout='constrained')
        fig.suptitle('Growth Rates')

        ax00, ax01, ax10, ax11 = axs.flat

        sns.lineplot(x=pre_df['Year'], y=pre_df['GrowthRate'], hue=pre_df['HSCode'], errorbar=None, ax=ax00)
        sns.lineplot(x=pre_switz['Year'], y=pre_switz['GrowthRate'], hue=pre_switz['HSCode'], errorbar=None, ax=ax01)

        sns.lineplot(x=post_df['Year'], y=post_df['GrowthRate'], hue=post_df['HSCode'], errorbar=None, ax=ax10)
        sns.lineplot(x=post_switz['Year'], y=post_switz['GrowthRate'], hue=post_switz['HSCode'], errorbar=None, ax=ax11)

        ax00.set_title(f'Pre TLC {partner}')
        ax10.set_title(f'Post TLC {partner}')

        ax01.set_title('Pre TLC Switzerland')
        ax11.set_title('Post TLC Switzerland')

        plt.savefig(f'images/growth-rates/complex/groratcom_{partner}.png')
        plt.show()
        plt.close()

    


if __name__ == '__main__':
    print('Executing eda.py')