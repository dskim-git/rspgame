import random

import streamlit as st


st.set_page_config(
    page_title="가위바위보 챌린지",
    page_icon="✊",
    layout="centered",
)

# 깔끔하고 재미있는 화면을 위한 간단한 CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7ff 0%, #fff5f8 100%);
    }

    .main-title {
        text-align: center;
        color: #342a63;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        text-align: center;
        color: #68627e;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }

    .result-card {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid #e8e4f5;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(52, 42, 99, 0.08);
        margin-top: 1rem;
    }

    .choice {
        font-size: 1.25rem;
        color: #342a63;
        margin: 0.6rem 0;
    }

    .result {
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 1rem;
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

st.markdown(
    '<div class="main-title">✊ 가위바위보 챌린지</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">컴퓨터와 한 판 대결해 봐요! 원하는 패를 골라주세요 👇</div>',
    unsafe_allow_html=True,
)

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
        result_color = "#6c63a8"
        st.session_state["wins"] = st.session_state.get("wins", 0)
        st.session_state["losses"] = st.session_state.get("losses", 0)
        st.session_state["draws"] = st.session_state.get("draws", 0) + 1
    elif (
        (user_choice == "가위" and computer_choice == "보")
        or (user_choice == "바위" and computer_choice == "가위")
        or (user_choice == "보" and computer_choice == "바위")
    ):
        result_text = "승리!"
        result_emoji = "🎉"
        result_color = "#198754"
        st.session_state["wins"] = st.session_state.get("wins", 0) + 1
        st.session_state["losses"] = st.session_state.get("losses", 0)
        st.session_state["draws"] = st.session_state.get("draws", 0)
    else:
        result_text = "패배!"
        result_emoji = "🥲"
        result_color = "#dc3545"
        st.session_state["wins"] = st.session_state.get("wins", 0)
        st.session_state["losses"] = st.session_state.get("losses", 0) + 1
        st.session_state["draws"] = st.session_state.get("draws", 0)

    st.session_state["last_round"] = {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result_text": result_text,
        "result_emoji": result_emoji,
        "result_color": result_color,
    }

if "last_round" in st.session_state:
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

wins = st.session_state.get("wins", 0)
draws = st.session_state.get("draws", 0)
losses = st.session_state.get("losses", 0)

score_cols = st.columns(3)
score_cols[0].metric("승리 🎉", wins)
score_cols[1].metric("무승부 🤝", draws)
score_cols[2].metric("패배 🥲", losses)

if st.button("전적 초기화 🔄", use_container_width=True):
    st.session_state["wins"] = 0
    st.session_state["draws"] = 0
    st.session_state["losses"] = 0
    st.session_state.pop("last_round", None)
    st.rerun()

st.caption("한 판 더 도전하고 오늘의 승리를 쌓아보세요! 🍀")
