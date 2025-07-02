import ollama
import json

### --- Very Important -- ###
# Make sure Ollama is running

def summarize_content_ollama(asset, text, model="mistral"):
    prompt = f"""
You are an asset valuation expert.

Given this text, estimate the current market value of "{asset}" and summarize the reasoning briefly.

TEXT:
{text[:4000]}

Respond only in JSON format like this:
{{
  "asset": "{asset}",
  "value": <number>,
  "note": "<brief summary of key points>"
}}
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    content = response['message']['content']

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Model did not return valid JSON.")
        print("Raw output:", content)
        return None


if __name__ == "__main__":
    asset = "Water in Germany"
    text = """
    Water prices in Germany vary significantly across different cities and regions. 
    On average, the cost of tap water is around 2.00 EUR per cubic meter, while bottled water can range from 0.50 to 2.00 EUR per liter.
    Factors influencing these prices include local infrastructure, supply sources, and demand.
    """
    
    result = summarize_content_ollama(asset, text)
    print(result)
