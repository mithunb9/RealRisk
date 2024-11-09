from typing import Dict
from collections import Counter
import requests

def get_weather_data(state: str):
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

def get_alert_summary(state: str, county: str):
    data = get_weather_data(state)
    return get_event_summary_for_county(data, county)

