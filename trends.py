import altair as alt
import pandas as pd
import streamlit as st
from ui import apply_style, banner

apply_style()
from seasons import load_seasons, load_weather, add_season_columns, yearly_series, linear_trend


@st.cache_data
def get_data():
    seasons = load_seasons("data/seasons.csv")
    weather = add_season_columns(load_weather("data/perth_daily_clean.csv"), seasons)
    return seasons, weather


seasons, weather = get_data()
MEASURES = {"Average max temp": ("max_temp_c", "°C"),
            "Average min temp": ("min_temp_c", "°C"),
            "Total rainfall": ("rainfall_mm", "mm")}

st.title("Trends")
st.caption("Explore long-term weather records at Perth Airport.")
banner("Historical weather · Bureau of Meteorology", "Is each season changing?", "Compare temperature and rainfall across seasons and years, using records from 1945 onwards.")

with st.container(border=True):
    st.subheader("Choose your comparison")
    c1, c2 = st.columns(2)
    season_name = c1.selectbox("Season", [s["name"] for s in seasons])
    measure = c2.selectbox("Measure", list(MEASURES))
    metric, unit = MEASURES[measure]
    
    first, last = int(weather["season_year"].min()), int(weather["season_year"].max())
    years = st.slider("Years", first, last, (first, last))

series = [(y, v) for y, v in yearly_series(weather, season_name, metric)
          if years[0] <= y <= years[1]]

if len(series) < 5:
    st.error("Pick a wider range of years. You need at least 5 complete seasons to show a trend.")
    st.stop()

slope, intercept = linear_trend(series)
df = pd.DataFrame(series, columns=["year", "value"])
df["trend"] = intercept + slope * df["year"]

base = alt.Chart(df).encode(x=alt.X("year:Q", axis=alt.Axis(format="d"), title=None))
line = base.mark_line(point=True, color="#176cb0").encode(
    y=alt.Y("value:Q", title=f"{measure} ({unit})", scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip("year:Q", format="d"), alt.Tooltip("value:Q", format=".1f")])
trend = base.mark_line(strokeDash=[6, 4], color="#dc8a32").encode(y="trend:Q")
with st.container(border=True):
    st.subheader(f"{season_name} · {measure}")
    st.caption("Blue: seasonal values · Orange dashed: fitted trend")
    chart = (line + trend).properties(height=340).configure_view(stroke=None).configure_axis(gridColor="#e8edf2", labelColor="#526779", titleColor="#375771")
    st.altair_chart(chart, width="stretch")

per_decade = slope * 10
m1, m2, m3 = st.columns(3)
m1.metric("Change per decade", f"{per_decade:+.2f} {unit}")
m2.metric(f"Average {years[0]}–{years[1]}", f"{df['value'].mean():.1f} {unit}")
m3.metric("Seasons included", len(df))
direction = "up" if per_decade > 0 else "down"
st.caption(f"Orange dashed line = line of best fit. {season_name} {measure.lower()} is trending "
           f"{direction} by about {abs(per_decade):.2f} {unit} per decade. "
           "Incomplete seasons at the start and end of the record are left out.")