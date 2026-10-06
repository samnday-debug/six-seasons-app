from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from seasons import load_seasons, season_for_date
from weather import get_live_weather

# Always use Perth time - the server might be in a different timezone
today = datetime.now(ZoneInfo("Australia/Perth")).date()

seasons = load_seasons("data/seasons.csv")
season = season_for_date(today, seasons)


@st.cache_data(ttl=600)          # reuse result for 10 minutes
def cached_weather():
    return get_live_weather()


st.title(f"It's {season['name']}")
st.caption(today.strftime("%A %d %B %Y") + " · Perth")
st.write(season["short"])

weather = cached_weather()
if weather is None:
    st.warning("Live weather isn't available right now. Try again in a few minutes.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Now", f"{weather['current_temp']:.1f} °C")
    c2.metric("Today's max", f"{weather['max_temp']:.1f} °C")
    c3.metric("Today's min", f"{weather['min_temp']:.1f} °C")
    c4.metric("Rain today", f"{weather['rain_mm']:.1f} mm")
    st.caption(f"Live data from Open-Meteo, updated {weather['updated']}")