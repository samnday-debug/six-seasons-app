"""Today's season, current conditions and Perth Airport forecast."""
from datetime import datetime
from html import escape
from math import isfinite
from zoneinfo import ZoneInfo
import streamlit as st
from seasons import load_seasons, season_for_date
from weather import get_live_weather, weather_condition
from ui import apply_style

apply_style()


def measurement(value, suffix="°", decimals=0):
    if not isinstance(value, (int, float)) or not isfinite(value):
        return "—"
    return f"{value:.{decimals}f}{suffix}"


def condition(row):
    icon, label = weather_condition(row.get("weather_code"), row.get("is_day", 1))
    return icon, escape(label)


@st.cache_data(ttl=600)
def cached_weather():
    return get_live_weather()


now = datetime.now(ZoneInfo("Australia/Perth"))
today = now.date()
season = season_for_date(today, load_seasons("data/seasons.csv"))
st.title(f"It's {season['name']}")
st.caption(today.strftime("%A %d %B %Y") + " · Perth Airport")
st.write(season["short"])

st.markdown('''<style>
.wx-hero{display:flex;align-items:center;justify-content:space-between;gap:28px;padding:30px 36px;border-radius:18px;background:linear-gradient(115deg,#c8eaff,#8bc8fa);color:#102c48;margin:12px 0 22px}
.wx-location{font-size:20px;font-weight:600}.wx-temp{font-size:88px;font-weight:700;line-height:1.15}.wx-condition{font-size:22px;font-weight:600}.wx-muted{opacity:.8}.wx-stats{display:grid;grid-template-columns:1fr 1fr;gap:20px 32px}.wx-stat strong{display:block;font-size:32px}.wx-stat small{font-size:15px}.wx-hero-icon{font-size:100px}
.wx-panel{border:1px solid #dce3ea;border-radius:16px;padding:20px;margin-bottom:18px}.wx-panel h3{font-size:22px;margin:0 0 18px}.wx-hours{display:flex;overflow-x:auto;padding-bottom:8px}.wx-hour{flex:1;min-width:100px;text-align:center;border-right:1px solid #e1e6ed}.wx-hour:last-child{border:0}.wx-icon{font-size:30px;display:block;margin:8px 0}.wx-hour strong{display:block;font-size:22px}.wx-rain{color:#0877cc;font-size:14px;margin-top:8px}.wx-table-wrap{overflow-x:auto}.wx-table{width:100%;border-collapse:collapse;white-space:nowrap}.wx-table th{font-weight:400;text-align:left;opacity:.8}.wx-table td,.wx-table th{padding:10px 12px;border-bottom:1px solid #e5e9ef}.wx-table .wx-today{background:#eaf5ff;color:#14324d}.wx-small{font-size:13px;opacity:.75;margin-left:8px}
@media(max-width:700px){.wx-hero{padding:22px;gap:18px;flex-wrap:wrap}.wx-temp{font-size:64px}.wx-hero-icon{display:none}.wx-stats{gap:12px 24px}.wx-stat strong{font-size:26px}.wx-panel{padding:14px}.wx-table td,.wx-table th{padding:10px 8px}}
</style>''', unsafe_allow_html=True)

weather = cached_weather()
if weather is None:
    st.warning("Weather isn't available right now. Please try again in a few minutes.")
else:
    current = weather["current"]
    daily = [row for row in weather["daily"] if datetime.fromisoformat(row["time"]).date() >= today]
    first = next((row for row in daily if row["time"] == today.isoformat()), {})
    icon, label = condition(current)
    st.markdown(f'''<section class="wx-hero" aria-label="Current weather and today's forecast">
<div><div class="wx-location">Perth Airport</div><div class="wx-temp">{measurement(current.get('temperature_2m'))}</div><div class="wx-condition">{label}</div><div class="wx-muted">Feels like {measurement(current.get('apparent_temperature'))}</div></div>
<div class="wx-stats"><div class="wx-stat"><small>Forecast high</small><strong>{measurement(first.get('temperature_2m_max'))}</strong></div><div class="wx-stat"><small>Forecast low</small><strong>{measurement(first.get('temperature_2m_min'))}</strong></div><div class="wx-stat"><small>Rain chance</small><strong>{measurement(first.get('precipitation_probability_max'), '%')}</strong></div><div class="wx-stat"><small>Forecast rain</small><strong>{measurement(first.get('precipitation_sum'), ' mm', 1)}</strong></div></div><div class="wx-hero-icon" aria-hidden="true">{icon}</div></section>''', unsafe_allow_html=True)
    hours = []
    for row in weather["hourly"]:
        time = datetime.fromisoformat(row["time"]).replace(tzinfo=ZoneInfo("Australia/Perth"))
        if time < now:
            continue
        icon, label = condition(row)
        time_label = time.strftime("%I %p").lstrip("0").lower()
        if time.date() != today:
            time_label += "<br><small>Tomorrow</small>"
        hours.append(f'<div class="wx-hour">{time_label}<span class="wx-icon" title="{label}" role="img" aria-label="{label}">{icon}</span><strong>{measurement(row.get("temperature_2m"))}</strong><div class="wx-rain">{measurement(row.get("precipitation_probability"), "%")} rain</div></div>')
    if hours:
        st.markdown('<section class="wx-panel"><h3>Next hours</h3><div class="wx-hours">' + ''.join(hours) + '</div></section>', unsafe_allow_html=True)
    else:
        st.info("Hourly forecast is currently unavailable.")
    rows = []
    for row in daily:
        date = datetime.fromisoformat(row["time"]).date()
        day = "Today" if date == today else date.strftime("%a")
        icon, label = condition(row)
        css = ' class="wx-today"' if date == today else ''
        rows.append(f'<tr{css}><td><strong>{day}</strong><span class="wx-small">{date.day} {date.strftime("%b")}</span></td><td>{icon} {label}</td><td>{measurement(row.get("temperature_2m_min"))} / <strong>{measurement(row.get("temperature_2m_max"))}</strong></td><td>{measurement(row.get("precipitation_probability_max"), "%")}</td><td>{measurement(row.get("precipitation_sum"), " mm", 1)}</td></tr>')
    if rows:
        st.markdown('<section class="wx-panel"><h3>7-day forecast</h3><div class="wx-table-wrap"><table class="wx-table"><thead><tr><th scope="col">Day</th><th scope="col">Conditions</th><th scope="col">Low / High</th><th scope="col">Rain chance</th><th scope="col">Forecast rain</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div></section>', unsafe_allow_html=True)
    else:
        st.info("Daily forecast is currently unavailable.")
    st.caption("Temperatures in °C · Times in Perth time · — means unavailable. Rainfall amounts are forecasts, not recorded rainfall.")
    updated = current.get("time")
    if updated:
        st.caption(f"Current conditions valid at {updated.replace('T', ' ')} AWST")
    st.caption("Weather and forecasts: [Open-Meteo](https://open-meteo.com/) · Refreshes every 10 minutes.")
