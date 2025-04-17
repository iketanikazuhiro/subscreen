# app.py
import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ① ページ設定
st.set_page_config(page_title="Simple Clock", layout="wide")

# ② UI をすっきり隠す
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ③ 全画面モード管理
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

if not st.session_state.fullscreen:
    if st.button("Fullscreen"):
        st.session_state.fullscreen = True

if st.session_state.fullscreen:
    st.markdown(
        """
        <script>
          document.documentElement.requestFullscreen();
        </script>
        """,
        unsafe_allow_html=True,
    )

# ④ 1分ごとに自動リフレッシュ
_ = st_autorefresh(interval=60_000, key="clock_refresh")

# ⑤ デジタル時計を右端に表示
now = datetime.now().strftime("%H:%M")
st.markdown(
    f"""
    <div style="
        display: flex;
        justify-content: flex-end;
        align-items: center;
        height: 100vh;
        margin: 0;
        background-color: #ccc;
    ">
      <div style="font-size:20px; color:#111;">
        {now}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
