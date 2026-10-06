"""Core logic for the Six Seasons app."""
import csv
from datetime import date


def months_in_season(start, end):
    """List the months in a season, wrapping past December.
    e.g. months_in_season(12, 1) -> [12, 1]
    """
    months = [start]
    m = start
    while m != end:
        m = m % 12 + 1      # 12 -> 1, otherwise +1
        months.append(m)
    return months


def load_seasons(path):
    """Read seasons.csv and check every month is covered exactly once."""
    seasons = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            start, end = int(row["start_month"]), int(row["end_month"])
            seasons.append({
                "name": row["season"],
                "months": months_in_season(start, end),
                "description": row["description"],
                "source": row["source"],
            })
    all_months = sorted(m for s in seasons for m in s["months"])
    if all_months != list(range(1, 13)):
        raise ValueError("Seasons must cover each month exactly once")
    return seasons


def season_for_date(d, seasons):
    """Return the season that a date falls in."""
    if not isinstance(d, date):
        raise TypeError("Expected a date")
    for s in seasons:
        if d.month in s["months"]:
            return s


if __name__ == "__main__":
    seasons = load_seasons("data/seasons.csv")
    for test in [date(2025, 12, 25), date(2026, 1, 15), date(2026, 6, 1), date(2026, 10, 6)]:
        print(test, "->", season_for_date(test, seasons)["name"])