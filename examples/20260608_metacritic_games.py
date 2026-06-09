"""
Quick start:
  Scrape Metacritic's best games this year, then fetch each game's metadata
  (title, developer, metascore, release date) in a single request.

  1. Go to https://siterows.com and create your FREE account, which will give you the API token.
  2. Clone this repo and add the API token to a `.env` file (see `.env.example`).
  3. In the repo root folder run: pip install -r requirements.txt
  4. In the repo root folder run: python examples/20260608_metacritic_games.py
"""

import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Scrape the main page and get the list of game URLs
links_response = requests.post(
    "https://siterows.com/Scrape",
    json={
        "pages": [{"url": "https://www.metacritic.com/browse/game/all/all/current-year/"}],
        "sql": """
            SELECT resolvedhref
            FROM @a
            WHERE parent ILIKE '%filter-results%'
              AND href ~ '^/game/[^/]+/$'
            LIMIT 10
        """,
    },
    headers={
        "Authorization": f"Bearer {os.getenv('SITEROWS_TOKEN', 'YOUR_API_KEY')}",
    },
)
links_response.raise_for_status()
game_urls = [row["RESOLVEDHREF"] for row in links_response.json()["rows"]]

# Now scrape the detail pages, passing in the list of game URLs
details_response = requests.post(
    "https://siterows.com/Scrape",
    json={
        "pages": [{"url": url} for url in game_urls],
        "sql": """
            SELECT
                url,
                max(value) FILTER (WHERE field = 'title') AS title,
                string_agg(DISTINCT value, ', ' ORDER BY value)
                    FILTER (WHERE field = 'developer') AS developer,
                max(value) FILTER (WHERE field = 'metascore') AS metascore,
                max(value) FILTER (WHERE field = 'release_date') AS release_date
            FROM (
                SELECT url, 'title' AS field, text AS value
                FROM @headings
                WHERE parent ILIKE '%hero-title%'

                UNION ALL

                SELECT url, 'developer', text
                FROM @a
                WHERE href ~ '^/company/[^/]+/$'

                UNION ALL

                SELECT url, 'metascore', text
                FROM @a
                WHERE parent ILIKE '%siteReviewScore%'
                  AND text ~ '^[0-9]{1,3}$'

                UNION ALL

                SELECT url, 'release_date', text
                FROM @a
                WHERE parent ILIKE '%hero-release-date%'
            ) AS fields
            GROUP BY url
        """,
    },
    headers={
        "Authorization": f"Bearer {os.getenv('SITEROWS_TOKEN', 'YOUR_API_KEY')}",
    },
)
details_response.raise_for_status()

print(json.dumps(details_response.json(), indent=2, ensure_ascii=False))

# by_url = {row["URL"]: row for row in details_response.json()["rows"]}
# games = [
#     {
#         "title": by_url[url]["title"],
#         "developer": by_url[url]["developer"],
#         "metascore": by_url[url]["metascore"],
#         "release_date": by_url[url]["release_date"],
#     }
#     for url in game_urls
#     if url in by_url
# ]
# print(json.dumps(games, indent=2, ensure_ascii=False))
