import json
import time
import undetected_chromedriver as uc

# Load cookies from file
with open("cookies.json", "r") as f:
    cookies = json.load(f)

# Start undetected Chrome
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

# Open the page
driver.get("https://businesssearch.ohiosos.gov/")
time.sleep(5)

# Add cookies
for cookie in cookies:
    if 'sameSite' in cookie:
        del cookie['sameSite']  # Avoid potential issues
    driver.add_cookie(cookie)

# Reload the page with cookies active
driver.get("https://businesssearch.ohiosos.gov/")
