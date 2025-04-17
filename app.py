# app.py
import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# ① ページ設定
st.set_page_config(page_title="Simple Clock", layout="wide")

# ② CSS：UI隠蔽＋背景＆レイアウト
st.markdown(
    """
    <style>
      /* メニューやフッターなどを非表示 */
      #MainMenu, footer, header {visibility: hidden;}

      /* 全体背景とコンテナ設定 */
      body, .stApp {
        background-color: #eee !important;
        margin: 0; padding: 0;
        position: relative;
        width: 100vw; height: 100vh;
        overflow: hidden;
      }

      /* フルスクリーンボタン */
      #fullscreen-btn {
        position: absolute;
        top: 10px; left: 10px;
        z-index: 1000;
      }

      /* 時計表示 */
      .clock {
        position: absolute;
        top: 50%;
        left: 66.667%;
        transform: translate(-50%, -50%);
        font-size: 60px;
        color: #111;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ③ フルスクリーン管理用セッションステート
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

# ④ フルスクリーンボタン（未押下時のみ表示）
if not st.session_state.fullscreen:
    if st.button("Fullscreen", key="fs", help="Enter fullscreen"):
        st.session_state.fullscreen = True
        # ⑤ フルスクリーン切替
        st.markdown(
            """
            <script>
              document.documentElement.requestFullscreen();
            </script>
            """,
            unsafe_allow_html=True,
        )

# ⑥ 時計表示（日本標準時）
now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%H:%M")
st.markdown(f'<div class="clock">{now}</div>', unsafe_allow_html=True)

# ⑦ 60秒ごとにページ全体をリロード（JS）
st.markdown(
    """
    <script>
      setTimeout(() => { window.location.reload(); }, 60000);
    </script>
    """,
    unsafe_allow_html=True,
)
