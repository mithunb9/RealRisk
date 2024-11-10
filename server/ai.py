from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List
from google import search
from pydantic import BaseModel
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PointsResponse(BaseModel):
    points: list[str]

def execute(prompt, model="gpt-4o-mini", response_format=None, history=None, stream=False):
    messages = []
    
    if history:
        messages.extend([
            {"role": msg["role"], "content": msg["content"]} 
            for msg in history
        ])
    

    search_pattern = r"/search\s+(.+)"
    search_match = re.search(search_pattern, prompt)
    
    if search_match:
        search_query = search_match.group(1)
        search_results = search(search_query)
        
        prompt = f"{prompt}\n\nSearch results: {search_results}"
    
    messages.append({"role": "user", "content": prompt})

    if response_format is None:
        return client.chat.completions.create(
            model=model,
            messages=messages,
            stream=stream
        )
    else:
        return client.beta.chat.completions.parse(
            model=model,
            messages=messages,
            response_format=response_format,
        ).choices[0].message.parsed
    
def get_points_of_interest(city, county, state):    
    search_query_old = search(f"What are the top 5 existing points of interest in {county}, {state}?")
    search_query_new = search(f"What are the top 5 new points of interest in {county}, {state}?")

    old_data = execute(f"Based on the following search results: {search_query_old}, provide a list of the top 5 existing points of interest in {county}, {state}. Provide only the names of the points of interest, separated by commas.", response_format=PointsResponse)
    new_data = execute(f"Based on the following search results: {search_query_new}, provide a list of the top 5 new points of interest in {county}, {state}. Provide only the names of the points of interest, separated by commas.", response_format=PointsResponse)

    return old_data.points, new_data.points