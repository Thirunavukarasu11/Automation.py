import itertools
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chars = ['a', 'b', 'c']
combinations = [''.join(p) for p in itertools.product(chars, repeat=3)]
states = ['WA', 'CA', 'NY']  # example states

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

all_results = []

def search_and_scrape(state, keyword):
    url = "https://ccfs.sos.wa.gov/#/"  # Replace with your actual URL
    driver.get(url)

    try:
        # Wait and find input fields — update selectors based on actual site!
        search_input = wait.until(EC.presence_of_element_located((By.ID, "searchInputId")))  # Change this
        state_select = driver.find_element(By.ID, "stateSelectId")  # Change this

        search_input.clear()
        search_input.send_keys(keyword)
        state_select.send_keys(state)

        submit_button = driver.find_element(By.ID, "submitBtnId")  # Change this
        submit_button.click()

        # Wait for results table or some unique element that shows results are loaded
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.results tbody tr")))

        rows = driver.find_elements(By.CSS_SELECTOR, "table.results tbody tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")

            # Suppose email is in 3rd column, or find mailto links inside the row:
            email = ""
            try:
                mail_link = row.find_element(By.CSS_SELECTOR, "a[href^='mailto:']")
                email = mail_link.get_attribute('href').replace("mailto:", "")
            except:
                # If no mailto link, try alternative ways here
                email = "N/A"

            record = {
                "State": state,
                "Keyword": keyword,
                "Column1": cols[0].text,
                "Column2": cols[1].text,
                "Email": email,
                # Add more fields as needed
            }
            all_results.append(record)

    except Exception as e:
        print(f"Error with state={state} keyword={keyword}: {e}")

for state in states:
    for kw in combinations:
        print(f"Searching state={state}, keyword={kw}")
        search_and_scrape(state, kw)

driver.quit()

df = pd.DataFrame(all_results)
df.to_excel("results_with_emails.xlsx", index=False)
print("Scraping complete. Check results_with_emails.xlsx")
