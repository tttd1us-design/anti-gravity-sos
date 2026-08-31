"""비상착륙 서킷브레이커 - 방법 문제가 아니라 연료 문제일 때 실험을 멈춘다."""
from __future__ import annotations
from datetime import datetime, timedelta, date

from app.models import Experiment, Outcome, User

SILENCE_DAYS = 3
NOT_STARTED_STREAK = 3
SOS_DAYS = 2


def not_started_streak(recent: list[Experiment]) -> int:
    """최신순 정렬 입력. 연속 미착수 횟수."""
    n = 0
    for e in recent:
        if e.outcome == Outcome.NOT_STARTED:
            n += 1
        elif e.outcome in (None, Outcome.NO_RESPONSE):
            continue
        else:
            break
    return n


def should_trigger(user: User, recent: list[Experiment]) -> tuple[bool, str]:
    if user.sos_until and user.sos_until >= date.today():
        return True, "active"
    if not_started_streak(recent) >= NOT_STARTED_STREAK:
        return True, "streak"
    observed = [e for e in recent if e.observed_at]
    if observed:
        gap = datetime.utcnow() - observed[0].observed_at
        if gap > timedelta(days=SILENCE_DAYS):
            return True, "silence"
    return False, ""


def activate(user: User) -> None:
    user.sos_until = date.today() + timedelta(days=SOS_DAYS)


def card(reason: str) -> dict:
    if reason == "silence":
        body = "며칠 조용했네요. 확인하려고 온 거 아니에요. 그냥 자리 지키고 있었어요."
    elif reason == "streak":
        body = "데이터 보니까 지금은 방법 문제가 아니라 연료 문제예요."
    else:
        body = "아직 착륙 중이에요. 천천히 하세요."
    return {
        "mode": "SOS",
        "title": "🛬 비상착륙 모드",
        "body": body,
        "missions": ["물 한 잔 마시기", "7시간 자기"],
        "footer": "실험은 잠시 멈춰둘게요. 비법서는 그대로 있어요. 없어지지 않아요.",
        "actions": [
            {"key": "ack", "label": "알겠어요"},
            {"key": "resume", "label": "그래도 아주 작은 거 하나 할래요"},
        ],
    }
