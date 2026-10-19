import random

import streamlit as st


st.set_page_config(
    page_title="가위바위보 챌린지",
    page_icon="✊",
    layout="centered",
)

# 가독성이 좋은 대비 중심 다크 테마 CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }

    .main-title {
        text-align: center;
        color: #f8fafc;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .result-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 28px rgba(2, 6, 23, 0.45);
        margin-top: 1rem;
    }

    .choice {
        font-size: 1.25rem;
        color: #f1f5f9;
        margin: 0.6rem 0;
    }

    .result {
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 1rem;
    }

    /* 기본 텍스트/라벨 대비 강화 */
    .stMarkdown, .stText, .stCaption, label, p, span, div {
        color: #e2e8f0;
    }

    /* 라디오/메트릭/버튼 주변 가독성 강화 */
    .stMetricLabel, .stMetricValue {
        color: #f8fafc !important;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

CHOICES = {
    "가위": "✌️",
    "바위": "✊",
    "보": "✋",
}

# 점수와 이전 라운드 결과를 세션에 저장합니다.
if "user_score" not in st.session_state:
    st.session_state["user_score"] = 0

if "computer_score" not in st.session_state:
    st.session_state["computer_score"] = 0

if "last_round" not in st.session_state:
    st.session_state["last_round"] = None

st.markdown(
    '<div class="main-title">✊ 가위바위보 챌린지</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">컴퓨터와 한 판 대결해 봐요! 원하는 패를 골라주세요 👇</div>',
    unsafe_allow_html=True,
)

# 현재 점수를 화면 상단에서 항상 확인할 수 있습니다.
score_col1, score_col2, score_col3 = st.columns([2, 1, 2])
with score_col1:
    st.metric("🙋 사용자 점수", st.session_state["user_score"])
with score_col2:
    st.markdown(
        "<div style='text-align:center; padding-top: 1.7rem; "
        "font-size: 1.4rem; font-weight: 800; color:#f8fafc;'>:</div>",
        unsafe_allow_html=True,
    )
with score_col3:
    st.metric("🤖 컴퓨터 점수", st.session_state["computer_score"])

user_choice = st.radio(
    "당신의 선택",
    options=list(CHOICES.keys()),
    format_func=lambda choice: f"{CHOICES[choice]} {choice}",
    horizontal=True,
)

if st.button("대결하기! 🎮", use_container_width=True, type="primary"):
    computer_choice = random.choice(list(CHOICES.keys()))

    if user_choice == computer_choice:
        result_text = "무승부!"
        result_emoji = "🤝"
        result_color = "#c4b5fd"
    elif (
        (user_choice == "가위" and computer_choice == "보")
        or (user_choice == "바위" and computer_choice == "가위")
        or (user_choice == "보" and computer_choice == "바위")
    ):
        result_text = "승리!"
        result_emoji = "🎉"
        result_color = "#34d399"
        st.session_state["user_score"] += 1
    else:
        result_text = "패배!"
        result_emoji = "🥲"
        result_color = "#f87171"
        st.session_state["computer_score"] += 1

    st.session_state["last_round"] = {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result_text": result_text,
        "result_emoji": result_emoji,
        "result_color": result_color,
    }

if st.session_state["last_round"] is not None:
    round_result = st.session_state["last_round"]

    st.markdown(
        f"""
        <div class="result-card">
            <div class="choice">
                🙋 나: {CHOICES[round_result["user_choice"]]}
                <strong>{round_result["user_choice"]}</strong>
            </div>
            <div class="choice">
                🤖 컴퓨터: {CHOICES[round_result["computer_choice"]]}
                <strong>{round_result["computer_choice"]}</strong>
            </div>
            <div class="result" style="color: {round_result["result_color"]};">
                {round_result["result_emoji"]} {round_result["result_text"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### 🏆 오늘의 전적")

wins = st.session_state["user_score"]
losses = st.session_state["computer_score"]

score_cols = st.columns(2)
score_cols[0].metric("승리 🎉", wins)
score_cols[1].metric("패배 🥲", losses)

if st.button("점수 초기화 🔄", use_container_width=True):
    st.session_state["user_score"] = 0
    st.session_state["computer_score"] = 0
    st.session_state["last_round"] = None
    st.rerun()

st.caption("한 판 더 도전하고 오늘의 승리를 쌓아보세요! 🍀")
