import pandas as pd

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath, header=8)
    df = df.dropna(subset=['YRKESOMRÅDE'])
    df_long = df.melt(id_vars=['YRKESOMRÅDE'], value_vars=df.columns[3:], var_name='Månad', value_name='Antal annonser')
    df_long['Månad'] = pd.to_datetime(df_long['Månad'], format='%Y-%m')
    df_long['Antal annonser'] = pd.to_numeric(df_long['Antal annonser'], errors='coerce')
    df_long['YRKESOMRÅDE'] = df_long['YRKESOMRÅDE'].str.lower()
    return df_long
