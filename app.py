# app.py
import streamlit as st
from datetime import datetime

# ① ページ設定
st.set_page_config(page_title="Simple Clock", layout="wide")

# ② デフォルト UI を隠し、背景を薄グレーに
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      body, .stApp {
        background-color: #eee !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ③ フルスクリーン制御
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

# ④ JS で 60秒後にページをリロード
st.markdown(
    """
    <script>
      setTimeout(() => { window.location.reload(); }, 60000);
    </script>
    """,
    unsafe_allow_html=True,
)

# ⑤ 時計表示（フォントサイズ60px）
now = datetime.now().strftime("%H:%M")
st.markdown(
    f"""
    <div style="
        display: flex;
        justify-content: flex-end;
        align-items: center;
        height: 100vh;
        margin: 0;
    ">
      <span style="font-size:60px; color:#111;">
        {now}
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)
