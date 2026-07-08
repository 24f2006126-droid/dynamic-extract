import json
import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI(
    api_key="YOUR_NEW_API_KEY_HERE"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestBody(BaseModel):
    text: str
    schema: dict


@app.post("/dynamic-extract")
def dynamic_extract(req: RequestBody):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
Extract information from this text.

Return ONLY JSON.

Schema:
{json.dumps(req.schema)}

Text:
{req.text}
"""
                }
            ],
            temperature=0
        )

        result = response.choices[0].message.content

        print("AI OUTPUT:")
        print(result)

        return json.loads(result)

    except Exception as e:
        print("ERROR DETAILS:")
        print(repr(e))
        return {"error": str(e)}