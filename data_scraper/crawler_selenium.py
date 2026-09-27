"""Optional: Google result snippets via headless Chrome (use with --snippets).

Google changes its markup often; if no snippets come back, the CSS selectors
below (div.g, div.VwiC3b) need updating.
"""
import time


def get_google_snippets(query, num_results=5, wait=5):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(options=options)  # Selenium 4.6+ downloads the driver itself
    try:
        driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
        time.sleep(wait)
        snippets = []
        for block in driver.find_elements(By.CSS_SELECTOR, "div.g"):
            try:
                snippets.append({
                    "title": block.find_element(By.TAG_NAME, "h3").text,
                    "url": block.find_element(By.TAG_NAME, "a").get_attribute("href"),
                    "snippet": block.find_element(By.CSS_SELECTOR, "div.VwiC3b").text,
                })
            except Exception:
                continue
            if len(snippets) >= num_results:
                break
        return snippets
    finally:
        driver.quit()


if __name__ == "__main__":
    for s in get_google_snippets("price of Gold in Mumbai"):
        print(s)
