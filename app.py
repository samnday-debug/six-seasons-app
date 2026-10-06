import streamlit as st

st.set_page_config(page_title="Six Seasons", page_icon="🌿", layout="wide")

pages = [
    st.Page("views/today.py", title="Today", icon="📅", default=True),
]
st.navigation(pages).run()