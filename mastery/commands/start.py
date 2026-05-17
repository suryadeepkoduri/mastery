import typer
from rich.panel import Panel
from rich.text import Text

from mastery.commands import app
from mastery.data import load_data, save_data, now_iso
from mastery.display import console, fmt_duration
from mastery.timer import run_live_timer

import time


@app.command()
def start(
    category: str = typer.Argument(
        "general", help="What you're working on (e.g. leetcode, dsa, os)"
    ),
    note: str = typer.Argument("", help="Optional short note"),
):
    """Start a timed work session."""
    data = load_data()

    if data["active_session"] is not None:
        s = data["active_session"]
        elapsed = time.time() - s["started_unix"]
        console.print()
        console.print(
            Panel(
                Text.assemble(
                    ("⚠  Session already running\n\n", "warn"),
                    ("category : ", "dim_text"),
                    (s.get("category", "general"), "cat"),
                    "\n",
                    ("elapsed  : ", "dim_text"),
                    (fmt_duration(elapsed), "accent"),
                    "\n\n",
                    ("Run ", "dim_text"),
                    ("mastery stop", "accent"),
                    (" to end it first.", "dim_text"),
                ),
                border_style="warn",
                padding=(1, 3),
            )
        )
        return

    category = category.lower().strip()
    note = note.strip()

    session = {
        "started_at": now_iso(),
        "started_unix": time.time(),
        "category": category,
        "note": note,
    }
    data["active_session"] = session
    save_data(data)

    console.print()
    run_live_timer(session, data["total_seconds"], category)
    console.print()

    # Ctrl+C exits the timer — fall through to stop
    from mastery.commands.stop import do_stop

    do_stop()
