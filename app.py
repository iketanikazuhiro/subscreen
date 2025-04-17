# app.py
import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ① ページ設定
st.set_page_config(page_title="Simple Clock", layout="wide")

# ② Streamlit のデフォルト UI を隠しつつ、背景色を薄いグレーに
st.markdown(
    """
    <style>
      /* メニューやフッターなどを非表示 */
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      /* ページ全体の背景色 */
      body, .stApp {
        background-color: #eee !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ③ フルスクリーン制御用のセッションステート
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

# ④ フルスクリーンボタン（押されたら状態をセット）
if not st.session_state.fullscreen:
    if st.button("Fullscreen"):
        st.session_state.fullscreen = True

# ⑤ フルスクリーン処理（状態が True なら JS で切り替え）
if st.session_state.fullscreen:
    st.markdown(
        """
        <script>
          document.documentElement.requestFullscreen();
        </script>
        """,
        unsafe_allow_html=True,
    )

# ⑥ 1 分ごとに自動更新
_ = st_autorefresh(interval=60_000, key="clock_refresh")

# ⑦ デジタル時計描画（フォントサイズを60pxに）
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
      <span style="
        font-size: 60px;
        color: #111;
      ">{now}</span>
    </div>
    """,
    unsafe_allow_html=True,
)
