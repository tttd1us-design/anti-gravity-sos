"""사용설명서 렌더링 + 공유 카드. 산출물이 곧 획득 채널이다."""
from __future__ import annotations

from app.models import Rule, RuleStatus

TOTAL_SLOTS = 30


def build(rules: list[Rule], nickname: str) -> dict:
    confirmed = [r for r in rules if r.status == RuleStatus.CONFIRMED]
    testing = [r for r in rules if r.status in (RuleStatus.HYPOTHESIS, RuleStatus.TESTING)]
    return {
        "title": f"📕 {nickname} 님의 사용설명서",
        "progress": {"found": len(confirmed), "total": TOTAL_SLOTS,
                     "locked": max(0, TOTAL_SLOTS - len(confirmed) - len(testing))},
        "confirmed": [
            {"no": f"#{i:02d}", "statement": r.statement,
             "evidence": f"실험 {r.evidence_n}회 · 해당 상황 {round(r.rate*100)}% / 평소 {round(r.baseline*100)}%",
             "rule_id": r.id}
            for i, r in enumerate(confirmed, start=1)
        ],
        "testing": [
            {"statement": r.statement, "evidence": f"{r.evidence_n}회 관찰 중", "rule_id": r.id}
            for r in testing
        ],
        "disclaimer_required": True,
    }


def to_markdown(manual: dict) -> str:
    lines = [f"# {manual['title']}", "",
             f"발견 {manual['progress']['found']}/{manual['progress']['total']}", ""]
    lines.append("## 확정된 법칙")
    for c in manual["confirmed"] or []:
        lines += [f"**{c['no']} {c['statement']}**", f"  - 근거: {c['evidence']}", ""]
    if not manual["confirmed"]:
        lines += ["아직 없어요. 관찰이 쌓이면 여기 채워집니다.", ""]
    if manual["testing"]:
        lines.append("## 검증 중인 가설")
        for t in manual["testing"]:
            lines.append(f"- {t['statement']} ({t['evidence']})")
    return "\n".join(lines)


def share_card(rule: Rule, nickname: str) -> dict:
    return {
        "headline": f"나의 사용설명서",
        "statement": rule.statement,
        "proof": f"실험 {rule.evidence_n}회로 알아냄",
        "byline": f"— {nickname}",
        "caption": "성격 테스트로 나온 게 아니라, 내가 실제로 한 걸로 알아냈습니다.",
    }
