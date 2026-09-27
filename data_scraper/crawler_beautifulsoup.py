import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}
NOISE_TAGS = ["script", "style", "noscript", "nav", "footer", "header", "aside", "form"]


def html_to_text(html):
    """Visible article text: drop scripts/nav/footer, collapse blank lines."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(NOISE_TAGS):
        tag.decompose()
    lines = (line.strip() for line in soup.get_text(separator="\n").splitlines())
    return "\n".join(line for line in lines if line)


def extract_text_from_url(url, timeout=10, session=None):
    """Return the page's visible text, or "" if the page cannot be fetched."""
    try:
        response = (session or requests).get(url, timeout=timeout, headers=HEADERS)
        response.raise_for_status()
        return html_to_text(response.text)
    except requests.RequestException:
        return ""


if __name__ == "__main__":
    print(extract_text_from_url("https://www.numbeo.com/cost-of-living/")[:500])
