"""행동 사다리 - 과제를 5단계 크기로 제시하고 선택권을 사용자에게 넘긴다.
AI가 마찰계수를 '추측'하지 않는다. 사용자의 선택이 곧 측정값이다.
"""
from __future__ import annotations

TASK_TYPES = {
    "WRITING":  ["글", "원고", "보고서", "리포트", "논문", "블로그", "책", "기획서", "제안서", "일기", "메일작성"],
    "STUDY":    ["공부", "인강", "강의", "문제집", "시험", "암기", "복습", "예습", "단어", "기출"],
    "EXERCISE": ["운동", "헬스", "스쿼트", "러닝", "달리기", "산책", "요가", "스트레칭", "홈트", "등산"],
    "CHORE":    ["청소", "설거지", "빨래", "정리", "분리수거", "치우", "정돈", "설거"],
    "CONTACT":  ["전화", "연락", "답장", "메일", "문의", "카톡", "예약", "상담신청"],
    "ADMIN":    ["서류", "신청", "정산", "세금", "계약", "제출", "결산", "청구"],
    "CREATIVE": ["디자인", "영상", "편집", "그림", "코딩", "개발", "작곡", "촬영", "썸네일"],
}

PERFECTION_WORDS = ["완벽", "제대로", "완성", "끝내", "다 ", "전부", "모두", "깔끔하게", "잘 "]

# level: (라벨, 분, 유형별 문장 템플릿)
_STEPS: dict[str, list[str]] = {
    "WRITING": [
        "{t} 파일/노트만 열고 바로 닫기",
        "{t} 제목 한 줄만 쓰기",
        "{t} 목차나 소제목만 적기",
        "{t} 아무 단락 하나만 쓰기",
        "{t} 원래 계획대로 하기",
    ],
    "STUDY": [
        "{t} 교재/영상만 켜고 바로 덮기",
        "{t} 첫 문제 하나만 읽기",
        "{t} 한 페이지만 훑기",
        "{t} 한 단원 절반만 하기",
        "{t} 원래 계획대로 하기",
    ],
    "EXERCISE": [
        "{t} 운동복만 갈아입기",
        "{t} 1세트만 / 3분만 하기",
        "{t} 절반 분량만 하기",
        "{t} 계획의 70%만 하기",
        "{t} 원래 계획대로 하기",
    ],
    "CHORE": [
        "{t} 하려는 곳 앞에 가서 서 있기",
        "{t} 3분 타이머 켜고 손에 잡히는 것만",
        "{t} 한 구역만 하기",
        "{t} 절반만 하기",
        "{t} 원래 계획대로 하기",
    ],
    "CONTACT": [
        "{t} 연락처/메일창만 열기",
        "{t} 첫 문장만 써두고 보내지 않기",
        "{t} 초안 다 쓰고 보내지 않기",
        "{t} 보내기",
        "{t} 원래 계획대로 하기",
    ],
    "ADMIN": [
        "{t} 필요한 서류 이름만 검색하기",
        "{t} 양식만 다운로드하기",
        "{t} 이름/날짜 칸만 채우기",
        "{t} 절반만 작성하기",
        "{t} 원래 계획대로 하기",
    ],
    "CREATIVE": [
        "{t} 작업 파일만 열기",
        "{t} 아무 요소 하나만 배치하기",
        "{t} 초안 스케치만 하기",
        "{t} 한 파트만 완성하기",
        "{t} 원래 계획대로 하기",
    ],
    "GENERIC": [
        "{t} 하는 자리에 가서 앉기",
        "{t} 3분 타이머 켜고 아무거나 손대기",
        "{t} 가장 쉬운 부분만 하기",
        "{t} 절반만 하기",
        "{t} 원래 계획대로 하기",
    ],
}

_MINUTES = [0.5, 3.0, 10.0, 25.0, 45.0]
_LABELS = ["열기만", "3분만", "10분만", "25분", "원래대로"]


def detect_task_type(task_text: str) -> str:
    low = task_text.replace(" ", "")
    for ttype, kws in TASK_TYPES.items():
        if any(k.replace(" ", "") in low for k in kws):
            return ttype
    return "GENERIC"


def has_perfection_word(task_text: str) -> bool:
    return any(w in task_text for w in PERFECTION_WORDS)


def _short(task_text: str, limit: int = 24) -> str:
    t = task_text.strip()
    return t if len(t) <= limit else t[:limit] + "…"


def build_ladder(task_text: str, task_type: str | None = None) -> list[dict]:
    """5단 사다리 생성. 0=가장 작음, 4=원래 크기."""
    ttype = task_type or detect_task_type(task_text)
    tmpl = _STEPS.get(ttype, _STEPS["GENERIC"])
    short = _short(task_text)
    return [
        {
            "level": i,
            "label": _LABELS[i],
            "minutes": _MINUTES[i],
            "text": tmpl[i].format(t=short),
        }
        for i in range(5)
    ]


def default_level(recent_not_started_streak: int) -> int:
    """제안 시작 단계. 최근 미착수가 반복될수록 더 낮은 곳에서 시작한다.
    이건 예측이 아니라 배려다. 사용자는 언제든 위/아래로 바꿀 수 있다.
    """
    if recent_not_started_streak >= 2:
        return 0
    if recent_not_started_streak == 1:
        return 1
    return 1
