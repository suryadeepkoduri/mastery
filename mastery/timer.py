import time
import signal

from rich.align import Align
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from mastery.config import AUTOSAVE_INTERVAL
from mastery.data import load_data, save_data
from mastery.display import console, fmt_hours


def _make_timer_panel(
    elapsed: float, category: str, note: str, total_before: float
) -> Panel:
    h, rem = divmod(int(elapsed), 3600)
    m, s = divmod(rem, 60)

    lines = Text(justify="center")
    lines.append(f"  {category}  ", style="bold #1a1a1a on #FFB300")
    if note:
        lines.append(f"\n{note}", style="muted")
    lines.append("\n\n")
    lines.append(f"{h:02d}:{m:02d}:{s:02d}", style="bold #FFB300")
    lines.append("\n\n")
    lines.append("total so far: ", style="dim_text")
    lines.append(fmt_hours(total_before + elapsed), style="accent")
    lines.append("  /  10,000h", style="dim_text")
    lines.append("\n\n")
    lines.append("ctrl+c", style="dim #555555")
    lines.append("  to stop", style="dim_text")

    return Panel(
        Align.center(lines),
        title=Text("  M A S T E R Y  ", style="bold #FFB300"),
        title_align="center",
        border_style="#333333",
        padding=(1, 6),
        width=52,
    )


def run_live_timer(session: dict, total_before: float, category: str) -> None:
    start = session["started_unix"]
    note = session.get("note", "")
    last_save = time.time()

    def on_stop(sig, frame):
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, on_stop)
    signal.signal(signal.SIGTERM, on_stop)

    try:
        with Live(
            Align.center(_make_timer_panel(0, category, note, total_before)),
            console=console,
            refresh_per_second=4,
            screen=False,
        ) as live:
            while True:
                elapsed = time.time() - start
                live.update(
                    Align.center(
                        _make_timer_panel(elapsed, category, note, total_before)
                    )
                )

                if time.time() - last_save >= AUTOSAVE_INTERVAL:
                    data = load_data()
                    if data["active_session"]:
                        data["active_session"]["checkpoint_elapsed"] = elapsed
                        data["active_session"]["checkpoint_unix"] = time.time()
                        save_data(data)
                    last_save = time.time()

                time.sleep(0.25)

    except KeyboardInterrupt:
        pass
