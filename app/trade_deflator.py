import pandas as pd
from initializer import initialize, format_dataframe

# --- Cargar índice de precios ---
CPI = '../data/raw-data/consumer-price-index/cpi.csv'
COUNTRY = 'colombia'
DF = f'../data/processed-data/{COUNTRY}/pre_main.csv'
DEST = f'../data/processed-data/{COUNTRY}/main.csv'

df_infalted = initialize(path=DF)
df_infalted = format_dataframe(df_infalted)

colums_to_load = [str(x) for x in range(2001, 2023)]
colums_to_load.append('Country Code')

def cpi():
    df_deflator = pd.read_csv(CPI, usecols=colums_to_load)
    return df_deflator

def filter_dataframe():
    df_deflator = cpi()
    df_deflator = df_deflator[df_deflator['Country Code'] == 'USA'] # Filtrar por Country Code
    df_deflator = df_deflator.drop(columns=['Country Code']) # Eliminar la columna Country Code
    return df_deflator

def adjust_dataframe():
    df_deflator = filter_dataframe()
    df_deflator = pd.melt(df_deflator, id_vars=[], var_name='Year', value_name='Index')
    df_deflator['Year'] = df_deflator['Year'].astype('int16')
    return df_deflator

def merge_dataframes(inflated_dataframe:pd.DataFrame) -> pd.DataFrame:
    df_deflator = adjust_dataframe()
    df_inflated = inflated_dataframe
    df_merged = pd.merge(df_inflated, df_deflator[['Year', 'Index']], on='Year', how='left')
    return df_merged

def deflated_dataframe():
    df_deflated = merge_dataframes(df_infalted)
    df_deflated['RealValue'] = df_deflated['FobValue'] / (df_deflated['Index'] / 100)
    df_deflated = df_deflated.drop(columns=['FobValue', 'Index'])
    return df_deflated

if __name__ == '__main__':

    print(f'Saving {COUNTRY} main.csv...')

    df = deflated_dataframe()

    df.to_csv(DEST, index=False, encoding='latin1')