import typer
from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from mastery.commands import app
from mastery.data import load_data
from mastery.display import console, fmt_hours, cat_color


@app.command()
def categories():
    """List all categories with time totals."""
    data = load_data()
    cats = data["categories"]

    if not cats:
        console.print(
            "\n[muted]No categories yet. Start: [accent]mastery start [category][/accent][/muted]\n"
        )
        return

    total_s = data["total_seconds"] or 1
    sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    all_cat_names = [c for c, _ in sorted_cats]

    table = Table(
        box=box.SIMPLE_HEAD, show_header=True, header_style="dim_text", padding=(0, 2)
    )
    table.add_column("CATEGORY", min_width=18)
    table.add_column("HOURS", justify="right", min_width=10)
    table.add_column("SHARE", min_width=26)
    table.add_column("%", justify="right", min_width=6)

    for cat, secs in sorted_cats:
        pct = secs / total_s
        color = cat_color(cat, all_cat_names)
        bar_w = int(pct * 22)
        bar = Text()
        bar.append("█" * bar_w, style=f"bold {color}")
        bar.append("░" * (22 - bar_w), style="dim_text")
        table.add_row(
            Text(cat, style=f"bold {color}"),
            Text(fmt_hours(secs), style="accent"),
            bar,
            Text(f"{pct * 100:.1f}%", style="muted"),
        )

    console.print()
    console.print(
        Panel(
            table,
            title="[dim_text]CATEGORIES[/dim_text]",
            border_style="#333333",
            padding=(0, 1),
        )
    )
    console.print()
