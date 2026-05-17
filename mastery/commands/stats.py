import time
import datetime

import typer
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from mastery.commands import app
from mastery.config import GOAL_HOURS, MILESTONES
from mastery.data import load_data
from mastery.display import console, fmt_hours, rich_bar, cat_color


@app.command()
def stats():
    """Show your full progress dashboard."""
    data = load_data()
    show_stats(data)


def show_stats(data: dict):
    bonus = 0.0
    bonus_cat = None
    if data["active_session"]:
        bonus = time.time() - data["active_session"]["started_unix"]
        bonus_cat = data["active_session"].get("category", "general")

    total_s = data["total_seconds"] + bonus
    total_h = total_s / 3600
    sessions = data["sessions"]
    n_sessions = len(sessions) + (1 if data["active_session"] else 0)

    cats = dict(data["categories"])
    if bonus_cat:
        cats[bonus_cat] = cats.get(bonus_cat, 0) + bonus
    sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    all_cat_names = [c for c, _ in sorted_cats]

    next_m = next((m for m in MILESTONES if m > total_h), None)

    console.print()
    console.print(
        Rule(Text("  M A S T E R Y  ", style="bold #FFB300"), style="#333333")
    )
    console.print()

    def stat_panel(label, value, sub="", color="#FFB300"):
        t = Text(justify="center")
        t.append(value + "\n", style=f"bold {color}")
        if sub:
            t.append(sub, style="dim_text")
        return Panel(
            Align.center(t),
            title=f"[dim_text]{label}[/dim_text]",
            border_style="#333333",
            padding=(0, 2),
        )

    console.print(
        Columns(
            [
                stat_panel("TOTAL", fmt_hours(total_s), "logged", "#FFB300"),
                stat_panel("SESSIONS", str(n_sessions), "completed", "#64B5F6"),
                stat_panel("GOAL", "10,000h", "to mastery", "#888888"),
            ],
            equal=True,
            expand=True,
        )
    )
    console.print()

    bar = rich_bar(total_h, GOAL_HOURS, width=50)
    pct = total_h / GOAL_HOURS * 100
    bar_text = Text()
    bar_text.append_text(bar)
    bar_text.append(f"  {pct:.3f}%", style="accent")
    if next_m:
        left = next_m - total_h
        bar_text.append(f"\n\nnext: ", style="dim_text")
        bar_text.append(f"{next_m}h", style="milestone")
        bar_text.append(f"  —  {left:.2f}h to go", style="muted")
    if data["milestones_hit"]:
        hit = "  ".join(f"{m}h" for m in sorted(data["milestones_hit"]))
        bar_text.append(f"\nhit:  ", style="dim_text")
        bar_text.append(hit, style="good")

    console.print(
        Panel(
            Align.center(bar_text),
            title="[dim_text]PROGRESS[/dim_text]",
            border_style="#333333",
            padding=(1, 4),
        )
    )
    console.print()

    if sorted_cats:
        cat_table = Table(
            box=box.SIMPLE, show_header=True, header_style="dim_text", padding=(0, 2)
        )
        cat_table.add_column("CATEGORY", min_width=16)
        cat_table.add_column("TIME", justify="right", min_width=10)
        cat_table.add_column("SHARE", min_width=28)
        cat_table.add_column("%", justify="right", min_width=6)

        for cat, secs in sorted_cats:
            pct_cat = secs / total_s if total_s else 0
            color = cat_color(cat, all_cat_names)
            bar_w = int(pct_cat * 24)
            bar_str = Text()
            bar_str.append("█" * bar_w, style=f"bold {color}")
            bar_str.append("░" * (24 - bar_w), style="dim_text")
            cat_table.add_row(
                Text(cat, style=f"bold {color}"),
                fmt_hours(secs),
                bar_str,
                f"{pct_cat * 100:.1f}%",
            )
        console.print(
            Panel(
                cat_table,
                title="[dim_text]BY CATEGORY[/dim_text]",
                border_style="#333333",
                padding=(0, 1),
            )
        )
        console.print()

    if sessions:
        avg_s = sum(s["duration_seconds"] for s in sessions) / len(sessions)
        longest = max(sessions, key=lambda s: s["duration_seconds"])
        week_ago = time.time() - 7 * 86400
        recent = [
            s
            for s in sessions
            if datetime.datetime.fromisoformat(s["started_at"]).timestamp() > week_ago
        ]
        week_s = sum(s["duration_seconds"] for s in recent)

        sg = Table.grid(padding=(0, 3))
        sg.add_column(style="dim_text", justify="right")
        sg.add_column(style="accent")
        sg.add_column(style="dim_text", justify="right")
        sg.add_column(style="accent")
        sg.add_row(
            "avg session",
            fmt_hours(avg_s),
            "this week",
            f"{fmt_hours(week_s)}  ({len(recent)} sessions)",
        )
        sg.add_row(
            "longest",
            fmt_hours(longest["duration_seconds"]),
            "category",
            longest["category"],
        )
        console.print(
            Panel(
                sg,
                title="[dim_text]SESSION STATS[/dim_text]",
                border_style="#333333",
                padding=(1, 3),
            )
        )
        console.print()

    console.print(Rule(style="#222222"))
    console.print()
