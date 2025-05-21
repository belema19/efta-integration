"""This module creates an unified csv from others csv"""

import os
import pandas as pd

PATH = 'raw-data/'
DEST_PATH = 'processed-data/'
FILE_NAME = 'trade_20012022.csv'
COLS = ['refPeriodId', 'reporterDesc', 'partnerISO', 'isOriginalClassification', 'fobvalue']

def get_files() -> list[str]:
    data = [f for f in os.listdir(f'{PATH}') if f.endswith('.csv')]
    print(f'\nFound files: {data}')
    return data

def read_files() -> list[pd.DataFrame]:
    data = get_files()
    frames = []
    print('\nReading files...')

    for file in data:
        try:
            tmp = pd.read_csv(PATH+file, encoding='latin1', usecols=COLS) 
            frames.append(tmp)
            print(f'\n{file} read successfully')
        except Exception as e:
            print(f'\nError reading {file}: {e}')
            
    return frames

def create_dataframe() -> pd.DataFrame:
    frames = read_files()
    if frames:
        print('\nMaking the dataframe...')
        df = pd.concat(frames, ignore_index=True)
        print('\nDataframe created')
    else:
        raise ValueError('Frames cannot be empty')
        
    return df

def save_dataframe() -> None:
    df = create_dataframe()
    file_name = FILE_NAME
    try:
        print('\nSaving dataframe to csv...')
        df.to_csv(DEST_PATH + file_name, index=False)
        print('\nDataframe saved')
    except Exception as e:
        print(f'something went wrong saving the dataframe: {e}')
        
        
if __name__ == '__main__':
    save_dataframe()