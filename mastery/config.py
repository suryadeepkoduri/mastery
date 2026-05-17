import pathlib

DATA_FILE = pathlib.Path.home() / ".mastery" / "data.json"
AUTOSAVE_INTERVAL = 60  # seconds
GOAL_HOURS = 10_000

MILESTONES = [10, 50, 100, 250, 500, 1_000, 2_500, 5_000, 7_500, 10_000]

MILESTONE_MESSAGES = {
    10: ("🌱", "10 hours", "The seed is planted."),
    50: ("🔥", "50 hours", "You're building a habit."),
    100: ("💯", "100 hours", "First checkpoint crossed."),
    250: ("⚡", "250 hours", "Past the beginner curve."),
    500: ("🏔️", "500 hours", "Halfway to competence."),
    1_000: ("🎯", "1,000 hours", "You now think like a CS person."),
    2_500: ("🚀", "2,500 hours", "Serious depth is forming."),
    5_000: ("🌟", "5,000 hours", "Half of mastery. You're dangerous."),
    7_500: ("🦅", "7,500 hours", "The gap between you and most is enormous."),
    10_000: ("👑", "10,000 hours", "MASTERY ACHIEVED."),
}

CAT_COLORS = [
    "#64B5F6",
    "#81C784",
    "#FFB300",
    "#F06292",
    "#BA68C8",
    "#4DB6AC",
    "#FF8A65",
    "#A1887F",
    "#90A4AE",
    "#E57373",
]
