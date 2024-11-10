import pandas as pd
from pathlib import Path

def load_crime_data():
    current_dir = Path(__file__).parent
    data_path = current_dir / 'data' / 'crime.csv'
    
    return pd.read_csv(data_path)

def get_crime_data(county, state):
    crime_df = load_crime_data()
    filtered_df = crime_df[crime_df['county_name'] == f"{county} County, {state}"]
    
    if filtered_df.empty:
        return 0
        
    crime_rate = float(filtered_df['crime_rate_per_100000'].values[0])
    ranking = int(filtered_df['index'].values[0])
    arrest_count = int(filtered_df['CPOPARST'].values[0])
    crime_count = int(filtered_df['CPOPCRIM'].values[0])
    
    return {
        'crime_rate': crime_rate,
        'ranking': ranking,
        'arrest_count': arrest_count,
        'crime_count': crime_count
    }