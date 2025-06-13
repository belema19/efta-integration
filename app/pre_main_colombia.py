import pandas as pd
from initializer import format_dataframe, filter_dataframe, COLS

DB = '../data/processed-data/colombia/trade20012022.csv'
DEST = '../data/processed-data/colombia/pre_main.csv'

def get_df():

    cols = list(COLS.keys())
    df = pd.read_csv(DB, usecols=cols)
    df = format_dataframe(df)

    return df


def compare():

    df = get_df()

    df = filter_dataframe(df, period='2011')

    df = df.groupby('Partner')['FobValue'].sum().sort_values(ascending=False).reset_index()

    return df

def control_group() -> list[str]:

    df = compare()

    control_group = df.query('8.9e8 < FobValue < 67e9')

    control_group = control_group['Partner'].values

    result = list(control_group)
    result.extend(['Norway', 'Iceland', 'World'])

    return result

def adjust_dataframe():

    df = get_df()
    partners = control_group()
    df = df.query(f'Partner in {partners}').reset_index(drop=True)

    return df


if __name__ == '__main__':

    df = adjust_dataframe()
    df.to_csv(DEST, index=False, encoding='latin1')