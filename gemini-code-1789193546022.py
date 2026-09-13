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

if "selected_feelings" not in st.session_state:
    st.session_state.selected_feelings = []

if "selected_reasons" not in st.session_state:
    st.session_state.selected_reasons = []

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
    st.session_state.selected_feelings = []
    st.session_state.selected_reasons = []
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
        placeholder="예: 길동이",
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
    st.subheader(f"2단계: 오늘 {st.session_state.name}의 기분은 10점 만점에 몇 점이야?")

    st.session_state.score = st.slider(
        "슬라이더를 움직여서 점수를 골라보세요!",
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
# STEP 3: 기분 단어 선택 (모바일 2열 강제 고정 - HTML multiselect)
# ------------------------------------------------------------------------------
elif st.session_state.page == 3:
    st.title("💭 기분 단어 고르기")
    st.subheader("3단계: 그 점수에 맞는 기분을 말로 표현해봅시다! (여러 개 선택 가능)")

    # 긍정 감정 (30개)
    pos_list = [
        "가벼운", "상쾌한", "포근한", "행복한", "신나는", "감사한",
        "개운한", "기대되는", "기운이 나는", "다정한", "든든한", "따뜻한",
        "마음이 놓이는", "만족스러운", "명랑한", "반가운", "뿌듯한", "산뜻한",
        "평화로운", "즐거운", "자랑스러운", "재미있는", "영광스러운", "여유로운",
        "후련한", "흥미로운", "활기가 넘치는", "놀란", "궁금한", "느긋한"
    ]

    # 부정 감정 (22개)
    neg_list = [
        "갑갑한", "걱정스러운", "공허한", "괴로운", "귀찮은", "난감한",
        "따분한", "막막한", "무기력한", "무서운", "민망한", "불편한",
        "떨리는", "서운한", "섭섭한", "슬픈", "속상한", "심심한",
        "쓸쓸한", "억울한", "아쉬운", "멍한"
    ]

    # 모바일에서도 절대 무너지지 않는 2열 체크박스 그리드 CSS
    st.markdown(
        """
        
        """,
        unsafe_allow_html=True,
    )

    # st.multiselect를 활용하여 모바일에서 확실하게 2열로 선택할 수 있게 배치
    col_p, col_n = st.columns(2)
    with col_p:
        selected_pos = st.multiselect(
            "긍정 감정",
            pos_list,
            default=[w for w in st.session_state.selected_feelings if w in pos_list]
        )
    with col_n:
        selected_neg = st.multiselect(
            "부정 감정",
            neg_list,
            default=[w for w in st.session_state.selected_feelings if w in neg_list]
        )

    # 선택된 단어 상태 업데이트
    st.session_state.selected_feelings = selected_pos + selected_neg

    st.divider()
    if st.session_state.selected_feelings:
        st.info(f"선택한 감정 단어: **{', '.join(st.session_state.selected_feelings)}**")
    else:
        st.caption("알맞은 감정 단어를 선택해줘!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전", use_container_width=True):
            prev_page()
            st.rerun()
    with col2:
        if st.button("다음 ➡️", use_container_width=True):
            if not st.session_state.selected_feelings:
                st.warning("최소 하나 이상의 감정 단어를 선택해줘!")
            else:
                next_page()
                st.rerun()

# ------------------------------------------------------------------------------
# STEP 4: 이유 선택 및 주관식 입력
# ------------------------------------------------------------------------------
elif st.session_state.page == 4:
    st.title("🌱 기분의 이유 알아보기")
    st.subheader("4단계: 그런 기분이 든 이유가 뭐야? (여러 개 선택 가능)")

    reason_rows = [
        ["친구", "선생님"],
        ["부모님", "학업/공부/학원"],
        ["학교", "기타"]
    ]

    for row in reason_rows:
        cols = st.columns(2)
        for idx, reason_item in enumerate(row):
            is_selected = reason_item in st.session_state.selected_reasons
            label = f"✅ {reason_item}" if is_selected else reason_item
            
            if cols[idx].button(label, key=f"r_btn_{reason_item}", use_container_width=True):
                if is_selected:
                    st.session_state.selected_reasons.remove(reason_item)
                else:
                    st.session_state.selected_reasons.append(reason_item)
                st.rerun()

    if st.session_state.selected_reasons:
        st.info(f"선택한 이유: **{', '.join(st.session_state.selected_reasons)}**")

    st.markdown("#### 4-1. 이유를 조금 더 자세히 적어봅시다.")
    st.caption("💡 **선택사항:** 안 쓰고 싶으면 안 써도 됩니다. 쓴 내용은 절대비밀보장!")
    
    st.session_state.reason_detail = st.text_area(
        "어떤 일이 있었는지 마음 편하게 작성해줘 (안 적어도 괜찮아):",
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
            if not st.session_state.selected_reasons:
                st.warning("최소 하나 이상의 이유 항목을 선택해주세요!")
            else:
                next_page()
                st.rerun()

# ------------------------------------------------------------------------------
# STEP 5: 최종 메시지 페이지
# ------------------------------------------------------------------------------
elif st.session_state.page == 5:
    st.balloons()
    
    st.title("💖 응원 메시지")
    st.write("")
    
    name = st.session_state.name
    st.success(f"### 🎉 {name}아! 오늘도 좋은 하루 보내!")

    st.divider()
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        restart()
        st.rerun()
