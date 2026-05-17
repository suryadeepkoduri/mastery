from rich.console import Console
from rich.text import Text
from rich.theme import Theme
from mastery.config import CAT_COLORS

THEME = Theme(
    {
        "accent": "bold #FFB300",
        "dim_text": "#666666",
        "good": "bold #00C896",
        "warn": "bold #FF6B35",
        "muted": "#888888",
        "cat": "bold #64B5F6",
        "milestone": "bold #FFD700",
        "header": "bold #EEEEEE",
    }
)

# Single console instance shared across the entire app
console = Console(theme=THEME, highlight=False)


def fmt_duration(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    elif m:
        return f"{m}m {s:02d}s"
    return f"{s}s"


def fmt_hours(seconds: float) -> str:
    return f"{seconds / 3600:.2f}h"


def rich_bar(
    current: float, total: float, width: int = 36, color: str = "#FFB300"
) -> Text:
    pct = min(current / total, 1.0) if total else 0
    filled = int(width * pct)
    bar = Text()
    bar.append("█" * filled, style=f"bold {color}")
    bar.append("░" * (width - filled), style="dim_text")
    return bar


def cat_color(cat: str, all_cats: list) -> str:
    try:
        idx = all_cats.index(cat)
    except ValueError:
        idx = 0
    return CAT_COLORS[idx % len(CAT_COLORS)]
