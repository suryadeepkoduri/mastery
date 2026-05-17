# Mastery

A terminal tracker for your 10,000-hour journey to CS mastery (you can use for any field)

<img width="1507" height="880" alt="stats" src="https://github.com/user-attachments/assets/52b2fee9-5773-44fd-8400-73cdc82b6b1c" />

## Installation

```bash
pip install mastery
```

## Quick Start

```bash
# begin a timed session
mastery start dsa

# view your stats dashboard
mastery
```

## Usage

| Command | Description |
| --- | --- |
| `mastery start [category] [note]` | Start a live session. Ctrl+C to stop. |
| `mastery stop` | Stop from a second terminal window. |
| `mastery log <minutes> [category] [note]` | Log time you forgot to track. |
| `mastery status` | Check elapsed time on a running session. |
| `mastery stats` | Full dashboard: hours, categories, milestones. |
| `mastery history [-n N]` | Last N sessions (default 10). |
| `mastery categories` | Per-category breakdown with share bars. |

## Contributing

Suggestions, bug reports, and pull requests are welcome. [Open an issue](https://github.com/suryadeepkoduri/mastery/issues) to discuss what you'd like to change before submitting a PR
