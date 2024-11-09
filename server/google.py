import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
URL = "https://google.serper.dev/search"

HEADERS = {
  'X-API-KEY': os.getenv("SERPER_API_KEY"),
  'Content-Type': 'application/json'
}

def search(query, country_code="us", location="United States", num=10):
    payload = json.dumps({
        "q": query,
        "gl": country_code,
        "location": location,
        "num": num
    })
    
    response = requests.request("POST", URL, headers=HEADERS, data=payload)

    return response.text