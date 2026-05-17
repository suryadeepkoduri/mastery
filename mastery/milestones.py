from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from mastery.config import MILESTONES, MILESTONE_MESSAGES
from mastery.display import console


def check_and_render_milestones(data: dict, previous_seconds: float) -> None:
    prev_h = previous_seconds / 3600
    curr_h = data["total_seconds"] / 3600
    for m in MILESTONES:
        if prev_h < m <= curr_h and m not in data["milestones_hit"]:
            data["milestones_hit"].append(m)
            icon, label, msg = MILESTONE_MESSAGES[m]
            console.print()
            console.print(
                Align.center(
                    Panel(
                        Align.center(
                            Text.assemble(
                                (f"{icon}  ", ""),
                                (label, "milestone"),
                                "\n",
                                (msg, "bold white"),
                            )
                        ),
                        border_style="milestone",
                        padding=(1, 4),
                    )
                )
            )
            console.print()
