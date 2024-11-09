from db import get_census_data_from_cache
from weather import get_air_quality_data
import numpy as np

def calculate_risk(zip_code, location, num_competitors, competitors_with_ratings, alerts):
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
        
    environment_risk = calculate_environment_risk(alerts['Event Type Count'] if alerts else None)
    regulatory_risk = calculate_regulatory_risk(alerts)
    crime_risk = calculate_crime_risk(zip_code)
    market_risk = calculate_market_risk(zip_code)

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
        'market_risk': market_risk,
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

    travel_time = float(census_data['Mean Travel Time to Work'])
    education_rate = float(census_data["Bachelor's Degree Rate"])
    income = float(census_data['Median Household Income'])
    employment_rate = float(census_data['Employment Rate'])
    home_ownership = float(census_data['Home Ownership Rate'])
    vacancy = float(census_data['Vacancy Rate'])
    median_household_value = float(census_data['Median House Value'])

    travel_time = np.log(travel_time + 1)
    education_rate = np.log(education_rate + 1)
    income = np.log(income + 1)
    employment_rate = np.log(employment_rate + 1)
    home_ownership = np.log(home_ownership + 1)
    vacancy = np.log(vacancy + 1)
    median_household_value = np.log(median_household_value + 1)

    print(travel_time, education_rate, income, employment_rate, home_ownership, vacancy, median_household_value)

    weights = {
    'travel_time': 0.10,
    'education_rate': 0.20,
    'income': 0.25,
    'employment_rate': 0.15,
    'home_ownership': 0.10,
    'vacancy': 0.10,
    'median_household_value': 0.10
    }


    risk_score = sum(weights[key] * value for key, value in zip(weights.keys(), 
                    [travel_time, education_rate, income, employment_rate, 
                     home_ownership, vacancy, median_household_value]))
    
    min_score = 0
    max_score = 15 
    normalized_score = 100 * (risk_score - min_score) / (max_score - min_score)
    
    return {
        'risk_score': round(max(0, min(normalized_score, 100))),
        'components': {}
    }

def calculate_competitor_risk(num_competitors, competitors_with_ratings):
    return {
        'risk_score': 100.0,
        'components': {}
    }

def calculate_environment_risk(event_counts):
    if not event_counts:
        return {
            'risk_score': 0,
            'components': {}
        }
        
    weights = {
        'tornado': 0.25,
        'flood': 0.20,
        'severe thunderstorm': 0.15,
        'winter storm': 0.15,
        'wind': 0.1,
        'air quality': 0.1,
        'other': 0.05
    }
    
    components = {
        'tornado': 0,
        'flood': 0,
        'severe thunderstorm': 0,
        'winter storm': 0,
        'wind': 0,
        'air quality': 0,
        'other': 0
    }
    
    for event_type, count in event_counts.items():
        event_type = event_type.lower()
        
        # Map severity based on count
        if count >= 3:
            severity = 'extreme'
        elif count == 2:
            severity = 'severe'
        elif count == 1:
            severity = 'moderate'
        else:
            severity = 'minor'
            
        severity_scores = {
            'extreme': 100,
            'severe': 75,
            'moderate': 50,
            'minor': 25
        }
        
        score = severity_scores[severity]
        
        # Add to appropriate component
        matched = False
        for component in components:
            if component in event_type:
                components[component] = max(components[component], score)
                matched = True
                break
                
        if not matched:
            components['other'] = max(components['other'], score)
    
    # Calculate weighted risk score
    risk_score = sum(
        components[component] * weights[component]
        for component in weights.keys()
    )
    
    return {
        'risk_score': round(risk_score),
        'components': components
    }

def calculate_regulatory_risk(alerts):
    return {
        'risk_score': 100.0,
        'components': {}
    }

def calculate_crime_risk(zip_code):
    return {
        'risk_score': 100.0,
        'components': {}
    }

def calculate_market_risk(zip_code):
    return {
        'risk_score': 100.0,
        'components': {}
    }  

print(calculate_demographic_risk(75024))