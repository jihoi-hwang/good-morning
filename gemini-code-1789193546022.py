import streamlit as st

st.set_page_config(
    page_title="오늘 나의 기분 체크", page_icon="☀️", layout="centered"
)

# ------------------------------------------------------------------------------
# 세션 상태(Session State) 초기화
# ------------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "name" not in st.session_state:
    st.session_state.name = ""

if "score" not in st.session_state:
    st.session_state.score = 5

if "feeling_word" not in st.session_state:
    st.session_state.feeling_word = "상쾌한"

if "reason_cat" not in st.session_state:
    st.session_state.reason_cat = "친구"

if "reason_detail" not in st.session_state:
    st.session_state.reason_detail = ""

# ------------------------------------------------------------------------------
# 페이지 이동 함수
# ------------------------------------------------------------------------------


def next_page():
    st.session_state.page += 1


def prev_page():
    st.session_state.page -= 1


def restart():
    st.session_state.page = 1
    st.session_state.name = ""
    st.session_state.score = 5
    st.session_state.reason_detail = ""


# ------------------------------------------------------------------------------
# STEP 1: 이름 입력
# ------------------------------------------------------------------------------
if st.session_state.page == 1:
    st.title("☀️ 좋은 아침이야!")
    st.subheader("1단계: 너의 이름을 알려줘")

    st.session_state.name = st.text_input(
        "이름을 입력하세요:",
        value=st.session_state.name,
        placeholder="예: 홍길동",
    )

    st.divider()
    if st.button("다음 ➡️", use_container_width=True):
        if not st.session_state.name.strip():
            st.warning("이름을 입력해야 다음으로 넘어갈 수 있어!")
        else:
            next_page()
            st.rerun()

# ------------------------------------------------------------------------------
# STEP 2: 오늘의 기분 점수 (10점 만점)
# ------------------------------------------------------------------------------
elif st.session_state.page == 2:
    st.title(f"👋 안녕, {st.session_state.name}아!")
    st.subheader("2단계: 오늘 너의 기분은 10점 만점에 몇 점이야?")

    st.session_state.score = st.slider(
        "슬라이더를 움직여서 점수를 골라봐!",
        min_value=1,
        max_value=10,
        value=st.session_state.score,
    )

    st.write(f"현재 선택한 점수: **{st.session_state.score}점** / 10점")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전", use_container_width=True):
            prev_page()
            st.rerun()
    with col2:
        if st.button("다음 ➡️", use_container_width=True):
            next_page()
            st.rerun()

# ------------------------------------------------------------------------------
# STEP 3: 기분 단어 선택
# ------------------------------------------------------------------------------
elif st.session_state.page == 3:
    st.title("💭 기분 단어 고르기")
    st.subheader("3단계: 그 점수에 맞는 기분을 말로 표현해볼까?")

    feeling_options = [
        "가벼운",
        "상쾌한",
        "포근한",
        "갑갑한",
        "민망한",
        "어색한",
        "긴장이 풀리는",
        "느긋한",
    ]

    # 기존 선택값의 위치 찾기
    default_idx = (
        feeling_options.index(st.session_state.feeling_word)
        if st.session_state.feeling_word in feeling_options
        else 0
    )

    st.session_state.feeling_word = st.radio(
        "지금 네 기분에 가장 가까운 단어를 골라줘:",
        feeling_options,
        index=default_idx,
    )

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전", use_container_width=True):
            prev_page()
            st.rerun()
    with col2:
        if st.button("다음 ➡️", use_container_width=True):
            next_page()
            st.rerun()

# ------------------------------------------------------------------------------
# STEP 4: 이유 선택 및 주관식 입력
# ------------------------------------------------------------------------------
elif st.session_state.page == 4:
    st.title("🌱 기분의 이유 알아보기")
    st.subheader("4단계: 그런 기분이 든 이유가 뭐야?")

    reason_options = ["친구", "가족", "돈", "공부, 학업", "기타"]
    default_r_idx = (
        reason_options.index(st.session_state.reason_cat)
        if st.session_state.reason_cat in reason_options
        else 0
    )

    st.session_state.reason_cat = st.selectbox(
        "가장 큰 이유를 선택해줘:", reason_options, index=default_r_idx
    )

    st.markdown("#### 4-1. 이유를 조금 더 자세히 적어볼까?")
    st.session_state.reason_detail = st.text_area(
        "어떤 일이 있었는지 마음 편하게 자유롭게 써봐! (선택사항)",
        value=st.session_state.reason_detail,
        placeholder="예: 오늘 단어 시험이 있어서 긴장돼요 / 친구랑 맛있는 걸 먹기로 했어요",
    )

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전", use_container_width=True):
            prev_page()
            st.rerun()
    with col2:
        if st.button("결과 보기 ✨", use_container_width=True):
            next_page()
            st.rerun()

# ------------------------------------------------------------------------------
# STEP 5: 맞춤 응원 메시지 페이지
# ------------------------------------------------------------------------------
elif st.session_state.page == 5:
    st.title("🌈 오늘의 응원 메시지")

    name = st.session_state.name
    score = st.session_state.score
    feeling = st.session_state.feeling_word
    reason = st.session_state.reason_cat
    detail = st.session_state.reason_detail

    # 1. 기분 상태 요약
    st.info(
        f"**{name}**이의 오늘 기분 점수는 **{score}점**! (**{feeling}** 기분)"
    )

    # 2. 이유별 긍정 메시지 생성 로직
    st.markdown("### 💌 너를 위한 오늘의 한마디")

    if reason == "공부, 학업":
        msg = f"✨ **{reason}** 때문에 신경이 쓰이는구나? 걱정마, **{name}아, 넌 뭐든지 해낼 수 있어!** 작은 발걸음부터 차근차근 해보자!"
    elif reason == "친구":
        msg = f"🤝 **{reason}**에 관한 일은 언제나 커다랗게 느껴지지. 하지만 그 어떤 것도 **{name}**이 너의 소중한 가치를 바꾸진 않아!"
    elif reason == "가족":
        msg = f"🏡 **{reason}**은 언제나 네 곁에 있는 가장 든든한 울타리야. 오늘 하루도 힘차게 시작해봐!"
    elif reason == "돈":
        msg = f"용돈이나 **{reason}**에 대한 고민이 있구나! 하지만 **{name}**이의 오늘 하루는 무엇과도 바꿀 수 없이 소중해!"
    else:  # 기타
        msg = f"🌈 어떤 이유든 괜찮아! **{name}**이의 오늘은 새로운 시작이야. 힘내서 멋진 하루 만들어보자!"

    # 점수가 높은 경우 추가 응원
    if score >= 7:
        st.success(
            f"{msg}\n\n오늘 기분이 최고네! 이 멋진 에너지로 주변 친구들에게도 밝은 기운을 전달해줘! 😆"
        )
    # 점수가 다소 낮은 경우 따뜻한 위로
    elif score <= 4:
        st.warning(
            f"{msg}\n\n오늘 기분이 조금 다운되어 있구나. 괜찮아, 마음이 그럴 수도 있지. 너무 부담 갖지 말고 편안한 마음으로 시작해보자 🌿"
        )
    else:
        st.success(msg)

    # 주관식 작성 내용 복기
    if detail.strip():
        st.markdown(f"> 💬 **네가 남긴 마음 소리:** *\"{detail}\"*")

    st.divider()
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        restart()
        st.rerun()