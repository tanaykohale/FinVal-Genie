from llm.reasoning import build_prompt, parse_llm_json, summarize_content_ollama


def test_parse_plain_json():
    assert parse_llm_json('{"asset": "Gold", "value": 6825}') == {"asset": "Gold", "value": 6825}


def test_parse_fenced_json_with_chatter():
    reply = 'Sure! Here you go:\n```json\n{"asset": "BTC", "value": 5820000, "currency": "INR"}\n```\nHope it helps'
    assert parse_llm_json(reply)["currency"] == "INR"


def test_parse_value_string_with_symbol():
    assert parse_llm_json('{"asset": "Gold", "value": "₹6,825"}')["value"] == 6825
    assert parse_llm_json('{"asset": "Gold", "value": "$1,234.50"}')["value"] == 1234.5
    assert parse_llm_json('{"asset": "Gold", "value": "unknown"}')["value"] is None


def test_parse_garbage():
    assert parse_llm_json("") is None
    assert parse_llm_json("no json here") is None
    assert parse_llm_json("{broken") is None
    assert parse_llm_json("[1, 2]") is None


def test_prompt_uses_up_to_three_nonempty_sources_and_trims():
    p = build_prompt("Gold", ["", "   ", "a" * 10000, "second", "third", "fourth"])
    assert "SOURCE 3" in p and "SOURCE 4" not in p
    assert "fourth" not in p
    assert "a" * 2501 not in p
    assert '"currency"' in p


def test_summarize_with_injected_llm():
    seen = {}

    def fake_chat(model, prompt):
        seen["model"], seen["prompt"] = model, prompt
        return '{"asset": "Gold", "value": 7000, "currency": "INR", "unit": "1 g", "note": "ok"}'

    r = summarize_content_ollama("Gold", "Gold is 7000 INR/g", model="llama3", chat_fn=fake_chat)
    assert r["value"] == 7000 and seen["model"] == "llama3"
    assert "Gold is 7000 INR/g" in seen["prompt"]


def test_summarize_returns_none_on_bad_output(capsys):
    assert summarize_content_ollama("Gold", "x", chat_fn=lambda m, p: "I cannot help") is None
    assert "did not return valid JSON" in capsys.readouterr().out
