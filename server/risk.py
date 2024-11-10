from db import get_census_data_from_cache
from weather import get_air_quality_data, get_alert_summary
from crime import get_crime_data
import numpy as np
from regulation import get_regulatory_score

def percent_difference(a, b):
    return (a - b) / ((a + b) / 2)

def calculate_risk(zip_code, location, num_competitors, competitors_with_ratings, alerts, state_name, county, city):
    if location and 'latitude' in location and 'longitude' in location:
        air_quality = get_air_quality_data(location['latitude'], location['longitude'])
        air_quality = air_quality['data']['aqi']
    else:
        air_quality = None
    
    demographic_risk = calculate_demographic_risk(zip_code)
    competitor_risk = calculate_competitor_risk(num_competitors, competitors_with_ratings)
    
    if air_quality:
        if not alerts:
            alerts = {'Event Type Count': {}}
        alerts['Event Type Count']['air quality'] = air_quality
        
    environment_risk = calculate_environment_risk(alerts)
    regulatory_risk = calculate_regulatory_risk(city, county)
    crime_risk = calculate_crime_risk(county, state_name)

    data = {
        'air_quality': air_quality,
        'alerts': alerts,
        'num_competitors': num_competitors,
        'competitors_with_ratings': competitors_with_ratings
    }

    return {
        'data': data,
        'demographic_risk': demographic_risk,
        'competitor_risk': competitor_risk,
        'environment_risk': environment_risk,
        'regulatory_risk': regulatory_risk,
        'crime_risk': crime_risk,
        'location': location
    }

def normalize_ratings(competitors_with_ratings):
    if not competitors_with_ratings:
        return 0.0
    
    normalized_scores = []
    
    for competitor in competitors_with_ratings:
        rating = competitor.get('rating')
        count = competitor.get('review_count', 0)
        
        if rating is None:
            base_score = 0.5
        else:
            base_score = (float(rating) / 5.0) ** 2
        
        if count > 0:
            confidence = min(count / 100, 1.0) 
            score = base_score * (0.5 + 0.5 * confidence)
        else:
            score = base_score * 0.3
            
        normalized_scores.append(score)
    
    return sum(normalized_scores) / len(normalized_scores)

def calculate_demographic_risk(zip_code):
    census_data = get_census_data_from_cache(zip_code)
    
    if census_data is None:
        return {'risk_score': None, 'error': 'No census data found'}

    education_rate = float(census_data["Bachelor's Degree Rate"])
    income = float(census_data['Median Household Income'])
    employment_rate = float(census_data['Employment Rate'])
    home_ownership = float(census_data['Home Ownership Rate'])
    vacancy = float(census_data['Vacancy Rate'])
    median_household_value = float(census_data['Median House Value'])

    risk_score = (-percent_difference(education_rate, .375) * 100 
                 - percent_difference(income, 37585) * 100 
                 - percent_difference(employment_rate, .5925) * 100 
                 - percent_difference(home_ownership, 0.656) * 100 
                 + percent_difference(vacancy, 0.069) * 100 
                 - percent_difference(median_household_value, 420400) * 100) / 6 + 50

    return {
        'risk_score': int(risk_score),
        'components': {
            'Education Rate': f'{education_rate * 100:.2f}%',
            'Income': f'${income:,.2f}',
            'Employment Rate': f'{employment_rate * 100:.2f}%', 
            'Home Ownership': f'{home_ownership * 100:.2f}%',
            'Vacancy': f'{vacancy * 100:.2f}%',
            'Median Household Value': f'${median_household_value:,.2f}'
        }, 'tooltip': {
            'Education Rate': 'Percentage of population with a Bachelor\'s degree',
            'Income': 'Median household income',
            'Employment Rate': 'Percentage of population employed',
            'Home Ownership': 'Percentage of households that are owner-occupied',
            'Vacancy': 'Percentage of rental units that are vacant',
            'Median Household Value': 'Median value of owner-occupied homes'
        }
    }

def calculate_competitor_risk(num_competitors, competitors_with_ratings):
    normalized_ratings = normalize_ratings(competitors_with_ratings)
    
    if num_competitors == 0:
        return {
            'risk_score': 20,
            'components': {
                'Number of Competitors': num_competitors,
                'Normalized Rating Score': '100%'
            }
        }
    
    normalized_ratings = normalize_ratings(competitors_with_ratings)
    
    return {
        'risk_score': 20,
        'components': {
            'Normalized Rating Score': f'{normalized_ratings * 100:.2f}%',
            'Number of Competitors': num_competitors
        }, 'tooltip': {
            'Normalized Rating Score': 'Normalized rating score based on number of reviews and ratings',
            'Number of Competitors': 'Number of competitors in the local market'
        }
    }
    
def calculate_environment_risk(event_counts):
    if not event_counts:
        return {
            'risk_score': 0,
            'components': {}
        }

    total_events = event_counts.get('Total Events', 0)

    flood_advisory = event_counts['Event Type Count'].get('Flood Advisory', 0)
    tornado_watch = event_counts['Event Type Count'].get('Tornado Watch', 0) 
    flood_watch = event_counts['Event Type Count'].get('Flood Watch', 0)
    air_quality_alerts = event_counts['Event Type Count'].get('air quality', 0)
    other = total_events - (flood_advisory + tornado_watch + flood_watch)

    minor_severity = event_counts['Severity Count'].get('Minor', 0)
    extreme_severity = event_counts['Severity Count'].get('Extreme', 0) 
    severe_severity = event_counts['Severity Count'].get('Severe', 0)

    risk_score = (
        - percent_difference(minor_severity, 0.2) * 100 
        - percent_difference(extreme_severity, 0.1) * 100 
        - percent_difference(severe_severity, 0.1) * 100 
        + percent_difference(flood_advisory, 0.15) * 100 
        + percent_difference(tornado_watch, 0.3) * 100 
        + percent_difference(flood_watch, 0.15) * 100 
        + percent_difference(air_quality_alerts, 0.1) * 100 
        + percent_difference(other, 0.15) * 100
    ) / 8 + 50

    return {
        'risk_score': int(risk_score),
        'components': {
            'Flood Advisory': flood_advisory,
            'Tornado Watch': tornado_watch,
            'Flood Watch': flood_watch,
            'Air Quality Alerts': air_quality_alerts,
            'Other': other
        }, 'tooltip': {
            'Flood Advisory': 'Number of flood advisory events',
            'Tornado Watch': 'Number of tornado watch events',
            'Flood Watch': 'Number of flood watch events',
            'Air Quality Alerts': 'Number of air quality alert events',
            'Other': 'Number of other events'
        }
    }

def calculate_regulatory_risk(city, county):
    regulatory_score, response = get_regulatory_score(city, county)
    
    return {
        'risk_score': regulatory_score,
        'components': {
            'Regulatory Score': regulatory_score,
        }, 'tooltip': {
            'Regulatory Score': 'Score based on the difficulty to navigate regulatory procedures and documents. Generated by GPT-4o. Click for more details.'
        }
    }

def calculate_crime_risk(county, state):
    crime_rate = get_crime_data(county, state)

    return {
        'risk_score': 75,
        'components': {
            'Crime Rate': f'{crime_rate * 100:.2f}%'
        }, 'tooltip': {
            'Crime Rate': 'Crime rate in the county'
        }
    }