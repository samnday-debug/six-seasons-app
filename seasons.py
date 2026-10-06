"""Core logic for the Six Seasons app."""
import csv
from datetime import date

import pandas as pd


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
                "alt_name": row["alt_name"],
                "months": months_in_season(start, end),
                "short": row["short"],
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


def load_weather(path):
    """Load the cleaned BOM data, starting from the first full year (1945)."""
    df = pd.read_csv(path, parse_dates=["date"])
    return df[df["date"] >= "1945-01-01"]


def add_season_columns(df, seasons):
    """Label every day with its season and 'season year'.

    December counts towards the NEXT year's Birak, so Dec 2024 + Jan 2025
    are grouped as one season (Birak 2025) instead of being split.
    """
    lookup = {m: s["name"] for s in seasons for m in s["months"]}
    wrap_months = {m for s in seasons if s["months"][0] > s["months"][-1]
                   for m in s["months"] if m >= s["months"][0]}
    df = df.copy()
    df["season"] = df["date"].dt.month.map(lookup)
    df["season_year"] = df["date"].dt.year + df["date"].dt.month.isin(wrap_months).astype(int)
    return df


def season_summary(df):
    """Average max/min temp and average total rainfall for each season."""
    # Total rain for each individual season (e.g. Birak 1990, Birak 1991...)
    per_season = df.groupby(["season", "season_year"]).agg(
        rain=("rainfall_mm", "sum"), days=("date", "count"))
    # Skip incomplete seasons (start/end of the record) - a full one is ~59-62 days
    per_season = per_season[per_season["days"] >= 55]

    summary = df.groupby("season").agg(avg_max=("max_temp_c", "mean"),
                                       avg_min=("min_temp_c", "mean"))
    summary["avg_rain"] = per_season.groupby("season")["rain"].mean()
    return summary.round(1)


if __name__ == "__main__":
    seasons = load_seasons("data/seasons.csv")
    for test in [date(2025, 12, 25), date(2026, 1, 15), date(2026, 6, 1), date(2026, 10, 6)]:
        print(test, "->", season_for_date(test, seasons)["name"])

    weather = add_season_columns(load_weather("data/perth_daily_clean.csv"), seasons)
    print()
    print(season_summary(weather))