from datetime import date

import pandas as pd
import pytest
import requests

import seasons as core
import weather

SEASONS_FILE = "data/seasons.csv"


@pytest.fixture
def seasons():
    return core.load_seasons(SEASONS_FILE)


# ---------- Main functionality ----------

def test_six_seasons_cover_every_month(seasons):
    assert len(seasons) == 6
    assert sorted(m for s in seasons for m in s["months"]) == list(range(1, 13))


@pytest.mark.parametrize("d, expected", [
    (date(2026, 6, 15), "Mookaroo"),
    (date(2026, 10, 6), "Kambarang"),
])
def test_season_for_date(seasons, d, expected):
    assert core.season_for_date(d, seasons)["name"] == expected


def test_month_table_has_12_months_starting_december(seasons):
    table = core.month_table(seasons)
    assert len(table) == 12
    assert table.iloc[0]["month"] == "Dec"


def test_other_seasons_finds_whale_in_djilba(seasons):
    signs = core.load_signs("data/seasonal_signs.csv", seasons)
    assert core.other_seasons(signs, "Eubalaena australis", "Mookaroo") == ["Djilba"]


# ---------- Algorithmic core ----------

def test_months_wrap_past_december():
    assert core.months_in_season(12, 1) == [12, 1]
    assert core.months_in_season(10, 11) == [10, 11]


def test_december_joins_next_years_birak(seasons):
    df = pd.DataFrame({"date": pd.to_datetime(["2024-12-15", "2025-01-15"])})
    out = core.add_season_columns(df, seasons)
    assert list(out["season"]) == ["Birak", "Birak"]
    assert list(out["season_year"]) == [2025, 2025]


def test_linear_trend_exact_line():
    slope, intercept = core.linear_trend([(0, 1), (1, 3), (2, 5)])
    assert slope == pytest.approx(2)
    assert intercept == pytest.approx(1)


def test_season_summary_skips_incomplete_seasons(seasons):
    full = pd.date_range("2000-06-01", "2000-07-31")      # 61 days
    partial = pd.date_range("2001-06-01", "2001-06-10")   # 10 days
    df = pd.DataFrame({"date": full.append(partial)})
    df["max_temp_c"] = 20.0
    df["min_temp_c"] = 10.0
    df["rainfall_mm"] = [1.0] * len(full) + [100.0] * len(partial)
    summary = core.season_summary(core.add_season_columns(df, seasons))
    assert summary.loc["Mookaroo", "avg_rain"] == 61.0   # partial season ignored


# ---------- Boundary conditions ----------

@pytest.mark.parametrize("d, expected", [
    (date(2025, 12, 1), "Birak"),      # first day of Birak
    (date(2026, 1, 31), "Birak"),      # last day of Birak, after new year
    (date(2026, 3, 31), "Boonaroo"),   # last day of Boonaroo
    (date(2026, 4, 1), "Djiran"),      # first day of Djiran
])
def test_season_boundaries(seasons, d, expected):
    assert core.season_for_date(d, seasons)["name"] == expected


# ---------- Invalid input & edge cases ----------

def test_season_for_date_rejects_non_date(seasons):
    with pytest.raises(TypeError):
        core.season_for_date("2026-10-06", seasons)


def test_overlapping_seasons_rejected(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("season,alt_name,start_month,end_month,short,description,source\n"
                   "A,A,1,6,,,\nB,B,6,12,,,\n")
    with pytest.raises(ValueError):
        core.load_seasons(bad)


def test_linear_trend_needs_two_points():
    with pytest.raises(ValueError):
        core.linear_trend([(2000, 20.0)])


def test_linear_trend_rejects_same_year():
    with pytest.raises(ValueError):
        core.linear_trend([(2000, 1.0), (2000, 2.0)])


def test_signs_with_unknown_season_rejected(tmp_path, seasons):
    bad = tmp_path / "signs.csv"
    bad.write_text("Season,Type,Scientific name\nSummer,Flora,X\n")
    with pytest.raises(ValueError):
        core.load_signs(bad, seasons)


def test_other_seasons_blank_name_returns_empty(seasons):
    signs = core.load_signs("data/seasonal_signs.csv", seasons)
    assert core.other_seasons(signs, "", "Mookaroo") == []


# ---------- Failure cases: no internet / API responses ----------

def test_live_weather_returns_none_when_offline(monkeypatch):
    def fail(*args, **kwargs):
        raise requests.ConnectionError("no internet")
    monkeypatch.setattr(weather.requests, "get", fail)
    assert weather.get_live_weather() is None


def test_week_forecast_returns_none_when_offline(monkeypatch):
    def fail(*args, **kwargs):
        raise requests.ConnectionError("no internet")
    monkeypatch.setattr(weather.requests, "get", fail)
    assert weather.get_week_forecast() is None


def test_week_forecast_parses_response(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"daily": {"time": ["2026-10-08", "2026-10-09"],
                              "temperature_2m_max": [25.0, 27.5],
                              "temperature_2m_min": [12.0, 13.1],
                              "precipitation_sum": [0.0, 2.4]}}
    monkeypatch.setattr(weather.requests, "get", lambda *a, **k: FakeResponse())
    week = weather.get_week_forecast()
    assert len(week) == 2
    assert week[1] == {"date": "2026-10-09", "max_temp": 27.5, "min_temp": 13.1, "rain_mm": 2.4}