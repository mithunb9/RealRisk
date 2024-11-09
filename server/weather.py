from typing import Dict
from collections import Counter
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(state: str):
    state_map = {
        'alabama': 'AL', 'alaska': 'AK', 'arizona': 'AZ', 'arkansas': 'AR', 'california': 'CA',
        'colorado': 'CO', 'connecticut': 'CT', 'delaware': 'DE', 'florida': 'FL', 'georgia': 'GA',
        'hawaii': 'HI', 'idaho': 'ID', 'illinois': 'IL', 'indiana': 'IN', 'iowa': 'IA',
        'kansas': 'KS', 'kentucky': 'KY', 'louisiana': 'LA', 'maine': 'ME', 'maryland': 'MD',
        'massachusetts': 'MA', 'michigan': 'MI', 'minnesota': 'MN', 'mississippi': 'MS', 'missouri': 'MO',
        'montana': 'MT', 'nebraska': 'NE', 'nevada': 'NV', 'new hampshire': 'NH', 'new jersey': 'NJ',
        'new mexico': 'NM', 'new york': 'NY', 'north carolina': 'NC', 'north dakota': 'ND', 'ohio': 'OH',
        'oklahoma': 'OK', 'oregon': 'OR', 'pennsylvania': 'PA', 'rhode island': 'RI', 'south carolina': 'SC',
        'south dakota': 'SD', 'tennessee': 'TN', 'texas': 'TX', 'utah': 'UT', 'vermont': 'VT',
        'virginia': 'VA', 'washington': 'WA', 'west virginia': 'WV', 'wisconsin': 'WI', 'wyoming': 'WY'
    }
    
    if len(state) != 2:
        state = state_map.get(state.lower(), state)

    response = requests.get(f'https://api.weather.gov/alerts/?area={state}')
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch weather data: {response.status_code}")

def get_event_summary_for_county(data: dict, county_name: str) -> Dict[str, dict]:
    severity_counter = Counter()
    certainty_counter = Counter()
    urgency_counter = Counter()
    event_counter = Counter()
    
    county_name_lower = county_name.lower()

    for feature in data.get("features", []):
        properties = feature.get("properties", {})
        if 'areaDesc' in properties and county_name_lower in properties['areaDesc'].lower():
            severity_counter[properties.get('severity', 'Unknown')] += 1
            certainty_counter[properties.get('certainty', 'Unknown')] += 1
            urgency_counter[properties.get('urgency', 'Unknown')] += 1
            event_counter[properties.get('event', 'Unknown')] += 1

    summary = {
        "Total Events": sum(severity_counter.values()),
        "Severity Count": dict(severity_counter),
        "Certainty Count": dict(certainty_counter),
        "Urgency Count": dict(urgency_counter),
        "Event Type Count": dict(event_counter)
    }

    return summary

def get_air_quality_data(latitude: float, longitude: float):
    response = requests.get(f'https://api.waqi.info/feed/geo:{latitude};{longitude}/?token={os.getenv("AIR_API_KEY")}')
    if response.status_code == 200:
        return response.json()
    else:
        print(response.json())
        raise Exception(f"Failed to fetch air quality data: {response.status_code}")

def get_alert_summary(state: str, county: str):
    data = get_weather_data(state)
    return get_event_summary_for_county(data, county)

