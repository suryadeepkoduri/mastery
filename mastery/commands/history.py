import typer
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mastery.commands import app
from mastery.data import load_data
from mastery.display import console, fmt_duration, cat_color


@app.command()
def history(
    n: int = typer.Option(10, "--n", "-n", help="Number of sessions to show"),
):
    """Show recent sessions."""
    data = load_data()
    sessions = data["sessions"]

    if not sessions:
        console.print("\n[muted]No sessions recorded yet.[/muted]\n")
        return

    recent = sessions[-n:][::-1]
    all_cat_names = sorted(set(s.get("category", "general") for s in sessions))

    table = Table(
        box=box.SIMPLE_HEAD, show_header=True, header_style="dim_text", padding=(0, 2)
    )
    table.add_column("DATE", min_width=12)
    table.add_column("CATEGORY", min_width=14)
    table.add_column("DURATION", justify="right", min_width=12)
    table.add_column("NOTE", min_width=24)

    for s in recent:
        date = s["started_at"][:10]
        cat = s.get("category", "general")
        color = cat_color(cat, all_cat_names)
        dur = fmt_duration(s["duration_seconds"])
        note = s.get("note", "")[:30]
        suffix = " [manual]" if s.get("manual") else ""
        table.add_row(
            Text(date, style="muted"),
            Text(cat, style=f"bold {color}"),
            Text(dur, style="accent"),
            Text(note + suffix, style="muted"),
        )

    console.print()
    console.print(
        Panel(
            table,
            title=f"[dim_text]LAST {min(n, len(sessions))} SESSIONS[/dim_text]",
            border_style="#333333",
            padding=(0, 1),
        )
    )
    console.print()
