import json
import os
import re


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", name).strip("_") or "report"


def saveto_json(data, filename):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filename
