from census import Census
import os
import pandas as pd
from us import states
import json
c = Census(os.getenv("CENSUS_API_KEY"))

RISK_VARIABLES = {
    'B01003_001E': 'Total Population',
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
    
    variables = ['NAME'] + list(RISK_VARIABLES.keys())
    
    data = c.acs5.state_zipcode(
        variables,
        state_fips,
        zip_code
    )

    df = pd.DataFrame(data)
    if df.empty:
        return None
        
    df.rename(columns=RISK_VARIABLES, inplace=True)

    df['Bachelor\'s Degree Rate'] = (df["Bachelor's Degree"] / df['Total Population']).astype(float)
    df['Employment Rate'] = (df['Employed'] / df['Labor Force']).astype(float)
    df['Home Ownership Rate'] = (df['Owner Occupied Housing Units'] / df['Total Housing Units']).astype(float)
    df['Vacancy Rate'] = (df['Vacant Housing Units'] / df['Total Housing Units']).astype(float)
    
    for col in ['Median Household Income', 'Median House Value']:
        df[col] = df[col].astype(float)

    final_columns = [
        'zip code tabulation area', 'Bachelor\'s Degree Rate',
        'Median Household Income', 'Employment Rate',
        'Home Ownership Rate', 'Vacancy Rate', 'Median House Value'
    ]

    result = df[final_columns].to_dict('records')[0]
    return {k: float(v) if isinstance(v, (pd.np.integer, pd.np.floating)) else v 
            for k, v in result.items()}

def get_census_data_by_county(state_fips, county_fips):
    fields = {
        'B01003_001E': 'population',
        'B25001_001E': 'housing_units',
        'B19013_001E': 'median_household_income',
        'B25077_001E': 'median_home_value',
        'B23025_004E': 'employment_rate',
        'B08303_001E': 'commute_time',
        'B01001_001E': 'land_area',
        'B25002_001E': 'green_space',
        'B08301_010E': 'public_transport_access',
    }

    data = c.acs5.state_county(list(fields.keys()), state_fips, county_fips)

    if not data:
        return {
            'Population': 'N/A',
            'Housing Units': 'N/A',
            'Median Household Income': 'N/A',
            'Median Home Value': 'N/A',
            'Employment Rate': 'N/A',
            'Average Commute Time (minutes)': 'N/A',
            'Land Area (approx.)': 'N/A',
            'Green Space (approx. vacant land)': 'N/A',
            'Public Transport Access': 'N/A'
        }

    results = {
        'Population': data[0].get(fields['population'], 'N/A'),
        'Housing Units': data[0].get(fields['housing_units'], 'N/A'),
        'Median Household Income': data[0].get(fields['median_household_income'], 'N/A'),
        'Median Home Value': data[0].get(fields['median_home_value'], 'N/A'),
        'Employment Rate': data[0].get(fields['employment_rate'], 'N/A'),
        'Average Commute Time (minutes)': data[0].get(fields['commute_time'], 'N/A'),
        'Land Area (approx.)': data[0].get(fields['land_area'], 'N/A'),
        'Green Space (approx. vacant land)': data[0].get(fields['green_space'], 'N/A'),
        'Public Transport Access': data[0].get(fields['public_transport_access'], 'N/A')
    }

    return results

STATE_MAPPING = {
    'AL': states.AL.fips,
    'AK': states.AK.fips,
    'AZ': states.AZ.fips,
    'AR': states.AR.fips,
    'CA': states.CA.fips,
    'CO': states.CO.fips,
    'CT': states.CT.fips,
    'DE': states.DE.fips,
    'FL': states.FL.fips,
    'GA': states.GA.fips,
    'HI': states.HI.fips,
    'ID': states.ID.fips,
    'IL': states.IL.fips,
    'IN': states.IN.fips,
    'IA': states.IA.fips,
    'KS': states.KS.fips,
    'KY': states.KY.fips,
    'LA': states.LA.fips,
    'ME': states.ME.fips,
    'MD': states.MD.fips,
    'MA': states.MA.fips,
    'MI': states.MI.fips,
    'MN': states.MN.fips,
    'MS': states.MS.fips,
    'MO': states.MO.fips,
    'MT': states.MT.fips,
    'NE': states.NE.fips,
    'NV': states.NV.fips,
    'NH': states.NH.fips,
    'NJ': states.NJ.fips,
    'NM': states.NM.fips,
    'NY': states.NY.fips,
    'NC': states.NC.fips,
    'ND': states.ND.fips,
    'OH': states.OH.fips,
    'OK': states.OK.fips,
    'OR': states.OR.fips,
    'PA': states.PA.fips,
    'RI': states.RI.fips,
    'SC': states.SC.fips,
    'SD': states.SD.fips,
    'TN': states.TN.fips,
    'TX': states.TX.fips,
    'UT': states.UT.fips,
    'VT': states.VT.fips,
    'VA': states.VA.fips,
    'WA': states.WA.fips,
    'WV': states.WV.fips,
    'WI': states.WI.fips,
    'WY': states.WY.fips,
}

def get_county_fips(match):
    with open('server/data/fips.json', 'r') as f:
        fips_data = json.load(f)
    
    for entry in fips_data:
        if match in entry[0]:
            return entry[2]
        
    return None