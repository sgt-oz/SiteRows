"""
Quick start:
  This example uses selenium to login to a site and then pass the HTML to the Scrape endpoint.

  1. Go to https://siterows.com and create your FREE account, which will give you the API token.
  2. Clone this repo and add the API token to a `.env` file (see `.env.example`).
  3. In the repo root folder run: pip install -r requirements.txt
  4. In the repo root folder run: python examples/20260528_pass_html_to_scrape.py
"""

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)

LOADER = "[data-testid='toggles-loader']"
MIN_APP_NODES = 30


def _dashboard_ready(driver: WebDriver) -> bool:
    if "sign-in" in (driver.current_url or "").lower():
        return False
    for el in driver.find_elements(By.CSS_SELECTOR, LOADER):
        if el.is_displayed():
            return False
    return len(driver.find_elements(By.CSS_SELECTOR, "#app *")) >= MIN_APP_NODES


def fetch_logged_in_html() -> str:
    """Log in via Selenium and return the rendered page HTML."""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)
    try:
        driver.get((os.getenv("URL") or "").strip())
        userid_textbox = wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_textbox = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        #type in the username and password
        userid_textbox.clear()
        userid_textbox.send_keys((os.getenv("SITE_USERNAME") or "").strip())
        password_textbox.clear()
        password_textbox.send_keys((os.getenv("SITE_PASSWORD") or "").strip())
        
        #click the login button
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        WebDriverWait(driver, 60).until(_dashboard_ready)
        time.sleep(2)

        #return the HTML
        return driver.page_source
    finally:
        driver.quit()


html = fetch_logged_in_html()

payload = {
    "pages": [
        {"html": html},
    ],
    "sql": """
        select URL, TAG, href, parent, text from @a limit 5
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
