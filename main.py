"""FinVal Genie: search the web for an asset, read the top pages, ask a local LLM for a fair value.

Make sure Ollama is running (http://localhost:11434) and the model is pulled:
    ollama pull mistral
"""
import argparse
from datetime import datetime

from data_scraper.crawler_beautifulsoup import extract_text_from_url
from llm.reasoning import summarize_content_ollama
from utils.io import safe_filename, saveto_json


def run(asset_name, model="mistral", num_links=5,
        search_fn=None, fetch_fn=extract_text_from_url, llm_fn=summarize_content_ollama):
    """Full pipeline. Dependencies are injectable so it can be tested offline."""
    if search_fn is None:
        from data_scraper.google_search import get_top_links as search_fn

    query = f"price of {asset_name}"
    print(f"Searching for: {query}")
    links = search_fn(query, num=num_links)
    texts, used = [], []
    for link in links:
        text = fetch_fn(link)
        if text.strip():
            texts.append(text)
            used.append(link)
    if not texts:
        print("Could not read any search result pages.")
        return None

    report = llm_fn(asset_name, texts, model=model)
    if report is None:
        return None
    report["sources"] = used[:3]
    report["generated_at"] = datetime.now().isoformat(timespec="seconds")
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description="Estimate an asset's market value with a local LLM.")
    p.add_argument("asset", nargs="?", help='e.g. "Gold 24 carat in Mumbai" (prompted if omitted)')
    p.add_argument("--model", default="mistral", help="Ollama model name (default: mistral)")
    p.add_argument("--links", type=int, default=5, help="search results to read (default: 5)")
    p.add_argument("--out", default="reports", help="output folder (default: reports/)")
    args = p.parse_args(argv)

    asset = args.asset or input("Enter asset name (default: Gold in Mumbai): ").strip() or "Gold in Mumbai"
    report = run(asset, model=args.model, num_links=args.links)
    if report is None:
        return 1
    print(report)
    path = saveto_json(report, f"{args.out}/{safe_filename(asset)}_report.json")
    print(f"Report saved to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
