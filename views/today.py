from datetime import date, datetime
from zoneinfo import ZoneInfo
import altair as alt
import pandas as pd
import streamlit as st
from seasons import load_seasons, season_for_date
from weather import get_live_weather, get_week_forecast

# Always use Perth time - the server might be in a different timezone
today = datetime.now(ZoneInfo("Australia/Perth")).date()

seasons = load_seasons("data/seasons.csv")
season = season_for_date(today, seasons)


@st.cache_data(ttl=600)          # reuse result for 10 minutes
def cached_weather():
    return get_live_weather()


@st.cache_data(ttl=1800)         # forecast changes slowly - reuse for 30 minutes
def cached_week():
    return get_week_forecast()


def temp(value):
    """Format a temperature, or a dash if the forecast is missing it."""
    return "–" if value is None else f"{value:.0f}°"


# ---------- Today ----------
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

# ---------- 7-day forecast ----------
st.divider()
st.subheader("7-day forecast")
week = cached_week()

if week is None:
    st.info("The 7-day forecast isn't available right now.")
else:
    cols = st.columns(len(week))
    for col, day in zip(cols, week):
        d = date.fromisoformat(day["date"])
        day_season = season_for_date(d, seasons)
        with col, st.container(border=True):
            st.markdown(f"**{'Today' if d == today else d.strftime('%a')}**")
            st.caption(d.strftime("%d %b"))
            st.markdown(f"{temp(day['max_temp'])} / {temp(day['min_temp'])}")
            rain = day["rain_mm"]
            st.caption("🌧 –" if rain is None else f"🌧 {rain:.1f} mm")
            if day_season["name"] != season["name"]:
                st.caption(f"→ {day_season['name']}")   # week crosses into a new season

        # Line chart of the week's max and min
    df = pd.DataFrame(week)
    df["date"] = pd.to_datetime(df["date"])
    df["day"] = df["date"].dt.strftime("%a %d")          # e.g. "Thu 08"
    long = df.melt(id_vars=["date", "day"], value_vars=["max_temp", "min_temp"],
                   var_name="Measure", value_name="Temp")
    long["Measure"] = long["Measure"].map({"max_temp": "Max", "min_temp": "Min"})

    chart = alt.Chart(long).mark_line(point=True).encode(
        x=alt.X("day:O", title=None, sort=list(df["day"]), axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Temp:Q", title=None, scale=alt.Scale(zero=False),
                axis=alt.Axis(labelExpr="datum.label + '°C'")),
        color=alt.Color("Measure:N", scale=alt.Scale(range=["#c44536", "#3b6ea5"])),
        tooltip=["day", "Measure", alt.Tooltip("Temp:Q", title="°C", format=".1f")],
    )
    st.altair_chart(chart, width="stretch")
    st.caption("Forecast from Open-Meteo for Perth Airport.")