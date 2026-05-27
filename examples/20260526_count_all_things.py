"""
Quick start:
  This example provides a count of links, images, headings, list items, and meta tags on a page.

  1. Go to https://siterows.com and create your FREE account, which will give you the API token.
  2. Clone this repo and add the API token to a `.env` file (see `.env.example`).
  3. In the repo root folder run: pip install -r requirements.txt
  4. In the repo root folder run: python examples/20260526_count_all_things.py
"""

import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

payload = {
    "pages": [
        {"url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview"},
    ],
    "sql": """
        SELECT 'Number of links' AS description, count(*) AS count FROM @a
        UNION ALL
        SELECT 'Number of images' AS description, count(*) AS count FROM @img
        UNION ALL
        SELECT 'Number of headings' AS description, count(*) AS count FROM @headings
        UNION ALL
        SELECT 'Number of list items' AS description, count(*) AS count FROM @li
        UNION ALL
        SELECT 'Number of meta tags' AS description, count(*) AS count FROM @meta
        ORDER BY description;
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
