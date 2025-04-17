# app.py
import streamlit as st
from datetime import datetime
import time

# ① ページ設定
st.set_page_config(page_title="Simple Clock", layout="wide")

# ② Streamlit デフォルトのヘッダー・フッターを非表示に
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

# ③ fullscreen フラグの初期化
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

# ④ 全画面ボタン（押されていなければ表示）
if not st.session_state.fullscreen:
    if st.button("Fullscreen"):
        st.session_state.fullscreen = True

# ⑤ 全画面表示のトリガー
if st.session_state.fullscreen:
    st.markdown(
        """
        <script>
          document.documentElement.requestFullscreen();
        </script>
        """,
        unsafe_allow_html=True,
    )

# ⑥ デジタル時計の描画
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

# ⑦ 1分ごとに更新して再実行
time.sleep(60)
st.experimental_rerun()
