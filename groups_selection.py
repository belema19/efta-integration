import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

PATH = 'processed-data/'
FILE_NAME = 'hs4_20012011.csv'
COLS = {
    'refPeriodId': 'Year',
    'reporterDesc': 'Flow',
    'isOriginalClassification': 'HSCode',
    'partnerISO': 'Partner',
    'fobvalue': 'FobValue' 
}
if FILE_NAME in os.listdir(PATH):
    print(f'\nCleaning file "{FILE_NAME}"...')
else:
    raise Exception(f'\nPlease create the csv file: "{FILE_NAME}", first')

def create_dataframe() -> pd.DataFrame:
    """Creates and format dataframe from csv"""
    df = pd.read_csv(PATH + FILE_NAME, encoding='latin1')
    df.rename(columns=COLS, inplace=True)
    return df   

def filter_dataframe() -> pd.DataFrame:
    """Excludes World entries in col Partners"""
    df = create_dataframe()
    df = df.query('Partner != "World"')
    df['HSCode'] = df['HSCode'].astype('str').str.slice(0, 4)
    return df 
  
def group_dataframe() -> pd.DataFrame:
    """Groups by Partner, HSCode and Year"""
    df = filter_dataframe()
    df = df.groupby(['Partner', 'HSCode', 'Year'])['FobValue'].sum()\
        .reset_index()
    return df

def make_region_col() -> pd.DataFrame:
    """Creates col Region"""
    df = group_dataframe()
    conditions = [(df['Partner'] == 'Switzerland'), (df['Partner'] == 'Norway'), (df['Partner'] == 'Iceland')]
    choices = ['EFTA', 'EFTA', 'EFTA']
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

def adjust_dataframe() -> pd.DataFrame:
    """Filters  by EFTA top HS4 codes"""
    ls_hscodes = top_hscodes()
    df = make_region_col()
    df = df.query(f'HSCode in {ls_hscodes}')
    return df

def comparison_dataframe() -> pd.DataFrame:
    """
    Returns the bilateral commerce total value
    by selected HS4 codes, for each country
    """
    df = adjust_dataframe()
    df = df.groupby('Partner')['FobValue'].sum()\
        .reset_index()
    return df

def log_transformation() -> pd.DataFrame:
    """
    Converts FobValue Columns
    using algorithm transformation
    for magnitude comparison 
    """
    df = adjust_dataframe()
    df['FobValue'] = np.log1p(df['FobValue'])
    return df

def multiple_graphics() -> None:
    """
    Creates graphics to compare bilateral 
    commerce tendencies, one to various
    """
    df = log_transformation()
    fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(12, 10)) # Ajusta figsize si es necesario

    countries = ['Trinidad and Tobago', 'China', 'Panama', 'Chile', 'Aruba',
                 'Spain', 'India', 'Ecuador', 'Peru', 'Brazil']
    switzerland = df.query('Partner == "Switzerland"')
    axs_flat = axs.flatten()

    for i, country in enumerate(countries):

        df_country = df[df['Partner'] == country]
        sns.lineplot(x=df_country['Year'], y=df_country['FobValue'], errorbar='sd', label = f'{country}', ax=axs_flat[i])
        sns.lineplot(x=switzerland['Year'], y=switzerland['FobValue'], errorbar='sd', label = 'Switzerland', ax=axs_flat[i])
        axs_flat[i].set_title(country)

    plt.tight_layout()
    plt.show()

def single_graphics() -> None:
    """
    Creates graphics to compare bilateral
    commerce tendencies, one to one
    """
    df = log_transformation()


    A = ['USA', 'Trinidad and Tobago', 'China', 'Chile', 'Spain',
                 'India', 'Peru', 'Brazil', 'Mexico', 'Italy',
                 'Netherlands', 'Germany', 'France', 'Costa Rica']
    B = 'Switzerland'
    country_b = df[df['Partner'] == B]

    for country in A:
        country_a = df[df['Partner'] == country] 
        fig, ax = plt.subplots()

        sns.lineplot(x=country_a['Year'], y=country_a['FobValue'], label=country, ax=ax)
        sns.lineplot(x=country_b['Year'], y=country_b['FobValue'], label=B, ax=ax)

        plt.tight_layout()
        plt.savefig(f'{country}.png')
        plt.close(fig)

if __name__ == '__main__':
    ...