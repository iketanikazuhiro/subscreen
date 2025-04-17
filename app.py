# app.py

import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh

# ───────────────────────────────────────────────────────
# 1. ページ設定は必ず最初に
st.set_page_config(page_title="Clock & Timer Suite", layout="wide")
# ───────────────────────────────────────────────────────

# 2. 自動リフレッシュ（1秒ごとに再実行）
_ = st_autorefresh(interval=1_000, key="refresh")

# 3. 共通 CSS：UI 非表示＋背景色＋配置＋タブアクティブ調整
st.markdown(
    """
    <style>
      /* メニュー・ヘッダー・フッターを非表示 */
      #MainMenu, header, footer { visibility: hidden; }

      /* 背景を薄グレーに */
      body, .stApp {
        background-color: #eee !important;
        margin: 0; padding: 0;
        width: 100vw; height: 100vh; overflow: hidden;
      }

      /* tab-list 内のタブラベル表示 */
      [data-baseweb="tab-list"] [role="tab"] > div:first-child {
        color: inherit;
        font-weight: normal;
      }
      /* アクティブタブの文字色を黒・太字に */
      [data-baseweb="tab-list"] [role="tab"][aria-selected="true"] > div:first-child {
        color: #000 !important;
        font-weight: 700 !important;
      }

      /* 時計表示：固定配置で縦中央・横は右1/3 */
      .clock {
        position: fixed;
        top: 50%;
        left: 66.667%;
        transform: translate(-50%, -50%);
        color: #fff;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# 4. 終了通知用スクリプト（画面フラッシュ + ビープ音）
flash_and_beep = """
<script>
  document.body.style.backgroundColor = "#fff";
  setTimeout(() => { document.body.style.backgroundColor = "#eee"; }, 150);
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const o = ctx.createOscillator();
  o.frequency.value = 440;
  o.connect(ctx.destination);
  o.start();
  setTimeout(() => { o.stop(); }, 200);
</script>
"""

# 5. モード切替タブ（Stopwatch を除外）
tabs = st.tabs(["Clock", "Timer", "Pomodoro"])
now = datetime.now(ZoneInfo("Asia/Tokyo"))

# ───────────────────────────────────────────────────────
# ▽ Clock モード
with tabs[0]:
    current_time = now.strftime("%H:%M")
    st.markdown(
        f'<div class="clock" style="font-size:120px;">{current_time}</div>',
        unsafe_allow_html=True,
    )

# ───────────────────────────────────────────────────────
# ▽ Timer モード
with tabs[1]:
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
        st.session_state.timer_running = False
        st.session_state.timer_remaining = 0
        st.session_state.timer_finished = False

    # 時間入力
    if not st.session_state.timer_end:
        h = st.number_input("Hours", min_value=0, max_value=23, value=0, key="ti_h")
        m = st.number_input("Minutes", min_value=0, max_value=59, value=1, key="ti_m")
        s = st.number_input("Seconds", min_value=0, max_value=59, value=0, key="ti_s")
        if st.button("Start", key="ti_start"):
            total = h * 3600 + m * 60 + s
            if total > 0:
                st.session_state.timer_end = now + timedelta(seconds=total)
                st.session_state.timer_running = True
                st.session_state.timer_finished = False

    # カウントダウンフェーズ
    else:
        if st.session_state.timer_running:
            remaining = st.session_state.timer_end - now
        else:
            remaining = timedelta(seconds=st.session_state.timer_remaining)

        if remaining.total_seconds() <= 0:
            if not st.session_state.timer_finished:
                st.markdown(flash_and_beep, unsafe_allow_html=True)
                st.session_state.timer_finished = True
                st.session_state.timer_running = False
            disp = "00:00:00"
        else:
            disp = str(remaining).split(".")[0]

        # 残り時間を大きく表示
        st.markdown(
            f'<div class="clock" style="font-size:120px;">{disp}</div>',
            unsafe_allow_html=True,
        )

        # 操作ボタン
        c1, c2 = st.columns(2)
        if c1.button("Pause", key="ti_pause") and st.session_state.timer_running:
            st.session_state.timer_remaining = remaining.total_seconds()
            st.session_state.timer_running = False
        if c2.button("Reset", key="ti_reset"):
            for k in ["timer_end", "timer_running", "timer_finished"]:
                st.session_state[k] = None if k=="timer_end" else False

        if (not st.session_state.timer_running
            and st.session_state.timer_remaining > 0
            and not st.session_state.timer_finished
            and c1.button("Resume", key="ti_resume")):
            st.session_state.timer_end = now + timedelta(seconds=st.session_state.timer_remaining)
            st.session_state.timer_running = True

# ───────────────────────────────────────────────────────
# ▽ Pomodoro モード
with tabs[2]:
    if "pomo_phase" not in st.session_state:
        st.session_state.pomo_phase = None
        st.session_state.pomo_end = None
        st.session_state.pomo_running = False
        st.session_state.pomo_finished = False
        st.session_state.pomo_remaining = 0

    # 開始ボタン
    if not st.session_state.pomo_end:
        if st.button("Start Pomodoro", key="po_start"):
            st.session_state.pomo_phase = "work"
            st.session_state.pomo_end = now + timedelta(minutes=25)
            st.session_state.pomo_running = True
            st.session_state.pomo_finished = False

    else:
        if st.session_state.pomo_running:
            remaining = st.session_state.pomo_end - now
        else:
            remaining = timedelta(seconds=st.session_state.pomo_remaining)

        if remaining.total_seconds() <= 0:
            if not st.session_state.pomo_finished:
                st.markdown(flash_and_beep, unsafe_allow_html=True)
                st.session_state.pomo_finished = True
                st.session_state.pomo_running = False

                # フェーズ切替
                if st.session_state.pomo_phase == "work":
                    st.session_state.pomo_phase = "break"
                    st.session_state.pomo_end = now + timedelta(minutes=5)
                else:
                    st.session_state.pomo_phase = "work"
                    st.session_state.pomo_end = now + timedelta(minutes=25)
                st.session_state.pomo_running = True
                st.session_state.pomo_finished = False
            disp = "00:00:00"
        else:
            disp = str(remaining).split(".")[0]

        # ラベルと時間を表示（ラベルは40pxに）
        label = "Work" if st.session_state.pomo_phase == "work" else "Break"
        st.markdown(
            f'''
            <div class="clock">
              <span style="font-size:40px;">{label}</span>
              <span style="font-size:120px; margin-left:10px;">{disp}</span>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        # 操作ボタン
        c1, c2 = st.columns(2)
        if c1.button("Pause", key="po_pause") and st.session_state.pomo_running:
            st.session_state.pomo_remaining = remaining.total_seconds()
            st.session_state.pomo_running = False
        if c2.button("Reset", key="po_reset"):
            for k in ["pomo_phase","pomo_end","pomo_running","pomo_finished"]:
                st.session_state[k] = None if k=="pomo_phase" else False

        if (not st.session_state.pomo_running
            and st.session_state.pomo_remaining > 0
            and not st.session_state.pomo_finished
            and c1.button("Resume", key="po_resume")):
            st.session_state.pomo_end = now + timedelta(seconds=st.session_state.pomo_remaining)
            st.session_state.pomo_running = True
