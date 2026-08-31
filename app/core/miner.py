"""법칙 채굴 - 정직한 집단 비교. 유의성 흉내를 내지 않고 표본수를 그대로 노출한다.
채굴 결과는 항상 '가설'이며, 사용자가 확정하지 않으면 비법서에 오르지 않는다.
"""
from __future__ import annotations
from collections import defaultdict

from app.models import Experiment, Outcome, STARTED_OUTCOMES

MIN_SAMPLE = 5          # 이보다 적으면 아무 말도 하지 않는다
EFFECT_THRESHOLD = 0.25  # 베이스라인 대비 착수율 차이
MIN_TOTAL = 8            # 전체 관찰이 이만큼 쌓여야 채굴 시작

DIMENSIONS = {
    "time_bucket": lambda e: e.ctx_time_bucket,
    "energy": lambda e: str(e.ctx_energy) if e.ctx_energy else None,
    "place": lambda e: e.ctx_place,
    "perfection": lambda e: "포함" if e.ctx_perfection_word else "미포함",
    "size": lambda e: f"L{e.ladder_level}",
    "task_type": lambda e: e.task_type,
    "social": lambda e: e.variation_key if e.variation_key in ("DECLARE", "SILENT") else None,
    "approach": lambda e: e.variation_key if e.variation_key in ("REVERSE", "HARD_STOP") else None,
}

_TIME_LABEL = {"dawn": "새벽(5~8시)", "morning": "오전(8~12시)", "afternoon": "오후(12~17시)",
               "evening": "저녁(17~21시)", "night": "밤(21시 이후)"}
_SIZE_LABEL = {"L0": "'열기만' 크기로", "L1": "'3분만' 크기로", "L2": "'10분만' 크기로",
               "L3": "'25분' 크기로", "L4": "원래 크기로"}


def _phrase(dimension: str, value: str, direction: str) -> str:
    verb = "시작할 확률이 높다" if direction == "up" else "시작하지 못한다"
    if dimension == "time_bucket":
        return f"나는 {_TIME_LABEL.get(value, value)}에 {verb}"
    if dimension == "energy":
        return f"나는 컨디션을 {value}점으로 느낄 때 {verb}"
    if dimension == "place":
        return f"나는 {value}에서 {verb}"
    if dimension == "perfection":
        if value == "포함":
            return "나는 '완벽하게/제대로' 같은 말이 붙은 일을 " + ("시작한다" if direction == "up" else "미룬다")
        return f"나는 표현이 느슨한 일을 {verb}"
    if dimension == "size":
        return f"나는 과제를 {_SIZE_LABEL.get(value, value)} 쪼갤 때 {verb}"
    if dimension == "task_type":
        return f"나는 '{value}' 종류의 일을 {verb}"
    if dimension == "social":
        return ("나는 먼저 선언하면 " if value == "DECLARE" else "나는 아무에게도 말하지 않으면 ") + verb
    if dimension == "approach":
        return ("나는 뒷부분부터 손대면 " if value == "REVERSE" else "나는 강제 종료 규칙이 있으면 ") + verb
    return f"{dimension}={value} 일 때 {verb}"


def mine(experiments: list[Experiment]) -> list[dict]:
    """관찰 목록에서 가설 후보를 뽑는다."""
    obs = [e for e in experiments if e.outcome and e.outcome != Outcome.NO_RESPONSE]
    if len(obs) < MIN_TOTAL:
        return []

    baseline = sum(1 for e in obs if e.outcome in STARTED_OUTCOMES) / len(obs)
    found: list[dict] = []

    for dim, getter in DIMENSIONS.items():
        groups: dict[str, list[Experiment]] = defaultdict(list)
        for e in obs:
            v = getter(e)
            if v and v != "unknown":
                groups[v].append(e)

        for value, rows in groups.items():
            if len(rows) < MIN_SAMPLE:
                continue
            rate = sum(1 for e in rows if e.outcome in STARTED_OUTCOMES) / len(rows)
            delta = rate - baseline
            if abs(delta) < EFFECT_THRESHOLD:
                continue
            direction = "up" if delta > 0 else "down"
            found.append({
                "dimension": dim,
                "dim_value": value,
                "statement": _phrase(dim, value, direction),
                "evidence_n": len(rows),
                "rate": round(rate, 3),
                "baseline": round(baseline, 3),
                "direction": direction,
            })

    found.sort(key=lambda d: (abs(d["rate"] - d["baseline"]), d["evidence_n"]), reverse=True)
    return found
