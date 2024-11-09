from db import get_census_data_from_cache

def run_agent(address):
    zip_code = address['ZipCode']
    census_data = get_census_data_from_cache(zip_code)
    
    return census_data
