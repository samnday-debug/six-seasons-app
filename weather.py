"""Current conditions and forecasts for Perth Airport from Open-Meteo."""
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

PERTH = ZoneInfo("Australia/Perth")
URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": -31.93,
    "longitude": 115.98,
    "current": "temperature_2m,apparent_temperature,weather_code,is_day",
    "hourly": "temperature_2m,precipitation_probability,weather_code,is_day",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code",
    "timezone": "Australia/Perth",
    "forecast_days": 7,
}


def weather_condition(code, is_day=1):
    """Translate WMO codes, including a night icon for clear conditions."""
    if code == 0:
        return ("☀️", "Sunny") if is_day else ("🌙", "Clear")
    if code in (1, 2):
        return ("🌤️", "Partly cloudy") if is_day else ("☁️", "Partly cloudy")
    if code == 3:
        return "☁️", "Overcast"
    if code in (45, 48):
        return "🌫️", "Fog"
    if code in (51, 53, 55):
        return "🌦️", "Drizzle"
    if code in (56, 57, 66, 67):
        return "🌧️", "Freezing rain"
    if code in (61, 63, 65):
        return "🌧️", "Rain"
    if code in (71, 73, 75, 77, 85, 86):
        return "🌨️", "Snow"
    if code in (80, 81, 82):
        return "🌦️", "Showers"
    if code in (95, 96, 99):
        return "⛈️", "Thunderstorms"
    return "—", "Conditions unavailable"


def _rows(section):
    """Keep missing measurements as None rather than treating them as zero."""
    times = section.get("time", [])
    return [{"time": time, **{
        key: values[i] if isinstance(values, list) and i < len(values) else None
        for key, values in section.items() if key != "time"
    }} for i, time in enumerate(times)]


def get_live_weather(now=None):
    """Return current conditions, upcoming hours and seven days, or None."""
    now = now or datetime.now(PERTH)
    now = now.astimezone(PERTH)
    try:
        response = requests.get(URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()
        current = data.get("current") or {}
        daily = [row for row in _rows(data.get("daily") or {})
                 if datetime.fromisoformat(row["time"]).date() >= now.date()][:7]
        hourly = [row for row in _rows(data.get("hourly") or {})
                  if datetime.fromisoformat(row["time"]).replace(tzinfo=PERTH) >= now][:8]
        if not current and not daily and not hourly:
            return None
        return {"current": current, "daily": daily, "hourly": hourly}
    except (requests.RequestException, KeyError, IndexError, ValueError, TypeError, AttributeError):
        return None
