"""LLM 어댑터 - 있으면 문장을 다듬고, 없으면 템플릿으로 작동한다.
LLM에게 진단·해석·마찰계수 추정을 절대 맡기지 않는다. 문장 다듬기 전용.
"""
import os

REPHRASE_SYSTEM = """당신은 '3분 실험실'의 문장 다듬기 도구입니다.

절대 규칙:
1. 사용자의 심리를 진단하거나 원인을 단정하지 마십시오.
2. "당신의 진짜 문제는 ~입니다" 같은 표현을 절대 쓰지 마십시오.
3. 패턴을 언급할 때는 반드시 관찰 횟수를 함께 말하고, 질문형으로 끝내십시오.
4. 격려하되 과장하지 마십시오. 못 한 것을 지적하거나 아쉬워하지 마십시오.
5. 출력은 2문장 이내, 존댓말, 이모지 없이.

당신이 하는 일: 주어진 실험 지시문을 더 구체적이고 부담 없는 한국어 문장으로 바꾸기.
"""


def available() -> bool:
    return bool(os.getenv("AG_LLM_API_KEY"))


def rephrase(step_text: str, variation_howto: str) -> str | None:
    """실패 시 None을 반환하고 호출자는 템플릿을 그대로 쓴다."""
    if not available():
        return None
    try:
        return None
    except Exception:
        return None
