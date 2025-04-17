# app.py
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# ページ設定
st.set_page_config(page_title="Simple Clock", layout="wide")

# CSS：UI 隠蔽＋背景色＋時計スタイル
st.markdown(
    """
    <style>
      /* メニューやフッターを非表示 */
      #MainMenu, footer, header { visibility: hidden; }

      /* 背景を薄いグレーに */
      body, .stApp {
        background-color: #eee !important;
        margin: 0; padding: 0;
        width: 100vw; height: 100vh;
        overflow: hidden;
      }

      /* 時計表示 */
      .clock {
        position: absolute;
        top: 50%;
        left: 66.667%; /* 画面右側1/3位置 */
        transform: translate(-50%, -50%);
        font-size: 120px;
        color: #fff;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 現在時刻を日本標準時で取得・表示
now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%H:%M")
st.markdown(f'<div class="clock">{now}</div>', unsafe_allow_html=True)

# 60秒ごとにリロード
st.markdown(
    """
    <script>
      setTimeout(() => { window.location.reload(); }, 60000);
    </script>
    """,
    unsafe_allow_html=True,
)
