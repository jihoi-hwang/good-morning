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

# 복수 선택을 위한 리스트 형태의 상태 관리
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
# STEP 3: 기분 단어 선택 (4열 8행 - 복수 선택 버튼)
# ------------------------------------------------------------------------------
elif st.session_state.page == 3:
    st.title("💭 기분 단어 고르기")
    st.subheader("3단계: 그 점수에 맞는 기분을 말로 표현해볼까? (여러 개 선택 가능)")

    # 4열 8행 = 총 32개 단어 (이미지 참고)
    feeling_grid = [
        ["가벼운", "상쾌한", "갑갑한", "긴장이 풀리는"],
        ["가슴뭉클한", "생기가 도는", "겁나는", "느긋한"],
        ["감격스러운", "설레는", "걱정스러운", "든든해지는"],
        ["감사한", "신나는", "불안한", "궁금한"],
        ["개운한", "싱그러운", "우울한", "긴장되는"],
        ["고마운", "여유로운", "괴로운", "지루한"],
        ["기쁜", "용기 나는", "귀찮은", "지친"],
        ["따뜻한", "즐거운", "답답한", "화나는"]
    ]

    # 네모 모양 버튼 Grid 구현
    for row in feeling_grid:
        cols = st.columns(4)
        for idx, word in enumerate(row):
            is_selected = word in st.session_state.selected_feelings
            # 선택 상태에 따라 버튼 스타일 구분 표시
            label = f"✅ {word}" if is_selected else word
            
            if cols[idx].button(label, key=f"btn_{word}", use_container_width=True):
                if is_selected:
                    st.session_state.selected_feelings.remove(word)
                else:
                    st.session_state.selected_feelings.append(word)
                st.rerun()

    if st.session_state.selected_feelings:
        st.info(f"선택한 감정 단어: **{', '.join(st.session_state.selected_feelings)}**")
    else:
        st.caption("알맞은 감정 단어를 모두 골라줘!")

    st.divider()
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
# STEP 4: 이유 선택 (한눈에 보는 4행 배치 및 복수 선택)
# ------------------------------------------------------------------------------
elif st.session_state.page == 4:
    st.title("🌱 기분의 이유 알아보기")
    st.subheader("4단계: 그런 기분이 든 이유가 뭐야? (여러 개 선택 가능)")

    # 4행 한눈에 보기 배치를 위해 구성
    reason_rows = [
        ["친구", "선생님"],
        ["부모님", "학업/공부/학원"],
        ["학교"],
        ["기타"]
    ]

    for row in reason_rows:
        cols = st.columns(len(row))
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
            if not st.session_state.selected_reasons:
                st.warning("최소 하나 이상의 이유를 선택해줘!")
            else:
                next_page()
                st.rerun()

# ------------------------------------------------------------------------------
# STEP 5: 최종 메시지 페이지
# ------------------------------------------------------------------------------
elif st.session_state.page == 5:
    st.balloons()  # 축하 애니메이션 (선택사항)
    
    st.title("💖 응원 메시지")
    st.write("")
    
    # 요청하신 메시지 출력
    name = st.session_state.name
    st.success(f"### 🎉 {name}아! 오늘도 좋은 하루 보내!")

    st.divider()
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        restart()
        st.rerun()
