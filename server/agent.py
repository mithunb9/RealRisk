from risk import calculate_risk
from google import search
from ai import execute
from pydantic import BaseModel
from yelp import get_builder_ratings
from weather import get_alert_summary

class Competitors(BaseModel):
    competitors: list[str]

def run_agent(address, location):
    zip_code = address['zip_code']
    state_name = address['state']
    city_name = address['city']

    """ COMPETITORS """
    competitors_search = search(f"housing builders near {city_name}, {state_name} {zip_code}", zip_code)
    competitors = execute(f"Extract the names of the housing builders from the following text: {competitors_search}", 
                        response_format=Competitors)
    print(competitors.competitors)  

    num_competitors = len(competitors.competitors)

    competitors_with_ratings = [
        get_builder_ratings(builder, f"{state_name}") 
        for builder in competitors.competitors
    ]
    
    competitors_with_ratings = [r for r in competitors_with_ratings if r is not None]

    """ ENVIRONMENT """
    alerts = get_alert_summary(state_name, address['county'])

    return calculate_risk(zip_code, location, num_competitors, competitors_with_ratings, alerts)
