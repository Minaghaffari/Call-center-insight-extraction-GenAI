import pandas as pd


def get_drs_calls_list(df):
    df_Dr = df[df['SKILLNAME'].str.contains(
        'dr|doctor', case=False, na=False)]
    df_Dr['CONTACTID'] = df_Dr['CONTACTID'].astype(str)
    df_ids = df_Dr[['CONTACTID']]
    return df_ids
