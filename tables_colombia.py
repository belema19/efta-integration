import pandas as pd
from app.initializer import initialize, format_dataframe, filter_dataframe

DB = 'data/processed-data/colombia/main.csv'

DTYPES = {
    'Year': 'int16',
    'Partner': 'category',
    'Flow': 'category',
    'HSCode': 'category',
    'RealValue': 'float64'
    }

DF = initialize(DB)
DF = format_dataframe(DF, dtypes=DTYPES)
DF = DF.query('Partner not in ["World", "USA", "Iceland"]')

def pivot_tables(
        index:str|list,
        columns:str|list,
        values:str|list,
        aggfunc:str|list
        ):

    df = DF.copy()

    df_20012011 = filter_dataframe(df, period='2011')
    df_20122022 = filter_dataframe(df, period='2022')

    pivot_20012011 = df_20012011\
        .pivot_table(
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            observed=True
        )

    pivot_20122022 = df_20122022\
        .pivot_table(
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            observed=True
        )

    return [pivot_20012011, pivot_20122022]
