from datetime import date, datetime
from zoneinfo import ZoneInfo
import streamlit as st
from seasons import load_seasons, season_for_date, load_weather, add_season_columns, season_summary


@st.cache_data
def get_data():
    seasons = load_seasons("data/seasons.csv")
    weather = add_season_columns(load_weather("data/perth_daily_clean.csv"), seasons)
    return seasons, season_summary(weather)


def month_range(s):
    first = date(2000, s["months"][0], 1).strftime("%B")
    last = date(2000, s["months"][-1], 1).strftime("%B")
    return f"{first} – {last}"


@st.dialog("Season details", width="large")
def show_season(s, stats):
    st.header(s["name"])
    st.caption(f"{month_range(s)} · also spelt {s['alt_name']}")
    st.write(s["description"])
    st.subheader("Average weather at Perth Airport (1945–today)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg max", f"{stats['avg_max']} °C")
    c2.metric("Avg min", f"{stats['avg_min']} °C")
    c3.metric("Avg total rain", f"{stats['avg_rain']:.0f} mm")
    st.caption(f"Source: {s['source']} · Weather: Bureau of Meteorology")


seasons, summary = get_data()
current = season_for_date(datetime.now(ZoneInfo("Australia/Perth")).date(), seasons)

st.title("Season Explorer")
st.write("Hover over a season for a quick summary, or click it to learn more.")

cols = st.columns(3)
for i, s in enumerate(seasons):
    with cols[i % 3]:
        label = f"**{s['name']}**  \n{month_range(s)}"
        if s["name"] == current["name"]:
            label += "  \n(now)"
        if st.button(label, key=s["name"], help=s["short"], width="stretch",
                     type="primary" if s["name"] == current["name"] else "secondary"):
            show_season(s, summary.loc[s["name"]])