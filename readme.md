# 🧠 FinVal Genie


FinVal Genie is a GenAI-powered web crawler that scrapes, interprets, and **Estimates asset valuations** using large language models.

---

## 🚀 Features

- 🌐 Google Search (`googlesearch-python`) → top 5 result URLs
- 📄 Crawler (requests + BeautifulSoup) extracts the visible article text, skipping scripts/nav/footers and unreadable pages
- 🤖 A local LLM (via [Ollama](https://ollama.com)) reads up to 3 sources and returns a fair value + rationale
- 🛡️ Robust JSON parsing (handles ```json fences, "₹6,825"-style numbers)
- 🔎 Optional: Google snippets via headless Chrome (`data_scraper/crawler_selenium.py`)
- 📊 Returns:
  ```json
  {
    "asset": "Bitcoin",
    "value": 5820000,
    "currency": "INR",
    "unit": "1 BTC",
    "note": "Price is consolidating after ETF inflows. Average of 3 sources.",
    "sources": ["https://...", "https://...", "https://..."],
    "generated_at": "2026-09-27T10:15:00"
  }
  ```

---

## ⚙️ Requirements

- Python 3.9+
- Ollama (for running a local LLM like Mistral, Llama 3, DeepSeek, etc.)
- Chrome — only for the optional Selenium snippet crawler (Selenium 4.6+ fetches the driver automatically)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚠️ Important

> ✅ **Ensure [Ollama](https://ollama.com) is running before using this bot.**  
> ✅ **Using a model other than `mistral`? Pass `--model <name>`.**

You can pull a model like:
```bash
ollama pull mistral
```

---

## 🧪 How to Use

1. **Start Ollama** (the desktop app, or `ollama serve`) and pull a model: `ollama pull mistral`

2. **Run:**
```bash
python main.py "Gold 24 carat in Mumbai"
python main.py "Bitcoin" --model llama3 --links 8
python main.py            # prompts for the asset
```
Be specific: location, quality (24 carat), unit or date help the model.

3. **Sample output** (saved to `reports/Gold_24_carat_in_Mumbai_report.json`):
```json
{
  "asset": "Gold 24 carat in Mumbai",
  "value": 68250,
  "currency": "INR",
  "unit": "10 g",
  "note": "Gold is steady on INR weakness and global demand; average of 3 sources.",
  "sources": ["https://...", "https://...", "https://..."],
  "generated_at": "2026-09-27T10:15:00"
}
```
*(Illustrative — values depend on the day's search results and the model.)*

---

## 🧪 Tests

Tests run offline — search, page fetches and the LLM are replaced with fakes.
```bash
pip install -r requirements-dev.txt
pytest
```

---


## 📌 Future Plans

- Add support for stock tickers
- Store historical reports in CSV/SQLite (JSON reports are saved already)
- Integrate into a Flask dashboard
- Plug into a daily email bot

---

## 🧑‍💻 Author

Tanay Kohale  
Open to feedback & contributions!

---

## 🛡️ Disclaimer

This project is for educational and personal analysis purposes. Do not rely on it for financial decisions without professional verification.
