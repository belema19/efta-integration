import pandas as pd

# --- Cargar índice de precios ---
DB = 'raw-data/consumer-price-index/cpi.csv'
colums_to_load = [str(x) for x in range(2001, 2023)]
colums_to_load.append('Country Code')

def initialize():
    df_deflator = pd.read_csv(DB, usecols=colums_to_load)
    return df_deflator

def filter_dataframe():
    df_deflator = initialize()
    df_deflator = df_deflator[df_deflator['Country Code'] == 'USA'] # Filtrar por Country Code
    df_deflator = df_deflator.drop(columns=['Country Code']) # Eliminar la columna Country Code
    return df_deflator

def adjust_dataframe():
    df_deflator = filter_dataframe()
    df_deflator = pd.melt(df_deflator, id_vars=[], var_name='Year', value_name='Index')
    df_deflator['Year'] = df_deflator['Year'].astype('int16')
    return df_deflator

def merge_dataframes():
    from main_df import optimized_dataframe
    df_deflator = adjust_dataframe()
    df_inflated = optimized_dataframe()
    df_deflated = pd.merge(df_inflated, df_deflator[['Year', 'Index']], on='Year', how='left')
    return df_deflated

def deflated_dataframe():
    df_deflated = merge_dataframes()
    df_deflated['RealValue'] = df_deflated['FobValue'] / (df_deflated['Index'] / 100)
    df_deflated = df_deflated.drop(columns=['FobValue', 'Index'])
    return df_deflated