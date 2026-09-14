import datetime
import requests
import streamlit as st

st.set_page_config(
    page_title="오늘 나의 기분 체크", page_icon="☀️", layout="centered"
)

# ==============================================================================
# 🎯 구글 앱스 스크립트(GAS) 웹앱 URL (새 주소 반영)
# ==============================================================================
GAS_WEBAPP_URL = "https://script.google.com/macros/s/AKfycbyJ31BFdk6qLu5usdlxRiqKCQOWC0NFYyNAuETS8I07349yhSneSpDfBghGARBY-8lw6g/exec"
# ==============================================================================

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

if "is_saved" not in st.session_state:
    st.session_state.is_saved = False

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
    st.session_state.is_saved = False

# ------------------------------------------------------------------------------
# STEP 1: 이름 입력
# ------------------------------------------------------------------------------
if st.session_state.page == 1:
    st.title("☀️ 좋은 아침!")
    st.subheader("1단계: 이름을 입력해 주세요")

    st.session_state.name = st.text_input(
        "이름을 입력하세요:",
        value=st.session_state.name,
        placeholder="예: 홍길동",
    )

    st.divider()
    if st.button("다음 ➡️", use_container_width=True):
        if not st.session_state.name.strip():
            st.warning("이름을 입력하셔야 다음으로 이동할 수 있습니다.")
        else:
            next_page()
            st.rerun()

# ------------------------------------------------------------------------------
# STEP 2: 오늘의 기분 점수 (10점 만점)
# ------------------------------------------------------------------------------
elif st.session_state.page == 2:
    st.title(f"👋 반갑습니다, {st.session_state.name}님!")
    st.subheader(f"2단계: 오늘 기분은 10점 만점에 몇 점인가요?")

    st.session_state.score = st.slider(
        "슬라이더를 움직여 점수를 선택해 주세요:",
        min_value=1,
        max_value=10,
        value=st.session_state.score,
    )

    st.write(f"현재 선택하신 점수: **{st.session_state.score}점** / 10점")

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
# STEP 3: 기분 단어 선택 (1줄 세로 배열 & 구분 적용)
# ------------------------------------------------------------------------------
elif st.session_state.page == 3:
    st.title("💭 기분 단어 선택하기")
    st.subheader("3단계: 현재 기분에 알맞은 단어를 선택해 주세요 (다중 선택 가능)")

    pos_list = [
        "상쾌한", "포근한", "행복한", "신나는", "감사한", "후련한", "놀란",
        "개운한", "기대되는", "기운이 나는", "다정한", "든든한", "따뜻한",
        "마음이 놓이는", "만족스러운", "반가운", "뿌듯한", "흥미로운",
        "평화로운", "즐거운", "자랑스러운", "재미있는", "여유로운"
    ]

    neg_list = [
        "갑갑한", "걱정스러운", "공허한", "괴로운", "귀찮은", "난감한",
        "따분한", "막막한", "무기력한", "무서운", "민망한", "불편한",
        "떨리는", "서운한", "슬픈", "속상한", "심심한",
        "쓸쓸한", "억울한", "아쉬운"
    ]

    # 1. 긍정 감정 단어 목록 (위쪽 배치)
    for i, word in enumerate(pos_list):
        is_selected = word in st.session_state.selected_feelings
        label = f"✓ {word}" if is_selected else word
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(label, key=f"btn_p_{i}_{word}", type=btn_type, use_container_width=True):
            if is_selected:
                st.session_state.selected_feelings.remove(word)
            else:
                st.session_state.selected_feelings.append(word)
            st.rerun()

    # 긍정과 부정 단어 사이 약간의 텀(여백 및 경계선)
    st.write("")
    st.markdown("---")
    st.write("")

    # 2. 부정 감정 단어 목록 (아래쪽 배치)
    for i, word in enumerate(neg_list):
        is_selected = word in st.session_state.selected_feelings
        label = f"✓ {word}" if is_selected else word
        btn_type = "primary" if is_selected else "secondary"
        
        if st.button(label, key=f"btn_n_{i}_{word}", type=btn_type, use_container_width=True):
            if is_selected:
                st.session_state.selected_feelings.remove(word)
            else:
                st.session_state.selected_feelings.append(word)
            st.rerun()

    st.divider()
    if st.session_state.selected_feelings:
        st.info(f"선택하신 감정 단어: **{', '.join(st.session_state.selected_feelings)}**")
    else:
        st.caption("알맞은 감정 단어를 선택해 주세요.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ 이전", use_container_width=True):
            prev_page()
            st.rerun()
    with col2:
        if st.button("다음 ➡️", use_container_width=True):
            if not st.session_state.selected_feelings:
                st.warning("최소 하나 이상의 감정 단어를 선택해 주세요.")
            else:
                next_page()
                st.rerun()

# ------------------------------------------------------------------------------
# STEP 4: 이유 선택 및 주관식 입력
# ------------------------------------------------------------------------------
elif st.session_state.page == 4:
    st.title("🌱 기분의 이유 알아보기")
    st.subheader("4단계: 그런 기분이 든 이유는 무엇인가요? (여러 개 선택 가능)")

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
            btn_type = "primary" if is_selected else "secondary"
            
            if cols[idx].button(label, key=f"r_btn_{reason_item}", type=btn_type, use_container_width=True):
                if is_selected:
                    st.session_state.selected_reasons.remove(reason_item)
                else:
                    st.session_state.selected_reasons.append(reason_item)
                st.rerun()

    if st.session_state.selected_reasons:
        st.info(f"선택하신 이유: **{', '.join(st.session_state.selected_reasons)}**")

    st.markdown("#### 4-1. 이유를 조금 더 자세히 적어봅시다.")
    st.caption("💡 **선택사항:** 작성하지 않아도 괜찮습니다. 작성한 내용은 절대 비밀 보장!")
    
    st.session_state.reason_detail = st.text_area(
        "어떤 일이 있으셨는지 편안하게 작성해 주세요:",
        value=st.session_state.reason_detail,
        placeholder="예: 오늘 시험이 있어서 긴장돼요 / 오늘 친구랑 엽떡먹기로 했어요",
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
                st.warning("최소 하나 이상의 이유 항목을 선택해 주세요.")
            else:
                next_page()
                st.rerun()

# ------------------------------------------------------------------------------
# STEP 5 부분의 데이터 전송 로직
if not st.session_state.is_saved:
    try:
        payload = {
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": st.session_state.name,
            "score": st.session_state.score,
            "feelings": ", ".join(st.session_state.selected_feelings),
            "reasons": ", ".join(st.session_state.selected_reasons),
            "detail": st.session_state.reason_detail,
        }
        
        # headers와 allow_redirects 옵션 추가
        headers = {"Content-Type": "application/json"}
        response = requests.post(GAS_WEBAPP_URL, json=payload, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            st.session_state.is_saved = True
    except Exception as e:
        st.error(f"구글 시트 저장 실패: {e}")

    st.title("💖 응원 메시지")
    st.write("")
    
    name = st.session_state.name
    st.success(f"### 💕 오늘도 행복한 하루~!")

    st.divider()
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        restart()
        st.rerun()
