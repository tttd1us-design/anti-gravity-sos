"""안전 계층 - 진단하지 않고, 판단하지 않고, 연결한다.
원문은 저장하지 않으며 감지 수준과 시각만 기록한다.
"""
from __future__ import annotations

_ELEVATED = ["의미없", "의미 없", "지쳤", "지친", "다 포기", "포기하고싶", "무기력",
             "아무것도 하고 싶지", "쓸모없", "쓸모 없", "쓸데없는 사람",
             "내가 싫", "혐오", "버티기 힘들", "숨이 막"]
_HIGH = ["사라지고 싶", "없어지고 싶", "죽고 싶", "살고 싶지 않", "끝내고 싶",
         "더는 못 견디", "아무도 필요 없"]


def screen(text: str | None) -> str:
    """NONE | ELEVATED | HIGH. 규칙 기반 1차 필터."""
    if not text:
        return "NONE"
    t = text.replace(" ", "")
    if any(k.replace(" ", "") in t for k in _HIGH):
        return "HIGH"
    if any(k.replace(" ", "") in t for k in _ELEVATED):
        return "ELEVATED"
    return "NONE"


def response(level: str) -> dict | None:
    if level == "NONE":
        return None
    if level == "ELEVATED":
        return {
            "mode": "SUPPORT",
            "title": "잠깐 실험을 멈출게요",
            "body": ("적어주신 걸 보니 지금은 시작 방법을 찾는 문제가 아닌 것 같아요. "
                     "이 앱은 행동 실험을 기록하는 도구예요. 마음이 무거운 상태 자체를 "
                     "다루는 건 제 역할이 아니고, 그건 사람에게 이야기할 때 훨씬 나아져요."),
            "suggestions": ["가까운 사람에게 오늘 얘기 한 번 꺼내보기",
                            "괜찮아지지 않으면 상담 한 번 받아보기"],
            "resources": [],
            "suppress_experiments": True,
        }
    return {
        "mode": "SUPPORT",
        "title": "지금은 실험보다 사람이 필요해요",
        "body": ("힘든 마음을 적어주셔서 고마워요. 그 얘기는 제가 아니라 "
                 "훈련받은 사람에게 하는 게 맞아요. 지금 바로 연결할 수 있는 곳이 있어요."),
        "suggestions": ["지금 통화 가능한 곳에 한 번 연락해보기"],
        "resources": [
            {"name": "자살예방 상담전화", "contact": "109", "note": "24시간"},
            {"name": "정신건강 상담전화", "contact": "1577-0199", "note": "24시간"},
        ],
        "suppress_experiments": True,
    }


DISCLAIMER = ("이 앱은 행동 실험 기록 도구입니다. 심리 진단이나 치료를 제공하지 않으며, "
              "발견된 '법칙'은 당신의 기록에서 계산된 통계일 뿐 의학적 판단이 아닙니다.")
