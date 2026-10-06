import streamlit as st

st.set_page_config(page_title="Six Seasons", page_icon="🌿", layout="wide")

pages = [
    st.Page("views/today.py", title="Today", icon="📅", default=True),
    st.Page("views/explorer.py", title="Season Explorer", icon="🌿"),
    st.Page("views/trends.py", title="Trends", icon="📈"),
    st.Page("views/sources.py", title="Sources & About", icon="📚"),
]
st.navigation(pages, position="sidebar").run()