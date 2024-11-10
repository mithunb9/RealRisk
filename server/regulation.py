from pydantic import BaseModel
from ai import execute
from typing import List
from google import search

class Query(BaseModel):
    query: str

class Score(BaseModel):
    score: int

def get_regulatory_score(city: str, county: str) -> int:
    response = execute(
        f"Given the following city and county: {city}, {county}. Provide as many google search queries as you need that will help you get the necessary information to find the different regulatory documents, zoning ordinances, and other relevant documents and information.",
        response_format=Query
    )

    search_results = search(response.query)

    next_response = execute(
        f"Given the following search results, provide a list of the most relevant documents and information to the query: {search_results} What are some regulatory documents, zoning ordinances, and other relevant documents and information?",
        model="gpt-4o",
    )

    score_response = execute(
        f"Given the following two responses, score them on a scale of 1 to 10 in terms of the regulatory documents, zoning ordinances, and other relevant documents and information in terms of difficulty to navigate as a builder: {next_response.choices[0].message.content} {search_results}",
        model="gpt-4o",
        response_format=Score
    )

    return score_response.score, next_response.choices[0].message.content
