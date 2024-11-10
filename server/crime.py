import pandas as pd
from pathlib import Path

def load_crime_data():
    current_dir = Path(__file__).parent
    data_path = current_dir / 'data' / 'crime.csv'
    
    return pd.read_csv(data_path)

def get_crime_data(county, state):
    crime_df = load_crime_data()
    filtered_df = crime_df[crime_df['county_name'] == f"{county}, {state}"]

    print(filtered_df.describe())

    if filtered_df.empty:
        return 0
    return filtered_df['crime_rate_per_100000'].values[0]
