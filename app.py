# app.py

import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh

# ────────────────────────────────────────
# １．必ずスクリプトの最初に呼ぶ
st.set_page_config(page_title="Simple Clock", layout="wide")
# ────────────────────────────────────────

# ２．自動リフレッシュ（1秒ごとに再実行）
_ = st_autorefresh(interval=1_000, key="clock_refresh")

# ３．CSS で UI 隠蔽＋背景色＋時計スタイル定義
st.markdown(
    """
    <style>
      /* メニュー・ヘッダー・フッターを非表示 */
      #MainMenu, header, footer { visibility: hidden; }

      /* 背景を薄グレーに */
      body, .stApp {
        background-color: #eee !important;
        margin: 0; padding: 0;
        width: 100vw; height: 100vh;
        overflow: hidden;
      }

      /* 時計表示：固定配置で縦横中央、横は右1/3 */
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

# ４．現在時刻を日本標準時で取得・表示
now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%H:%M")
st.markdown(f'<div class="clock">{now}</div>', unsafe_allow_html=True)
