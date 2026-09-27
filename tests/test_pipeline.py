import json

import main as app
from data_scraper.crawler_beautifulsoup import extract_text_from_url, html_to_text
from utils.io import safe_filename, saveto_json


def test_html_to_text_drops_scripts_and_nav():
    html = "<html><nav>Menu</nav><script>var x=1</script><p>Gold  is</p>\n\n<p>₹7000</p><footer>©</footer></html>"
    assert html_to_text(html) == "Gold  is\n₹7000"


def test_extract_text_returns_empty_on_error():
    class Boom:
        def get(self, *a, **k):
            import requests
            raise requests.ConnectionError("down")
    assert extract_text_from_url("http://x", session=Boom()) == ""


def fake_llm(asset, texts, model):
    return {"asset": asset, "value": len(texts), "currency": "INR", "note": model}


def test_run_skips_unreadable_pages_and_records_sources():
    pages = {"a": "", "b": "gold 7000", "c": "gold 7100", "d": "gold 6900", "e": "gold 7050"}
    r = app.run("Gold", model="m",
                search_fn=lambda q, num: list(pages),
                fetch_fn=lambda url: pages[url],
                llm_fn=fake_llm)
    assert r["value"] == 4           # 4 non-empty pages passed to the LLM
    assert r["sources"] == ["b", "c", "d"]
    assert r["note"] == "m" and "generated_at" in r


def test_run_returns_none_when_nothing_readable():
    assert app.run("Gold", search_fn=lambda q, num: ["x"], fetch_fn=lambda u: "", llm_fn=fake_llm) is None


def test_run_returns_none_when_llm_fails():
    assert app.run("Gold", search_fn=lambda q, num: ["x"], fetch_fn=lambda u: "t",
                   llm_fn=lambda *a, **k: None) is None


def test_main_cli_saves_report(tmp_path, monkeypatch):
    monkeypatch.setattr(app, "run", lambda asset, model, num_links: {"asset": asset, "value": 1})
    assert app.main(["Gold 24k in Mumbai", "--out", str(tmp_path)]) == 0
    saved = json.loads((tmp_path / "Gold_24k_in_Mumbai_report.json").read_text())
    assert saved["asset"] == "Gold 24k in Mumbai"


def test_io_helpers(tmp_path):
    assert safe_filename("Gold / 24k?") == "Gold_24k"
    assert safe_filename("???") == "report"
    p = saveto_json({"v": "₹"}, str(tmp_path / "sub" / "r.json"))
    assert json.loads(open(p, encoding="utf-8").read()) == {"v": "₹"}
