"""Fetch live weather for Perth Airport from Open-Meteo (free, no API key)."""
import requests

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": -31.93,          # Perth Airport (same site as our BOM data)
    "longitude": 115.98,
    "current": "temperature_2m,precipitation",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Australia/Perth",
}


def _fetch(days):
    """Ask Open-Meteo for a forecast covering this many days."""
    response = requests.get(URL, params={**PARAMS, "forecast_days": days}, timeout=5)
    response.raise_for_status()          # error if not 200 OK
    return response.json()


def get_live_weather():
    """Return today's weather as a dict, or None if anything goes wrong."""
    try:
        data = _fetch(1)
        return {
            "current_temp": data["current"]["temperature_2m"],
            "max_temp": data["daily"]["temperature_2m_max"][0],
            "min_temp": data["daily"]["temperature_2m_min"][0],
            "rain_mm": data["daily"]["precipitation_sum"][0],
            "updated": data["current"]["time"],
        }
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return None    # no internet, API down, or unexpected response


def get_week_forecast():
    """Return a list of 7 daily forecasts, or None if anything goes wrong."""
    try:
        daily = _fetch(7)["daily"]
        week = []
        for i, day in enumerate(daily["time"]):
            week.append({
                "date": day,
                "max_temp": daily["temperature_2m_max"][i],
                "min_temp": daily["temperature_2m_min"][i],
                "rain_mm": daily["precipitation_sum"][i],
            })
        return week
    except (requests.RequestException, KeyError, IndexError, ValueError, TypeError):
        return None


if __name__ == "__main__":
    print(get_live_weather())
    for day in get_week_forecast() or []:
        print(day)