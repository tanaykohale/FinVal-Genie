from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_google_snippets(query, num_results=5):
    # Setup headless browser
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")  # Ensure English results
    driver = webdriver.Chrome(options=options)

    try:
        # Load the Google search results page
        driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        time.sleep(10)  # Let page load fully

        snippets = []
        # Get organic search results
        result_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.g')

        for result in result_blocks:
            try:
                title_element = result.find_element(By.TAG_NAME, 'h3')
                link_element = result.find_element(By.TAG_NAME, 'a')
                snippet_element = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b')  # snippet text class

                title = title_element.text
                url = link_element.get_attribute('href')
                snippet = snippet_element.text

                snippets.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet
                })

                if len(snippets) >= num_results:
                    break

            except Exception:
                continue

        return snippets

    finally:
        driver.quit()



if __name__ == "__main__":

    # Example
    query = "price of Gold in Mumbai"
    result= get_google_snippets(query)