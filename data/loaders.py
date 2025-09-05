import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_DIR.mkdir(exist_ok=True)

def load_jsonl(path):
    path = Path(path)
    out = []
    if not path.exists():
        return out
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            out.append(json.loads(line))
    return out
