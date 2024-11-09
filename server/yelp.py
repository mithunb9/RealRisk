import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YELP_API_KEY")
HEADERS = {'Authorization': f'Bearer {API_KEY}'}

def get_builder_ratings(builder_name, location):
    url = 'https://api.yelp.com/v3/businesses/search'
    params = {
        'term': builder_name,
        'location': location,
        'categories': 'contractors',
        'limit': 1
    }

    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        businesses = response.json().get('businesses', [])
        
        if businesses:
            business = businesses[0]
            return {
                'name': business['name'],
                'rating': business['rating'],
                'review_count': business['review_count']
            }
        return None
    else:
        print(f"Error: {response.status_code}")
        return None
