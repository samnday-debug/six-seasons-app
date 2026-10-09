from datetime import date, datetime
from zoneinfo import ZoneInfo
import altair as alt
import streamlit as st
from ui import apply_style, banner
from seasons import (load_seasons, season_for_date, load_weather, add_season_columns,
                     season_summary, load_signs, other_seasons,
                     EUROPEAN_SEASONS, month_table)

apply_style()

# Richer (less pastel) colours for the season wheel
NOONGAR_COLOURS = ["#e4572e", "#b5172b", "#d49a0b", "#1d4e89", "#2a9d8f", "#7b3fa0"]
EUROPEAN_COLOURS = ["#f08a24", "#9c5a2b", "#3f6fa8", "#5b9a3c"]

# Light blue season cards, darker blue for the current season
st.markdown("""<style>
[class*="st-key-season-card"] {background:#e8f3fc; border-radius:16px;}
[class*="st-key-season-now"]  {background:#b9dbf6; border-radius:16px;}
</style>""", unsafe_allow_html=True)


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
    banner("Season details", s["name"], f"{month_range(s)} · also spelt {s['alt_name']}")
    st.write(s["description"])

    st.subheader("Average weather at Perth Airport (1945–today)", anchor=False)
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg max", f"{stats['avg_max']} °C")
    c2.metric("Avg min", f"{stats['avg_min']} °C")
    c3.metric("Avg total rain", f"{stats['avg_rain']:.0f} mm")

    st.subheader("Seasonal signs", anchor=False)
    season_signs = all_signs[all_signs["Season"] == s["name"]]
    flora = season_signs[season_signs["Type"] == "Flora"]
    fauna = season_signs[season_signs["Type"] == "Fauna"]
    tab1, tab2 = st.tabs([f"🌿 Flora ({len(flora)})", f"🦘 Fauna ({len(fauna)})"])
    with tab1:
        show_signs(flora, all_signs, s["name"])
    with tab2:
        show_signs(fauna, all_signs, s["name"])

    source = str(s.get("source") or "").strip()
    if source.lower() in {"", "none", "nan"}:
        source_label = "Seasonal references: see Sources & About"
    else:
        source_label = f"Seasonal source: {source}"
    st.caption(f"{source_label} · Weather: Bureau of Meteorology")


seasons, summary, signs = get_data()
today = datetime.now(ZoneInfo("Australia/Perth")).date()
current = season_for_date(today, seasons)
order = [s["name"] for s in seasons]

# ---------- 1. Six season boxes ----------
st.title("Season Explorer")
st.caption("Explore the six seasons, their weather and recorded plants and animals.")
banner("Current season · Perth", current["name"], month_range(current))
st.subheader("Explore a season", anchor=False)

for start in (0, 3):
    cols = st.columns(3)
    for col, s in zip(cols, seasons[start:start + 3]):
        is_current = s["name"] == current["name"]
        # The key gives each box a CSS class so we can colour it (see style above)
        box_key = f"season-now-{s['name']}" if is_current else f"season-card-{s['name']}"
        with col:
            with st.container(border=True, key=box_key):
                st.caption("CURRENT SEASON" if is_current else "NOONGAR SEASON")
                st.subheader(s["name"], anchor=False)
                st.caption(month_range(s))
                if st.button("Explore " + s["name"], key=s["name"], help=s["short"], width="stretch",
                             type="primary" if is_current else "secondary"):
                    show_season(s, summary.loc[s["name"]], signs)

# ---------- 2. Season wheel ----------
with st.container(border=True):
    st.subheader("Six Seasons vs Four Seasons?", anchor=False)
    st.write("**Outer ring:** Noongar seasons · **Inner ring:** European seasons. "
             "Hover over the wheel to compare. This month is outlined and darker.")

    months = month_table(seasons)
    this_month = alt.datum.month_num == today.month
    base = alt.Chart(months).encode(
        theta=alt.Theta("value:Q", stack=True),
        order=alt.Order("pos:Q"),
        opacity=alt.condition(this_month, alt.value(1.0), alt.value(0.75)),
        tooltip=[alt.Tooltip("month:N", title="Month"),
                 alt.Tooltip("noongar:N", title="Noongar season"),
                 alt.Tooltip("european:N", title="European season")],
    )
    outline = {"stroke": alt.condition(this_month, alt.value("#12344f"), alt.value("white")),
               "strokeWidth": alt.condition(this_month, alt.value(3), alt.value(1))}
    outer = base.mark_arc(innerRadius=120, outerRadius=180).encode(
        color=alt.Color("noongar:N", title="Noongar",
                        scale=alt.Scale(domain=order, range=NOONGAR_COLOURS)), **outline)
    inner = base.mark_arc(innerRadius=55, outerRadius=115).encode(
        color=alt.Color("european:N", title="European",
                        scale=alt.Scale(domain=list(EUROPEAN_SEASONS), range=EUROPEAN_COLOURS)),
        **outline)
    labels = base.mark_text(radius=200, fontSize=12).encode(text="month:N")
    wheel = (alt.layer(outer, inner, labels)
             .resolve_scale(color="independent")
             .properties(width=440, height=440)
             .configure_view(stroke=None))
    st.altair_chart(wheel)