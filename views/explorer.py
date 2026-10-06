from datetime import date, datetime
from zoneinfo import ZoneInfo
import altair as alt
import streamlit as st
from seasons import (load_seasons, season_for_date, load_weather, add_season_columns,
                     season_summary, load_signs, other_seasons,
                     EUROPEAN_SEASONS, month_table)

NOONGAR_COLOURS = ["#e8833a", "#c44536", "#c9a227", "#3b6ea5", "#5a9e6f", "#b5739d"]
EUROPEAN_COLOURS = ["#f2b134", "#a3664d", "#6c8ebf", "#8cc084"]


@st.cache_data
def get_data():
    seasons = load_seasons("data/seasons.csv")
    weather = add_season_columns(load_weather("data/perth_daily_clean.csv"), seasons)
    signs = load_signs("data/seasonal_signs.csv", seasons)
    return seasons, season_summary(weather), signs


def month_range(s):
    first = date(2000, s["months"][0], 1).strftime("%B")
    last = date(2000, s["months"][-1], 1).strftime("%B")
    return f"{first} – {last}"


def show_signs(rows, all_signs, season_name):
    """One card per plant/animal."""
    if rows.empty:
        st.write("No entries recorded for this season yet.")
        return
    for _, r in rows.iterrows():
        title = f"**{r['Noongar name'] or r['Common name']}**"
        if r["Noongar name"]:
            title += f" — {r['Common name']}"
        if r["Scientific name"]:
            title += f" (*{r['Scientific name']}*)"
        with st.container(border=True):
            st.markdown(title)
            st.write(r["Why it is associated with the season"] or "No description recorded yet.")
            extras = []
            if r["Association type"]:
                extras.append(r["Association type"])
            also = other_seasons(all_signs, r["Scientific name"], season_name)
            if also:
                extras.append("Also in: " + ", ".join(also))
            if extras:
                st.caption(" · ".join(extras))


@st.dialog("Season details", width="large")
def show_season(s, stats, all_signs):
    st.header(s["name"])
    st.caption(f"{month_range(s)} · also spelt {s['alt_name']}")
    st.write(s["description"])

    st.subheader("Average weather at Perth Airport (1945–today)")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg max", f"{stats['avg_max']} °C")
    c2.metric("Avg min", f"{stats['avg_min']} °C")
    c3.metric("Avg total rain", f"{stats['avg_rain']:.0f} mm")

    st.subheader("Seasonal signs")
    season_signs = all_signs[all_signs["Season"] == s["name"]]
    flora = season_signs[season_signs["Type"] == "Flora"]
    fauna = season_signs[season_signs["Type"] == "Fauna"]
    tab1, tab2 = st.tabs([f"🌿 Flora ({len(flora)})", f"🦘 Fauna ({len(fauna)})"])
    with tab1:
        show_signs(flora, all_signs, s["name"])
    with tab2:
        show_signs(fauna, all_signs, s["name"])

    st.caption(f"Source: {s['source']} · Weather: Bureau of Meteorology")


seasons, summary, signs = get_data()
today = datetime.now(ZoneInfo("Australia/Perth")).date()
current = season_for_date(today, seasons)
order = [s["name"] for s in seasons]

# ---------- 1. Six season boxes ----------
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
            show_season(s, summary.loc[s["name"]], signs)

# ---------- 2. Season wheel ----------
st.divider()
st.subheader("Six seasons vs four")
st.write("**Outer ring:** Noongar seasons · **Inner ring:** European seasons. "
         "Hover over the wheel to compare. This month is highlighted.")

months = month_table(seasons)
highlight = alt.condition(alt.datum.month_num == today.month, alt.value(1.0), alt.value(0.45))
base = alt.Chart(months).encode(
    theta=alt.Theta("value:Q", stack=True),
    order=alt.Order("pos:Q"),
    opacity=highlight,
    tooltip=[alt.Tooltip("month:N", title="Month"),
             alt.Tooltip("noongar:N", title="Noongar season"),
             alt.Tooltip("european:N", title="European season")],
)
outer = base.mark_arc(innerRadius=120, outerRadius=180, stroke="white").encode(
    color=alt.Color("noongar:N", title="Noongar",
                    scale=alt.Scale(domain=order, range=NOONGAR_COLOURS)))
inner = base.mark_arc(innerRadius=55, outerRadius=115, stroke="white").encode(
    color=alt.Color("european:N", title="European",
                    scale=alt.Scale(domain=list(EUROPEAN_SEASONS), range=EUROPEAN_COLOURS)))
labels = base.mark_text(radius=200, fontSize=12).encode(text="month:N")
wheel = (alt.layer(outer, inner, labels)
         .resolve_scale(color="independent")
         .properties(width=440, height=440))
st.altair_chart(wheel)

# ---------- 3. Seasonal signs chart ----------
st.divider()
st.subheader("Plants and animals recorded for each season")
counts = signs.groupby(["Season", "Type"]).size().reset_index(name="Count")
chart = alt.Chart(counts).mark_bar().encode(
    x=alt.X("Season:N", sort=order, title=None, axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Count:Q", title="Number recorded"),
    color=alt.Color("Type:N", scale=alt.Scale(range=["#4c9a5f", "#c8743a"])),
    xOffset="Type:N",
    tooltip=["Season", "Type", "Count"],
)
st.altair_chart(chart, width="stretch")
st.caption("Based on our seasonal signs dataset. Fewer entries means less was recorded "
           "in our sources, not that fewer species are present.")