# --  Extracting Additional data from URLs using BeautifulSoup and requests
from googlesearch import search

def get_top_links(query, num=5):
    return list(search(query, num_results=num))


if __name__ == "__main__":
    asset_name = input("Enter asset name (default: Gold in Mumbai): ") or "Gold in Mumbai"
    query = f"price of {asset_name}"
    top_links = get_top_links(query)