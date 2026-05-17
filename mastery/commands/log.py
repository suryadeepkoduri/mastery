import typer
from rich.panel import Panel
from rich.table import Table

from mastery.commands import app
from mastery.data import load_data, save_data, now_iso
from mastery.display import console, fmt_duration, fmt_hours
from mastery.milestones import check_and_render_milestones


@app.command()
def log(
    minutes: float = typer.Argument(..., help="Duration in minutes"),
    category: str = typer.Argument("general", help="Category label"),
    note: str = typer.Argument("", help="Optional note"),
):
    """Manually log a completed time block (forgot to start the timer?)."""
    if minutes <= 0:
        console.print("[warn]Minutes must be a positive number.[/warn]")
        raise typer.Exit(1)

    data = load_data()
    seconds = minutes * 60
    category = category.lower().strip()
    note = note.strip()
    previous = data["total_seconds"]

    data["total_seconds"] += seconds
    data["categories"].setdefault(category, 0)
    data["categories"][category] += seconds
    data["sessions"].append(
        {
            "started_at": now_iso(),
            "ended_at": now_iso(),
            "duration_seconds": seconds,
            "category": category,
            "manual": True,
            **({"note": note} if note else {}),
        }
    )

    check_and_render_milestones(data, previous)
    save_data(data)

    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="dim_text", justify="right")
    grid.add_column(style="accent")
    grid.add_row("logged", fmt_duration(seconds))
    grid.add_row("category", f"[cat]{category}[/cat]")
    if note:
        grid.add_row("note", f"[muted]{note}[/muted]")
    grid.add_row("total", fmt_hours(data["total_seconds"]))

    console.print()
    console.print(Panel("✓  Manually logged", border_style="good", padding=(0, 3)))
    console.print(Panel(grid, border_style="#333333", padding=(0, 3)))
    console.print()
