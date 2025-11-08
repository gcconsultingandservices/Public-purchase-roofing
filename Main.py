from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import requests
import json

# options = Options()

# driver = webdriver.Chrome(options=options)

# VARIABLES
username = "manuel.madeira"
password = "AlakaiRoofing123"
base_url = "https://www.publicpurchase.com"

# search keywords
keyword = "roofing"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_experimental_option("detach", True)  # Keeps browser open

# chrome_options.add_argument("--headless")  # Uncomment to run without opening a browser window

# Set up ChromeDriver service
service = Service(ChromeDriverManager().install())

# Create the driver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the login page
driver.get("https://www.publicpurchase.com/gems/login/login")

# LOGGING IN
# insert username
driver.find_element(By.NAME, "uname").send_keys(username)

# insert password
driver.find_element(By.NAME, "pwd").send_keys(password)

# click login button
driver.find_element(By.CSS_SELECTOR, "input[type='button']").click()

# WAIT until login completes (e.g. until page URL or element changes)
try:
    WebDriverWait(driver, 15).until(
        EC.url_contains("https://www.publicpurchase.com/gems/vendor/home")
    )
    print("✅ Logged in successfully!")
except:
    print("⚠️ Login might have failed or taken too long.")


# NAVIGATE to the search page
driver.get("https://www.publicpurchase.com/gems/browse/search")
print("➡️ Navigated to search page.")

# Searching using a keyword.
driver.find_element(By.NAME, "bidTitle").send_keys(keyword)

# clicking the search button
# driver.find_element(By.CSS_SELECTOR, "input[type='button']").click()
driver.find_element(By.ID, "searchButton").click()


# WAIT until search results appear
try:
    results_table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "table.tabHome tbody tr.listA, table.tabHome tbody tr.listB")
        )
    )
    print("✅ Search successful: results table loaded!")
except:
    print("⚠️ Search results did not load or took too long.")
    


# Scrape table data and store it in the results array
results = []
rows = driver.find_elements(By.CSS_SELECTOR, "table.tabHome tbody tr.listA, table.tabHome tbody tr.listB")

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    
    # Extract link from <a> in the Title column
    title_element = cells[3].find_element(By.TAG_NAME, "a")
    title_text = title_element.text
    link = base_url + title_element.get_attribute("href") if title_element.get_attribute("href").startswith("/") else title_element.get_attribute("href")
    
    row_data = {
        "Bid Id": cells[0].text,
        "Agency": cells[1].text,
        "State": cells[2].text,
        "Title": title_text,
        "Type": cells[4].text,
        "Link": link
    }
    results.append(row_data)

# Example: print results array


# print("RESULTS: ", results)

# MAKING A POST REQUEST TO THE N8N URL WITH THE RESULTS
# The URL to post to
# TEST URL
# url = "https://n8n.srv988364.hstgr.cloud/webhook-test/90bc76af-ac70-4bde-89a0-43b0c27bdf42"

# PRODUCTION URL
url = "https://n8n.srv988364.hstgr.cloud/webhook/90bc76af-ac70-4bde-89a0-43b0c27bdf42"

# Make the POST request
response = requests.post(url, json=results)

# Print response for debugging
print("Status code:", response.status_code)
print("Response text:", response.text)