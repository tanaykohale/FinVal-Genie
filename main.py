from data_scraper.crawler_selenium import get_google_snippets
from data_scraper.google_search import get_top_links

from data_scraper.crawler_beautifulsoup import extract_text_from_url
from utils.io import saveto_json
from llm.reasoning import summarize_content_ollama
# import llm.chatgpt.chatgpt_api


#### --Verry Important-- ####
# Make sure Ollama is running on port 11434 or api key is set


def main():
    asset_name = input("Enter asset name (default: Gold in Mumbai): ") or "Gold in Mumbai"
    query = f"price of {asset_name}"
    print(f"Searching for: {query}")

    top_links = get_top_links(query)

    # snippets_result= get_google_snippets(query)

    extracted_texts = [extract_text_from_url(link) for link in top_links]

    report=summarize_content_ollama(asset_name, extracted_texts[0], model="mistral")
    print(report)

    #report = llm.chatgpt.chatgpt_api.summarize_content_chatgpt(asset_name, extracted_texts[0])
    #print(report)

    saveto_json(report, f"{asset_name}_report.json")
    print('report saved.')
