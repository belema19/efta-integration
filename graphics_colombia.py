import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
from app.initializer import initialize, filter_dataframe
from tables_colombia import pivot_tables

def log_transform(dfs:list[pd.DataFrame]=[]) -> list[pd.DataFrame]:

    if not dfs:
        raise ValueError("dfs cannot be empty")
    
    result = []

    for df in dfs:

        if df.empty:
            result.append(df)

        else:
            df['LogRealValue'] = np.log1p(df['RealValue'])
            result.append(df)

    return result 

def get_df(which:str='') -> pd.DataFrame:
    
    if not which:
        raise ValueError(
            """
                Missing arg 'which' of type str
                options: all, partners, world
            """
        )

    df = initialize()

    match which:
        case 'all':
            pass
        case 'partners':
            df = df.query('Partner != "World"')
        case 'world':
            df = df.query('Partner == "World"')
        case _:
            raise ValueError(
                """
                    incorrect option.
                    valid options: all, partners, world
                """
            )
    
    return df




def graphic_dist():

    partners_df = get_df(which='partners')
    world_df = get_df(which='world')

    partners_df, world_df = \
        log_transform(
            [
                partners_df.copy(deep=True),
                world_df.copy(deep=True)
            ]
        )

    fig, axs = plt.subplot_mosaic([['boxplot'], ['histplot']], layout='constrained')

    sns.boxplot(x=partners_df['LogRealValue'], ax=axs['boxplot'])
    sns.histplot(x=partners_df['LogRealValue'], kde=True, ax=axs['histplot'])

    axs['boxplot'].set_ylabel('IQR')

    fig.suptitle('Bilateral Trade Distribution')
    plt.savefig('images/partners_dist_hscode.png')
    plt.show()


def graphic_dist_hscode():
    partners_df = get_df(which='partners')
    world_df = get_df(which='world')

    partners_df, world_df = \
        log_transform(
            [
                partners_df.copy(deep=True),
                world_df.copy(deep=True)
            ]
        )

    fig, axs = plt.subplot_mosaic([['boxplot'], ['histplot']], layout='constrained')

    sns.boxplot(x=partners_df['LogRealValue'], hue=partners_df['HSCode'], ax=axs['boxplot'])
    sns.histplot(x=partners_df['LogRealValue'], hue=partners_df['HSCode'], element='step', kde=True, ax=axs['histplot'])

    axs['boxplot'].set_ylabel('IQR')

    fig.suptitle('Bilateral Trade Distribution')
    plt.savefig('images/partners_dist_hscode.png')
    plt.show()


def graphic_heatmap():

    partners = [
                'Germany', 'China', 'Spain', 'USA',
                'Netherlands', 'Italy', 'India', 'Peru',
                'Trinidad and Tobago', 'Switzerland'
                ]

    period = '2022'
    variables = {'x': 'HSCode', 'y': 'LogRealValue'}
    hue = 'Flow'
    figtitle = 'Heatmap by Flow 2012-2022'

    df = initialize()
    df = filter_dataframe(df, period=period, partners=partners)
    df, _ = log_transform([df.copy(deep=True), pd.DataFrame()])


    fig, axs = plt.subplot_mosaic([['1', '2', '3'],
                                   ['4', '5', '6'],
                                   ['7', '8', '9'],
                                   ['10', '10', '10']],
                                   layout='constrained', figsize=(20, 12))

    axd = [ax for k, ax in axs.items()]
    
    for i, partner in enumerate(partners):

        pdf = df.query(f'Partner == "{partner}"')

        if hue:

            sns.histplot(x=pdf[variables['x']], y=pdf[variables['y']], hue=pdf[hue], ax=axd[i])

        else:

            sns.histplot(x=pdf[variables['x']], y=pdf[variables['y']], ax=axd[i])

        axd[i].set_title(f'{partner}')
        axd[i].set_ylabel('')
        axd[i].set_xlabel('')

    fig.suptitle(figtitle)
    fig.supylabel(variables['y'])
    fig.supxlabel(variables['x'])

    plt.savefig('images/bidistributions/heamap20122022.png')
    plt.show()


def graphic_tend_hscodes():

    partners = [
                'Germany', 'China', 'Spain', 'USA',
                'Netherlands', 'Italy', 'India', 'Peru',
                'Trinidad and Tobago', 'Switzerland'
                ]

    df = initialize()
    df = filter_dataframe(df, period='all', partners=partners)
    df = df.groupby(['Year', 'Partner', 'HSCode'], observed=True)['RealValue'].sum().reset_index()
    df['LogRealValue'] = np.log1p(df['RealValue'])

    fig, axs = plt.subplot_mosaic([['1', '2', '3'],
                                   ['4', '5', '6'],
                                   ['7', '8', '9'],
                                   ['10', '10', '10']],
                                   layout='constrained', figsize=(20, 12))

    axd = [ax for k, ax in axs.items()]
    
    for i, partner in enumerate(partners):

        pdf = df.query(f'Partner == "{partner}"')

        sns.lineplot(x=pdf['Year'], y=pdf['LogRealValue'], hue=pdf['HSCode'], errorbar=None, legend=False, ax=axd[i])

        axd[i].set_title(f'{partner}')
        axd[i].set_ylabel('')
        axd[i].set_xlabel('')

    hscodes = pd.unique(df['HSCode']).astype('int')
    hscodes.sort()
    hscodes = hscodes.astype(str)
    
    fig.legend(hscodes, loc='upper right', ncols=5, bbox_to_anchor=(1, 1.05), title='HSCode')

    fig.suptitle('HSCode Tendency')
    fig.supylabel('LogRealValue')
    fig.supxlabel('Year')

    plt.savefig('images/tendencies/tend_hscode.png', bbox_inches='tight')
    plt.show()


def graphic_tend_flow():

    partners = [
                'Germany', 'China', 'Spain', 'USA',
                'Netherlands', 'Italy', 'India', 'Peru',
                'Trinidad and Tobago', 'Switzerland'
                ]

    df = initialize()
    df = filter_dataframe(df, period='all', partners=partners)
    df = df.groupby(['Partner', 'Year', 'Flow'], observed=True)['RealValue'].sum().reset_index()

    fig, axs = plt.subplot_mosaic([['1', '2', '3'],
                                   ['4', '5', '6'],
                                   ['7', '8', '9'],
                                   ['10', '10', '10']],
                                   layout='constrained', figsize=(20, 12))

    axd = [ax for k, ax in axs.items()]
    
    for i, partner in enumerate(partners):

        pdf = df.query(f'Partner == "{partner}"')

        sns.lineplot(x=pdf['Year'], y=pdf['RealValue'], hue=pdf['Flow'], errorbar=None, legend=True, ax=axd[i])

        axd[i].set_title(f'{partner}')
        axd[i].set_ylabel('')
        axd[i].set_xlabel('')

    fig.legend(['M', 'X'], loc='upper right', ncols=3, bbox_to_anchor=(1, 1.05), title='Flow')

    fig.suptitle('Flow Tendency')
    fig.supylabel('RealValue')
    fig.supxlabel('Year')

    #plt.savefig('images/tendencies/tend_flow.png', bbox_inches='tight')
    plt.show()


def contingency_table(pivot_tables:list):

    """Input: 2 pivot tables"""

    fig, (ax0, ax1) = plt.subplots(
        ncols=2,
        figsize=(22,12),
        layout='constrained'
        )

    color_pallete = sns.color_palette("ch:s=.25,rot=-.25", as_cmap=True)
    font_axes = FontProperties(family='Times New Roman', weight='bold', size=14)
    font_fig = FontProperties(family='Times New Roman', weight='bold', size=20)

    fig.suptitle('Contingency Table', fontproperties=font_fig)

    g1 = sns.heatmap(
        pivot_tables[0], 
        cmap=color_pallete,
        annot=True,
        vmin=0.1e9,
        vmax=1e9,
        linewidths=.7,
        ax=ax0
        )

    g2 = sns.heatmap(pivot_tables[1],
                     cmap=color_pallete,
                     annot=True,
                     vmin=0.1e9,
                     vmax=1e9,
                     linewidths=.7,
                     ax=ax1
                     )

    ax0.set_title('Period 2001-2011', fontproperties=font_axes, pad=20)
    ax0.set_xlabel('')
    ax0.set_ylabel('')

    ax1.set_title('Period 2012-2022', fontproperties=font_axes, pad=20)
    ax1.set_xlabel('')
    ax1.set_ylabel('')


if __name__ == '__main__':

    print('Executing graphics_colombia.py')

    tables = pivot_tables(
        index='HSCode',
        columns='Partner',
        values='RealValue',
        aggfunc='sum'
        )

    contingency_table(tables)