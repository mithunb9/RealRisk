from census import Census
import os
import pandas as pd
from us import states

c = Census(os.getenv("CENSUS_API_KEY"))

VARIABLES = {
    'B01003_001E': 'Total Population',
    'B08012_001E': 'Mean Travel Time to Work',
    'B15003_022E': "Bachelor's Degree",
    'B19013_001E': 'Median Household Income',
    'B23025_002E': 'Labor Force',
    'B23025_004E': 'Employed',
    'B25003_001E': 'Total Housing Units',
    'B25003_002E': 'Owner Occupied Housing Units',
    'B25002_003E': 'Vacant Housing Units',
    'B25077_001E': 'Median House Value',
}

def get_census_data(zip_code):
    state_fips = str(zip_code)[:2]
    
    variables = ['NAME'] + list(VARIABLES.keys())
    
    data = c.acs5.state_zipcode(
        variables,
        state_fips,
        zip_code
    )

    df = pd.DataFrame(data)
    if df.empty:
        return None
        
    df.rename(columns=VARIABLES, inplace=True)

    df['Bachelor\'s Degree Rate'] = df["Bachelor's Degree"] / df['Total Population']
    df['Employment Rate'] = df['Employed'] / df['Labor Force']
    df['Home Ownership Rate'] = df['Owner Occupied Housing Units'] / df['Total Housing Units']
    df['Vacancy Rate'] = df['Vacant Housing Units'] / df['Total Housing Units']

    final_columns = [
        'zip code tabulation area', 'Mean Travel Time to Work', 'Bachelor\'s Degree Rate',
        'Median Household Income', 'Employment Rate',
        'Home Ownership Rate', 'Vacancy Rate', 'Median House Value'
    ]

    return df[final_columns].to_dict('records')[0]
