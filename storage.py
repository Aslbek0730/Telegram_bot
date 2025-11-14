import json
from pathlib import Path
from typing import Set


def _ensure_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def load_chat_ids(path: Path) -> Set[int]:
    _ensure_file(path)
    raw = path.read_text(encoding="utf-8").strip() or "[]"
    ids = json.loads(raw)
    return {int(chat_id) for chat_id in ids}


def save_chat_ids(path: Path, chat_ids: Set[int]) -> None:
    _ensure_file(path)
    serialized = json.dumps(sorted(chat_ids), ensure_ascii=False, indent=2)
    path.write_text(serialized + "\n", encoding="utf-8")

