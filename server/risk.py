from db import get_census_data_from_cache

def calculate_risk(zip_code, num_competitors, competitors_with_ratings, alerts):
    census_data = get_census_data_from_cache(zip_code)

    if census_data is None:
        return {'risk_score': None, 'error': 'No census data found'}
        
    median_income = float(census_data['Median Household Income'])
    employment_rate = float(census_data['Employment Rate']) 
    education_rate = float(census_data["Bachelor's Degree Rate"])
    home_ownership = float(census_data['Home Ownership Rate'])
    vacancy_rate = float(census_data['Vacancy Rate'])
    
    income_score = min(median_income / 100000, 1.0)  
    employment_score = employment_rate
    education_score = education_rate
    ownership_score = home_ownership
    vacancy_score = 1 - vacancy_rate
    competitor_score = min(num_competitors / 10, 1.0)
    competitor_rating_score = normalize_ratings(competitors_with_ratings)
    
    weights = {
        'income': 0.25,
        'employment': 0.15, 
        'education': 0.15,
        'ownership': 0.15,
        'vacancy': 0.1,
        'competitors': 0.1,
        'competitor_ratings': 0.1
    }
    
    risk_score = (
        weights['income'] * income_score +
        weights['employment'] * employment_score +
        weights['education'] * education_score + 
        weights['ownership'] * ownership_score +
        weights['vacancy'] * vacancy_score +
        weights['competitors'] * (1 - competitor_score) +
        weights['competitor_ratings'] * (1 - competitor_rating_score)
    )
    
    risk_score = round(risk_score * 100)
    
    # return {
    #     'risk_score': risk_score,
    #     'components': {
    #         'income_score': round(income_score * 100),
    #         'employment_score': round(employment_score * 100),
    #         'education_score': round(education_score * 100),
    #         'ownership_score': round(ownership_score * 100),
    #         'vacancy_score': round(vacancy_score * 100),
    #         'competitor_score': round((1 - competitor_score) * 100),
    #         'competitor_rating_score': round((1 - competitor_rating_score) * 100)
    #     }
    # }

    demographic_risk = calculate_demographic_risk(zip_code)
    competitor_risk = calculate_competitor_risk(num_competitors, competitors_with_ratings)
    environment_risk = calculate_environment_risk(alerts)
    regulatory_risk = calculate_regulatory_risk(alerts)
    crime_risk = calculate_crime_risk(zip_code)
    market_risk = calculate_market_risk(zip_code)


    return {
        'demographic_risk': demographic_risk,
        'competitor_risk': competitor_risk,
        'environment_risk': environment_risk,
        'regulatory_risk': regulatory_risk,
        'crime_risk': crime_risk,
        'market_risk': market_risk
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
    
    travel_time = min(travel_time / 100, 1.0)
    education_rate = min(education_rate / 100, 1.0) 
    income = min(income / 100000, 1.0) * 100
    employment_rate = min(employment_rate / 100, 1.0) * 100
    home_ownership = min(home_ownership / 100, 1.0) * 100
    vacancy = min(vacancy / 100, 1.0) * 100
    median_household_value = min(median_household_value / 1000000, 1.0) * 100

    weights = {
        'travel_time': 0.15,
        'education_rate': 0.15,
        'income': 0.15,
        'employment_rate': 0.15,
        'home_ownership': 0.15,
        'vacancy': 0.15,
        'median_household_value': 0.10
    }

    risk_score = (
        weights['travel_time'] * travel_time +
        weights['education_rate'] * education_rate +
        weights['income'] * income +
        weights['employment_rate'] * employment_rate +
        weights['home_ownership'] * home_ownership +
        weights['vacancy'] * vacancy +
        weights['median_household_value'] * median_household_value
    )   

    risk_score = round(risk_score * 100)

    return {
        'risk_score': risk_score,
        'components': {
            'travel_time': round(travel_time),
            'education_rate': round(education_rate * 100),
            'income': round(income),
            'employment_rate': round(employment_rate * 100),
            'home_ownership': round(home_ownership * 100),
            'vacancy': round(vacancy * 100),
            'median_household_value': round(median_household_value)
        }
    }

def calculate_competitor_risk(num_competitors, competitors_with_ratings):
    return {
        'risk_score': 0.0,
        'components': {}
    }

def calculate_environment_risk(alerts):
    return {
        'risk_score': 0.0,
        'components': {}
    }

def calculate_regulatory_risk(alerts):
    return {
        'risk_score': 0.0,
        'components': {}
    }

def calculate_crime_risk(zip_code):
    return {
        'risk_score': 0.0,
        'components': {}
    }

def calculate_market_risk(zip_code):
    return {
        'risk_score': 0.0,
        'components': {}
    }  