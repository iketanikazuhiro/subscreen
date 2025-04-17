# app.py

import streamlit as st
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from streamlit_autorefresh import st_autorefresh

# ───────────────────────────────────────────────────────
# １．最初にページ設定
st.set_page_config(page_title="Clock & Timer Suite", layout="wide")
# ───────────────────────────────────────────────────────

# ２．１秒ごとに自動リフレッシュ（時刻やタイマー更新用）
_ = st_autorefresh(interval=1_000, key="refresh")

# ３．共通 CSS（UI 非表示＋背景色＋右１/３・中央配置用クラス）
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

      /* 共通：右1/3・中央配置 */
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

# ４．終了通知用スクリプト（画面フラッシュ＋ビープ音）
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

# ５．モード切替タブ
tabs = st.tabs(["Clock", "Timer", "Pomodoro", "Stopwatch"])
now = datetime.now(ZoneInfo("Asia/Tokyo"))

# ───────────────────────────────────────────────────────
# ▽ Clock モード
with tabs[0]:
    current_time = now.strftime("%H:%M")
    st.markdown(f'<div class="clock">{current_time}</div>', unsafe_allow_html=True)

# ───────────────────────────────────────────────────────
# ▽ Timer モード
with tabs[1]:
    # セッションステート初期化
    if "timer_end" not in st.session_state:
        st.session_state.timer_end = None
        st.session_state.timer_running = False
        st.session_state.timer_remaining = 0
        st.session_state.timer_finished = False

    # 入力フェーズ
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
        # 時間計算
        if st.session_state.timer_running:
            remaining = st.session_state.timer_end - now
        else:
            remaining = timedelta(seconds=st.session_state.timer_remaining)

        # 終了判定
        if remaining.total_seconds() <= 0:
            if not st.session_state.timer_finished:
                st.markdown(flash_and_beep, unsafe_allow_html=True)
                st.session_state.timer_finished = True
                st.session_state.timer_running = False
            disp = "00:00:00"
        else:
            disp = str(remaining).split(".")[0]

        # 残り時間表示
        st.markdown(f'<div class="clock">{disp}</div>', unsafe_allow_html=True)

        # 操作ボタン
        c1, c2 = st.columns(2)
        if c1.button("Pause", key="ti_pause") and st.session_state.timer_running:
            st.session_state.timer_remaining = remaining.total_seconds()
            st.session_state.timer_running = False
        if c2.button("Reset", key="ti_reset"):
            st.session_state.timer_end = None
            st.session_state.timer_running = False
            st.session_state.timer_finished = False

        # Resume ボタン（Pause 後のみ）
        if (not st.session_state.timer_running and 
            st.session_state.timer_remaining > 0 and 
            not st.session_state.timer_finished and
            c1.button("Resume", key="ti_resume")):
            st.session_state.timer_end = now + timedelta(seconds=st.session_state.timer_remaining)
            st.session_state.timer_running = True

# ───────────────────────────────────────────────────────
# ▽ Pomodoro モード
with tabs[2]:
    # 初期化
    if "pomo_phase" not in st.session_state:
        st.session_state.pomo_phase = None  # "work" or "break"
        st.session_state.pomo_end = None
        st.session_state.pomo_running = False
        st.session_state.pomo_finished = False

    # 開始ボタン
    if not st.session_state.pomo_end:
        if st.button("Start Pomodoro", key="po_start"):
            st.session_state.pomo_phase = "work"
            st.session_state.pomo_end = now + timedelta(minutes=25)
            st.session_state.pomo_running = True
            st.session_state.pomo_finished = False

    # カウントダウン
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

        # フェーズ表示
        label = "Work" if st.session_state.pomo_phase == "work" else "Break"
        st.markdown(f'<div class="clock">{label} {disp}</div>', unsafe_allow_html=True)

        # 操作ボタン
        c1, c2 = st.columns(2)
        if c1.button("Pause", key="po_pause") and st.session_state.pomo_running:
            st.session_state.pomo_remaining = remaining.total_seconds()
            st.session_state.pomo_running = False
        if c2.button("Reset", key="po_reset"):
            st.session_state.pomo_phase = None
            st.session_state.pomo_end = None
            st.session_state.pomo_running = False
            st.session_state.pomo_finished = False

        # Resume
        if (not st.session_state.pomo_running and
            st.session_state.pomo_remaining > 0 and
            not st.session_state.pomo_finished and
            c1.button("Resume", key="po_resume")):
            st.session_state.pomo_end = now + timedelta(seconds=st.session_state.pomo_remaining)
            st.session_state.pomo_running = True

# ───────────────────────────────────────────────────────
# ▽ Stopwatch モード
with tabs[3]:
    # 初期化
    if "sw_running" not in st.session_state:
        st.session_state.sw_running = False
        st.session_state.sw_start = None
        st.session_state.sw_elapsed = 0
        st.session_state.sw_laps = []

    # スタート
    if not st.session_state.sw_running and st.session_state.sw_start is None:
        if st.button("Start", key="sw_start"):
            st.session_state.sw_start = now
            st.session_state.sw_running = True

    # 計測中 or 一時停止中
    if st.session_state.sw_start:
        if st.session_state.sw_running:
            elapsed = (now - st.session_state.sw_start).total_seconds() + st.session_state.sw_elapsed
        else:
            elapsed = st.session_state.sw_elapsed

        disp = str(timedelta(seconds=int(elapsed))).split(".")[0]
        st.markdown(f'<div class="clock">{disp}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        if c1.button("Pause", key="sw_pause") and st.session_state.sw_running:
            st.session_state.sw_elapsed = elapsed
            st.session_state.sw_running = False
        if c2.button("Lap", key="sw_lap"):
            st.session_state.sw_laps.append(disp)
        if c3.button("Reset", key="sw_reset"):
            st.session_state.sw_running = False
            st.session_state.sw_start = None
            st.session_state.sw_elapsed = 0
            st.session_state.sw_laps = []

        # ラップ表示
        for i, lap in enumerate(st.session_state.sw_laps, start=1):
            st.write(f"Lap {i}: {lap}")
