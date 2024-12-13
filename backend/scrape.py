# scrape.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, ElementNotInteractableException

def scrape_data():
    print("Performing web scraping...")
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment this to run headless (without UI)

    # Set up Chrome driver using the existing chromedriver
    chrome_driver_path = "/usr/local/bin/chromedriver"  # Replace with actual path to chromedriver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

    # URL of the webpage
    url = "https://www.ccilindia.com/web/ccil/rbi-nds-om1"
    driver.get(url)

    # Wait until the table element is visible
    try:
        # Find the current page by checking for the "current" class
        current_page = None

        # Wait for the table element to be rendered
        table = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//table[contains(@id, "ndsomEntityTable")]'))
        )
        if table is not None:
            print("Table found!")
        else:
            return []

        data = []

        while True:
            # Locate the pagination container and find all <a> tags
            pagination_links = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "paginate_button") and contains(@class, "current")]'))
            )
            if pagination_links:
                for link in pagination_links:
                    if "current" in link.get_attribute("class"):
                        current_page = link.text  # Extract the text (which is the page number)
                        break
            else:
                print("Unable to find pagination link")

            # Scrape the current page data
            rows = table.find_elements(By.TAG_NAME, "tr")

            # Skip the header row (if any)
            for row in rows[1:-1]:  # Start from index 1 to skip header
                cols = row.find_elements(By.TAG_NAME, "td")

                # Exclude the 2nd last and 3rd last columns
                if len(cols) > 2:  # Ensure there are enough columns to avoid index errors
                    data_row = []  # Initialize a new list for the row
                    for i in range(len(cols)):
                        # Skip the second-last and third-last columns
                        if i == len(cols) - 2 or i == len(cols) - 3:
                            continue

                        # If it's the last column, get innerHTML instead of text as the web we are scraping from does not display the last three columns
                        if i == len(cols) - 1:
                            last_column_html = cols[i].get_attribute('innerHTML').strip()
                            data_row.append(last_column_html)
                        else:
                            # For other columns, use .text.strip()
                            col_text = cols[i].text.strip()
                            data_row.append(col_text)

                data.append(data_row)

            # Try to find the "Next" button and check if it's enabled
            try:
                # Locate the "Next" button using class name
                next_button = driver.find_element(By.ID, "ndsomEntityTable_next")

                # Check if the "Next" button is disabled (no "next" class or disabled attribute)
                if "disabled" in next_button.get_attribute("class"):
                    print("Last page reached.")
                    break  # Exit if the next button is disabled (last page)
                else:
                    print(f"Going to next page, page {current_page}...")
                    # Use JavaScript to click the button if it's not clickable directly
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(2)  # Wait for the table to update

                    # Re-locate the table after the page has been refreshed
                    print("Waiting for the table to refresh...")
                    table = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//table[contains(@id, "ndsomEntityTable")]'))
                    )
                    if table is not None:
                        print("Table re-located successfully!")
                    else:
                        return []

            except Exception as e:
                print("Error while navigating to the next page:", e)
                break  # Exit if we hit an error with pagination

        # Print total scraped data
        print(f"Scraped data: {len(data)} rows")
        for row in data:
            print(row)  # Print each row

        print("Web scraping completed.")
        return data  # Return the scraped data

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        driver.quit()
