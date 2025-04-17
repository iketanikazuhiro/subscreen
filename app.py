import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh

# 1秒ごとにリフレッシュをトリガー
_ = st_autorefresh(interval=1_000, key="clock")

st.set_page_config(page_title="Simple Clock", layout="wide")
st.markdown(
    """
    <style>
      #MainMenu, footer, header { visibility: hidden; }
      body, .stApp {
        background-color: #eee !important;
        margin: 0; padding: 0;
        width: 100vw; height: 100vh;
        overflow: hidden;
      }
      .clock {
        position: fixed;
        top: 50%;
        left: 66.667%;
        transform: translate(-50%, -50%);
        font-size: 120px;
        color: #fff;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%H:%M")
st.markdown(f'<div class="clock">{now}</div>', unsafe_allow_html=True)
