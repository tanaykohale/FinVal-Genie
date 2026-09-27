import json
import re

MAX_CHARS_PER_SOURCE = 2500
MAX_SOURCES = 3


def build_prompt(asset, texts):
    """Prompt with up to MAX_SOURCES non-empty sources, each trimmed."""
    sources = [t.strip()[:MAX_CHARS_PER_SOURCE] for t in texts if t and t.strip()][:MAX_SOURCES]
    blocks = "\n\n".join(f"SOURCE {i}:\n{t}" for i, t in enumerate(sources, 1))
    return f"""You are an asset valuation expert.

Using the sources below, estimate the current market value of "{asset}".
If sources disagree, average the credible ones and say so.

{blocks}

Respond ONLY with JSON in exactly this shape:
{{
  "asset": "{asset}",
  "value": <number>,
  "currency": "<ISO code, e.g. INR, USD>",
  "unit": "<what the value is per, e.g. 10 g, 1 BTC>",
  "note": "<brief summary of key points and which sources were used>"
}}"""


def parse_llm_json(content):
    """Pull the JSON object out of an LLM reply (handles ```json fences and chatter).

    Returns a dict, or None if no valid object is found.
    """
    if not content:
        return None
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.S)
    candidates = [fenced.group(1)] if fenced else []
    start, end = content.find("{"), content.rfind("}")
    if start != -1 and end > start:
        candidates.append(content[start:end + 1])
    for c in candidates:
        try:
            data = json.loads(c)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            return normalize(data)
    return None


def normalize(data):
    """Coerce value to a number when the model returns e.g. "₹6,825"."""
    v = data.get("value")
    if isinstance(v, str):
        num = re.sub(r"[^\d.]", "", v)
        try:
            data["value"] = float(num) if "." in num else int(num)
        except ValueError:
            data["value"] = None
    return data


def summarize_content_ollama(asset, texts, model="mistral", chat_fn=None):
    """Ask a local Ollama model for a valuation. ``texts`` may be a string or a list.

    ``chat_fn(model, prompt) -> str`` can be injected for testing.
    """
    if isinstance(texts, str):
        texts = [texts]
    prompt = build_prompt(asset, texts)
    if chat_fn is None:
        import ollama  # Make sure Ollama is running (default http://localhost:11434)

        def chat_fn(m, p):
            return ollama.chat(model=m, messages=[{"role": "user", "content": p}])["message"]["content"]

    content = chat_fn(model, prompt)
    result = parse_llm_json(content)
    if result is None:
        print("Model did not return valid JSON. Raw output:\n", content)
    return result


if __name__ == "__main__":
    sample = ("Water prices in Germany vary across cities. On average tap water costs "
              "around 2.00 EUR per cubic meter.")
    print(summarize_content_ollama("Water in Germany", sample))
