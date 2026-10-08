"""Shared visual styling for the weather and season pages."""
from html import escape
import streamlit as st


def apply_style():
    st.markdown('''<style>
[data-testid="stMainBlockContainer"]{padding-top:2.5rem;padding-bottom:3rem}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:16px!important;border-color:#dce5ee!important}
[data-testid="stMetric"]{background:linear-gradient(120deg,#edf7ff,#f5faff);border:1px solid #dce9f4;border-radius:14px;padding:18px;color:#153653}
[data-testid="stMetricLabel"]{color:#375771}
.stButton button{border-radius:12px;border-color:#d7e3ee;min-height:48px}
.stButton button[kind="primary"]{background:#176cb0;border-color:#176cb0;color:white}
.stButton button:hover{border-color:#176cb0;color:#176cb0;background:#edf7ff}
.stButton button[kind="primary"]:hover{color:white;background:#125c97}
[data-baseweb="tab-highlight"]{background:#176cb0}
button[role="tab"][aria-selected="true"]{color:#176cb0}
.season-banner{background:linear-gradient(115deg,#c8eaff,#9acffa);border-radius:18px;padding:24px 28px;margin:8px 0 24px;color:#12344f}
.season-banner .eyebrow{font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.season-banner h2{font-size:30px;margin:0 0 8px;color:#12344f}
.season-banner p{margin:0;font-size:16px;line-height:1.5}
@media(max-width:700px){[data-testid="stMainBlockContainer"]{padding-top:1.5rem}.season-banner{padding:20px}.season-banner h2{font-size:25px}}
</style>''', unsafe_allow_html=True)


def banner(eyebrow, title, description):
    st.markdown(f'<section class="season-banner"><div class="eyebrow">{escape(eyebrow)}</div><h2>{escape(title)}</h2><p>{escape(description)}</p></section>', unsafe_allow_html=True)
