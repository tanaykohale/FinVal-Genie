# 🧠 FinVal Genie


FinVal Genie is a GenAI-powered web crawler that scrapes, interprets, and **Estimates asset valuations** using large language models.

---

## 🚀 Features

- 🌐 Google Search + Web Crawler (Selenium) 
- 📄 Extracts snippets + full article text
- 🤖 Summarizes market value & sentiment using LLM (via [Ollama](https://ollama.com))
- 📊 Returns:  
  ```json
  {
    "asset": "Bitcoin",
    "value": 5820000,
    "note": "Price is consolidating due to ETF approval. Average value from 3 sources."
  }
  ```

---

## ⚙️ Requirements

- Python 3.8+
- Chrome + [ChromeDriver](https://chromedriver.chromium.org/)
- Ollama (for running local LLM like Mistral, Deepseek, etc.)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## ⚠️ Important

> ✅ **Ensure [Ollama](https://ollama.com) is running before using this bot.**  
> ✅ **Replace the model name in code if you're using something other than  `mistral`.**

You can pull a model like:
```bash
ollama pull mistral
```

---

## 🧪 How to Use

1. **Start Ollama (if not running already):**
```bash
ollama run mistral
```

2. **Run the script:**
```bash
python main.py
```
Enter asset name and details (Demographics, or time or quality like 24 carat)
3. **Sample Output:**
```json
{
  "asset": "Gold",
  "value": 6825,
  "note": "Gold is trading steady due to INR weakness and global demand. Bloomberg, Economic Times, and Coindesk average suggests ₹6825 per 10g."
}
```

---


## 📌 Future Plans

- Add support for stock tickers
- Store historical reports in CSV/SQLite
- Integrate into a Flask dashboard
- Plug into a daily email bot

---

## 🧑‍💻 Author

Tanay Kohale  
Open to feedback & contributions!

---

## 🛡️ Disclaimer

This project is for educational and personal analysis purposes. Do not rely on it for financial decisions without professional verification.
