# SiteRows API examples

Have you ever wondered: *Why can't I query a web page like I can query a DB?* That question led me to start building [SiteRows](https://siterows.com).

The idea is to expose web content as queryable datasets, so you can do things like:

```
URL:    https://wikipedia.org
SQL:    SELECT * FROM @a WHERE text LIKE '%English%'
RESULT: A list of all links whose text contains "English"
```

There is a front-end with a SQL-like object explorer, and there is an API to set up automation. This repo provides examples of how you can start using the SiteRows API.

Please feel free to visit [SiteRows](https://siterows.com) and let me know what you think.

## Quick start

1. Go to [SiteRows](https://siterows.com) and create you FREE account, which will give you an API token
2. Clone this repo and add the API token to an .env file
3. In root folder run: pip install -r requirements.txt
4. In root folder run: python examples/20260522_first_api_example.py

The example calls the `POST /Scrape` endpoint and prints the JSON response.
