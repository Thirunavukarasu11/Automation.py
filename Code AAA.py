import itertools
import time
import re
import pandas as pd
import undetected_chromedriver as uc
from packaging.version import Version as LooseVersion 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Generate 3-letter combinations from A, B, C
prefixes = [''.join(p) for p in itertools.product('ABC', repeat=3)]

# Setup undetected Chrome
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# Store all results
data = []

# Loop through each prefix
for prefix in prefixes:
    try:
        print(f"Searching: {prefix}")
        driver.get("https://businesssearch.ohiosos.gov/")

        time.sleep(3)  # Let the page settle

        # Enter business name prefix
        name_input = wait.until(EC.presence_of_element_located((By.ID, "businessName")))
        name_input.clear()
        name_input.send_keys(prefix)

        # Select 'Active' status
        active_radio = driver.find_element(By.XPATH, "//input[@value='Active']")
        active_radio.click()

        # Click 'Search'
        search_button = driver.find_element(By.XPATH, "//button[text()='SEARCH']")
        search_button.click()

        # Wait for results to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchResult")))

        while True:
            rows = driver.find_elements(By.CLASS_NAME, "searchResult")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    business_name = cols[0].text.strip()
                    entity_number = cols[1].text.strip()
                    type_ = cols[2].text.strip()
                    status = cols[3].text.strip()

                    if re.match(f"^{prefix}", business_name):
                        data.append({
                            "Prefix": prefix,
                            "Business Name": business_name,
                            "Entity Number": entity_number,
                            "Type": type_,
                            "Status": status
                        })

            # Handle pagination
            try:
                next_button = driver.find_element(By.LINK_TEXT, "Next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(2)
            except:
                break

        time.sleep(3)  # Slow down between prefixes to avoid bot block

    except Exception as e:
        print(f"Error on {prefix}: {e}")
        time.sleep(5)
        continue

# Done scraping
driver.quit()

# Save results to Excel
df = pd.DataFrame(data)
df.to_excel("ohio_active_businesses_ABC.xlsx", index=False)
print(f"\n✅ Scraping complete. {len(df)} records saved to 'ohio_active_businesses_ABC.xlsx'")
