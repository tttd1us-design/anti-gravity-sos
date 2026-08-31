"""실험 설계자 - 매일 다른 실험을, 그러나 무작위가 아니라 정보이득 순으로.
선택 규칙: 검증 대기 가설이 있으면 그것을 겨냥한 변주를, 없으면 가장 덜 시도한 변주를.
"""
from __future__ import annotations
import random

from app.core.ladder import build_ladder, detect_task_type, default_level

# tests: 이 변주가 어떤 차원의 가설을 검증하는가
VARIATIONS: list[dict] = [
    {"key": "PLAIN", "name": "그냥 3분", "tests": "size",
     "howto": "군더더기 없이 3분 타이머만 켜고 시작합니다."},
    {"key": "WORST_DRAFT", "name": "일부러 최악으로", "tests": "perfection",
     "howto": "'형편없이 하기'가 목표입니다. 잘하려고 하면 규칙 위반입니다."},
    {"key": "HARD_STOP", "name": "3분 되면 강제 종료", "tests": "perfection",
     "howto": "더 하고 싶어도 무조건 멈춥니다. 아쉬움을 남기는 게 목적입니다."},
    {"key": "NINETY_SEC", "name": "90초로 줄이기", "tests": "size",
     "howto": "3분도 부담이면 90초. 실패가 물리적으로 불가능한 크기입니다."},
    {"key": "STAND_UP", "name": "서서 하기", "tests": "place",
     "howto": "앉지 않고 서서 진행합니다. 자세가 시작에 영향을 주는지 봅니다."},
    {"key": "PHONE_AWAY", "name": "휴대폰 다른 방에", "tests": "place",
     "howto": "시작 전 휴대폰을 물리적으로 다른 공간에 둡니다."},
    {"key": "DECLARE", "name": "먼저 선언하고 하기", "tests": "social",
     "howto": "시작 직전 한 사람에게 '지금 3분 한다'고 알립니다."},
    {"key": "SILENT", "name": "아무에게도 말 안 하고", "tests": "social",
     "howto": "누구에게도 알리지 않고 혼자 조용히 진행합니다."},
    {"key": "REVERSE", "name": "뒷부분부터 하기", "tests": "approach",
     "howto": "처음이 아니라 마지막 부분이나 쉬운 부분부터 손댑니다."},
    {"key": "PRECOMMIT", "name": "시작 시각 미리 못박기", "tests": "time_bucket",
     "howto": "지금 시작 시각을 정하고 알람을 걸어둡니다. 알람이 울리면 무조건 시작."},
    {"key": "MOVE_EARLY", "name": "평소보다 이른 시간에", "tests": "time_bucket",
     "howto": "평소 하던 시간보다 앞당겨 진행합니다."},
    {"key": "TWO_MIN_WALK", "name": "2분 걷고 시작", "tests": "energy",
     "howto": "시작 전 2분간 걷거나 몸을 움직인 뒤 착수합니다."},
]

_BY_DIM: dict[str, list[dict]] = {}
for _v in VARIATIONS:
    _BY_DIM.setdefault(_v["tests"], []).append(_v)


def pick_variation(open_hypotheses: list, tried_counts: dict[str, int]) -> dict:
    """정보이득 우선. 검증 대기 가설의 차원을 겨냥하되, 같은 변주 반복은 피한다."""
    candidates: list[dict] = []
    for h in open_hypotheses:
        candidates.extend(_BY_DIM.get(h.dimension, []))
    if not candidates:
        candidates = VARIATIONS  # 탐색 모드: 아직 가설이 없으면 넓게 훑는다

    least = min(tried_counts.get(c["key"], 0) for c in candidates)
    pool = [c for c in candidates if tried_counts.get(c["key"], 0) == least]
    return random.choice(pool)


def design_experiment(
    task_text: str,
    experiment_no: int,
    open_hypotheses: list,
    tried_counts: dict[str, int],
    not_started_streak: int,
) -> dict:
    """오늘의 실험 카드 데이터 생성."""
    ttype = detect_task_type(task_text)
    variation = pick_variation(open_hypotheses, tried_counts)
    ladder = build_ladder(task_text, ttype)
    level = default_level(not_started_streak)

    target = open_hypotheses[0] if open_hypotheses else None
    if target:
        hypothesis_line = target.statement
        evidence_line = f"지금까지 {target.evidence_n}번 관찰됐어요. 더 확인해볼까요?"
        hypothesis_id = target.id
    else:
        hypothesis_line = "아직 당신에 대해 아는 게 없어요. 오늘은 탐색 실험입니다."
        evidence_line = "관찰이 5번 쌓이면 첫 패턴을 찾아볼 수 있어요."
        hypothesis_id = None

    return {
        "experiment_no": experiment_no,
        "task_text": task_text,
        "task_type": ttype,
        "hypothesis_id": hypothesis_id,
        "hypothesis_line": hypothesis_line,
        "evidence_line": evidence_line,
        "variation": variation,
        "ladder": ladder,
        "suggested_level": level,
    }
