"""Fetch live weather for Perth Airport from Open-Meteo (free, no API key)."""
import requests

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": -31.93,          # Perth Airport (same site as our BOM data)
    "longitude": 115.98,
    "current": "temperature_2m,precipitation",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Australia/Perth",
    "forecast_days": 1,
}


def get_live_weather():
    """Return today's weather as a dict, or None if anything goes wrong."""
    try:
        response = requests.get(URL, params=PARAMS, timeout=5)
        response.raise_for_status()          # error if not 200 OK
        data = response.json()
        return {
            "current_temp": data["current"]["temperature_2m"],
            "max_temp": data["daily"]["temperature_2m_max"][0],
            "min_temp": data["daily"]["temperature_2m_min"][0],
            "rain_mm": data["daily"]["precipitation_sum"][0],
            "updated": data["current"]["time"],
        }
    except (requests.RequestException, KeyError, IndexError, ValueError):
        return None    # no internet, API down, or unexpected response


if __name__ == "__main__":
    print(get_live_weather())
    