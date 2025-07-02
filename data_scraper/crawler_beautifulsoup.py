import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n")
    except Exception as e:
        return ""


if __name__ == "__main__":
    #example links
    top_links = [
        "https://www.reddit.com/r/germany/comments/u0qmha/whats_the_deal_with_the_price_of_water_at_german/",
        "https://www.waternewseurope.com/water-prices-compared-in-36-eu-cities/",
        "https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=7",
        "https://www.selinawamucii.com/insights/prices/germany/mineral-water/",
        "https://worldpopulationreview.com/country-rankings/bottled-water-cost-by-country"
    ] 
    extracted_texts = [extract_text_from_url(link) for link in top_links]