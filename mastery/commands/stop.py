import time

import typer
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mastery.commands import app
from mastery.config import GOAL_HOURS, MILESTONES
from mastery.data import load_data, save_data, now_iso
from mastery.display import console, fmt_duration, fmt_hours, rich_bar
from mastery.milestones import check_and_render_milestones


@app.command()
def stop():
    """Stop the current session."""
    do_stop()


def do_stop():
    data = load_data()

    if data["active_session"] is None:
        console.print()
        console.print(
            Panel(
                Text.assemble(
                    ("No session is running.\n\n", "warn"),
                    ("Start one: ", "dim_text"),
                    ("mastery start [category]", "accent"),
                ),
                border_style="#444444",
                padding=(1, 3),
            )
        )
        return

    session = data["active_session"]
    elapsed = time.time() - session["started_unix"]
    category = session.get("category", "general")
    note = session.get("note", "")
    previous = data["total_seconds"]

    data["total_seconds"] += elapsed
    data["categories"].setdefault(category, 0)
    data["categories"][category] += elapsed
    data["sessions"].append(
        {
            "started_at": session["started_at"],
            "ended_at": now_iso(),
            "duration_seconds": round(elapsed, 1),
            "category": category,
            **({"note": note} if note else {}),
        }
    )
    data["active_session"] = None

    check_and_render_milestones(data, previous)
    save_data(data)

    total_h = data["total_seconds"] / 3600
    next_m = next((m for m in MILESTONES if m > total_h), None)

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="dim_text", justify="right")
    grid.add_column(style="accent")
    grid.add_row("duration", fmt_duration(elapsed))
    grid.add_row("category", f"[cat]{category}[/cat]")
    if note:
        grid.add_row("note", f"[muted]{note}[/muted]")
    grid.add_row("total", f"{fmt_hours(data['total_seconds'])}  /  10,000h")
    if next_m:
        left = next_m - total_h
        grid.add_row("next milestone", f"[muted]{next_m}h  ({left:.2f}h away)[/muted]")

    bar = rich_bar(total_h, GOAL_HOURS)
    bar_text = Text()
    bar_text.append_text(bar)
    bar_text.append(f"  {total_h / GOAL_HOURS * 100:.3f}%", style="accent")

    console.print(
        Panel(
            Align.left(Text.assemble(("■  Session saved\n\n", "good"), bar_text, "\n")),
            border_style="good",
            padding=(0, 3),
        )
    )
    console.print(Panel(grid, border_style="#333333", padding=(0, 3)))
    console.print()
