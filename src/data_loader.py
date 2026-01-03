import pandas as pd

def load_csv(file):
    df = pd.read_csv(
        file,
        sep=';',
        decimal=',',
        skiprows=5,        # <<< PULA ATÉ O HEADER REAL
        engine='python',
        encoding='utf-8'
    )
    return df
