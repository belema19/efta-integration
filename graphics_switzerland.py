import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DB = 'processed-data/switzerland/main.csv'

DTYPES = {
    'Year': 'int16',
    'Partner': 'category',
    'Flow': 'category',
    'HSCode': 'category',
    'FobValue': 'float64'
}

DF = pd.read_csv(DB, dtype=DTYPES, encoding='latin1')

def filter_flow():

    df = DF.copy(deep=True)

    df = df.query('Flow in ["M", "X"]').reset_index(drop=True)

    return df

def compare():

    df = filter_flow()

    df = df.groupby('Partner', observed=False)['RealValue'].sum().sort_values(ascending=False).reset_index()

    return df

def control_group() -> list[str]:

    df = compare()

    control_group = df.query('4.7e9 < RealValue < 7.3e9')

    control_group = control_group['Partner'].values

    result = []

    for partner in control_group:

        result.append(partner)

    return result


def compare_tendency():

    partners = control_group()

    df = filter_flow()

    df = df.groupby(['Year', 'Partner', 'HSCode'], observed=False)['RealValue'].sum().reset_index()

    df['LogRealValue'] = np.log1p(df['RealValue'])

    fig, axs = plt.subplots(nrows=3, ncols=4, layout='constrained')

    axs = axs.flat

    for i, partner in enumerate(partners):

        query = df.query(f'Partner == "{partner}"')

        sns.lineplot(x=query['Year'], y=query['RealValue'], hue=query['HSCode'], ax=axs[i], legend=False)

        cordinates = query.query('Year == 2011 and HSCode == "7108"')
        y_cordinate = cordinates['RealValue'].values

        axs[i].annotate(
            '2011',
            xy=(2011, y_cordinate),
            xytext=(2001, 2.5e8),
            arrowprops=dict(facecolor='black', shrink=0.05)
        )

        axs[i].set_title(f'{partner}')
        axs[i].set_ylabel('')
        axs[i].set_xlabel('')
    
    fig.suptitle('Tendencies')
    fig.supylabel('RealValue')
    fig.supxlabel('Year')

    plt.show()

def colombia():

    df = filter_flow()

    query = df.query('Partner == "Colombia"').reset_index(drop=True)

    query = query.groupby(['Partner', 'Year', 'HSCode'], observed=True)['RealValue'].sum().reset_index()

    query['LogRealValue'] = np.log1p(query['RealValue'])

    fig, ax = plt.subplots()

    sns.lineplot(x=query['Year'], y=query['RealValue'], hue=query['HSCode'], legend=False)

    cordinates = query.query('Year == 2011 and HSCode == "3004"')
    y_cordinate = cordinates['RealValue'].values

    ax.annotate(
        '2011',
        xy=(2011, y_cordinate), # type: ignore
        xytext=(2005, 5e8),
        arrowprops=dict(facecolor='black', shrink=0.05)
    )

    fig.legend(['M', 'X'])

    plt.show()
