"""
Quick start:
  This example calls the `POST /Scrape` endpoint and prints the JSON response.

  1. Go to https://siterows.com and create your FREE account, which will give you the API token.
  2. Clone this repo and add the API token to a `.env` file (see `.env.example`).
  3. In the repo root folder run: pip install -r requirements.txt
  4. In the repo root folder run: python examples/20260522_first_api_example.py
"""

import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

payload = {
    "pages": [
        {"url": "https://en.wikipedia.org/wiki/Main_Page"},
    ],
    "sql": """
        SELECT TAG, HREF, PARENT, TEXT
        FROM @a
        WHERE text ILIKE '%English%'
    """,
}

response = requests.post(
    "https://siterows.com/Scrape",
    json=payload,
    headers={
        "Authorization": f"Bearer {os.getenv('SITEROWS_TOKEN', 'YOUR_API_KEY')}",
    },
)

response.raise_for_status()
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
