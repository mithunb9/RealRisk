from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def execute(prompt, model="gpt-4o-mini", response_format=None, history=None, stream=False):
    messages = []
    
    if history:
        messages.extend([
            {"role": msg["role"], "content": msg["content"]} 
            for msg in history
        ])
    
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