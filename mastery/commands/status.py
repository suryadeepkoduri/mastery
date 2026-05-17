import time

import typer
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mastery.commands import app
from mastery.data import load_data
from mastery.display import console, fmt_duration, fmt_hours


@app.command()
def status():
    """Show current session status."""
    data = load_data()
    show_status(data)


def show_status(data: dict):
    session = data["active_session"]
    console.print()
    if session is None:
        console.print(
            Panel(
                Text.assemble(
                    ("No session running.\n\n", "dim_text"),
                    ("Total logged: ", "dim_text"),
                    (fmt_hours(data["total_seconds"]), "accent"),
                    "\n",
                    ("Start:  ", "dim_text"),
                    ("mastery start [category]", "accent"),
                ),
                title="[dim_text]STATUS[/dim_text]",
                border_style="#333333",
                padding=(1, 3),
            )
        )
    else:
        elapsed = time.time() - session["started_unix"]
        cat = session.get("category", "general")
        note = session.get("note", "")
        grid = Table.grid(padding=(0, 2))
        grid.add_column(style="dim_text", justify="right")
        grid.add_column(style="accent")
        grid.add_row("category", f"[cat]{cat}[/cat]")
        grid.add_row("started", session["started_at"])
        grid.add_row("elapsed", fmt_duration(elapsed))
        if note:
            grid.add_row("note", f"[muted]{note}[/muted]")
        grid.add_row("running total", fmt_hours(data["total_seconds"] + elapsed))
        console.print(
            Panel(
                grid,
                title="[accent]▶  SESSION RUNNING[/accent]",
                border_style="#FFB300",
                padding=(1, 3),
            )
        )
    console.print()
