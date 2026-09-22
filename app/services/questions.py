import json
import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATA_FILE = DATA_DIR / "questions.json"


def _next_question_id(existing):
    numbers = []
    for item in existing:
        raw = str(item.get("id", ""))
        if raw.startswith("LET-"):
            try:
                numbers.append(int(raw[4:]))
            except ValueError:
                pass
    return f"LET-{(max(numbers, default=0) + 1):04d}"


def save_question(question):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    existing = []
    if DATA_FILE.exists():
        try:
            existing = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except (OSError, json.JSONDecodeError):
            existing = []

    question = {
        "id": _next_question_id(existing),
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        **question,
        "status": "New",
        "notes": "",
    }

    existing.append(question)

    temporary = DATA_FILE.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(existing, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(temporary, DATA_FILE)
    return question
