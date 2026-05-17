import json
import datetime
from mastery.config import DATA_FILE


def load_data() -> dict:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        default = {
            "total_seconds": 0,
            "categories": {},
            "sessions": [],
            "active_session": None,
            "milestones_hit": [],
        }
        save_data(default)
        return default
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data: dict) -> None:
    """Atomic write — temp file then rename, so JSON is never half-written."""
    tmp = DATA_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    tmp.replace(DATA_FILE)


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")