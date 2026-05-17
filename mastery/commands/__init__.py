import typer

app = typer.Typer(
    add_completion=True,
    no_args_is_help=False,
    invoke_without_command=True,
    rich_markup_mode="rich",
)

# Import all command modules so their @app.command() decorators register
from mastery.commands import start, stop, status, stats, log, history, categories  # noqa: E402, F401


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """10,000 Hour Mastery Tracker. Run without args to see your stats."""
    if ctx.invoked_subcommand is None:
        from mastery.data import load_data
        from mastery.commands.status import show_status
        from mastery.commands.stats import show_stats

        data = load_data()
        if data["active_session"]:
            show_status(data)
        else:
            show_stats(data)
