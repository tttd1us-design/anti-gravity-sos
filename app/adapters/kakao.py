"""
3분 실험실 - 카카오톡 오픈빌더(Kakao i Builder) 스킬 웹훅 어댑터 & 대화 상태머신(FSM)
설계 원칙:
1. 앱 설치 마찰을 없애고 카카오톡 대화창에서 아침 실험 카드와 저녁 관찰 기록을 100% 처리한다.
2. 버튼 1클릭으로 사다리 조절, 관찰 기록, 사용설명서 법칙 승인을 완료한다.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models import User, Experiment, Rule, Outcome, RuleStatus
from app.core import ladder as ladder_mod, designer, miner, sos, safety, manual as manual_mod


class KakaoResponseBuilder:
    """카카오톡 i-Builder 스킬 응답 포맷 빌더"""

    @staticmethod
    def simple_text(text: str, quick_replies: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        res: Dict[str, Any] = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"simpleText": {"text": text}}
                ]
            }
        }
        if quick_replies:
            res["template"]["quickReplies"] = [
                {"label": qr["label"], "action": "message", "messageText": qr["text"]}
                for qr in quick_replies
            ]
        return res

    @staticmethod
    def basic_card(title: str, description: str, buttons: Optional[List[Dict[str, str]]] = None, quick_replies: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        card: Dict[str, Any] = {
            "title": title,
            "description": description
        }
        if buttons:
            card["buttons"] = [
                {"action": "message", "label": b["label"], "messageText": b["text"]}
                for b in buttons
            ]

        res: Dict[str, Any] = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {"basicCard": card}
                ]
            }
        }
        if quick_replies:
            res["template"]["quickReplies"] = [
                {"label": qr["label"], "action": "message", "messageText": qr["text"]}
                for qr in quick_replies
            ]
        return res


def get_or_create_kakao_user(db: Session, kakao_user_id: str, nickname: str = "연구자") -> User:
    user = db.scalar(select(User).where(User.id == kakao_user_id))
    if not user:
        user = User(id=kakao_user_id, nickname=nickname, consent_emotion_log=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def handle_kakao_message(db: Session, payload: Dict[str, Any]) -> Dict[str, Any]:
    """카카오 i-Builder 스킬 웹훅 진입점"""
    user_key = payload.get("userRequest", {}).get("user", {}).get("id", "kakao_test_user")
    user_msg = payload.get("userRequest", {}).get("utterance", "").strip()

    user = get_or_create_kakao_user(db, user_key)
    recent = list(db.scalars(
        select(Experiment).where(Experiment.user_id == user.id)
        .order_by(desc(Experiment.created_at)).limit(30)
    ))

    # 1. 안전 스크리닝 (위기 표현 감지)
    safety_level = safety.screen(user_msg)
    if safety_level != "NONE":
        sos.activate(user)
        db.commit()
        resp = safety.response(safety_level)
        return KakaoResponseBuilder.simple_text(
            f"{resp['title']}\n\n{resp['body']}\n\n" + "\n".join([f"· {r['name']} ({r['contact']})" for r in resp.get('resources', [])])
        )

    # 2. 비상착륙 상태 확인
    triggered, reason = sos.should_trigger(user, recent)
    if triggered:
        if reason != "active":
            sos.activate(user)
            db.commit()
        card_data = sos.card(reason)
        return KakaoResponseBuilder.basic_card(
            title=card_data["title"],
            description=f"{card_data['body']}\n\n오늘의 유일한 미션:\n- " + "\n- ".join(card_data["missions"]) + f"\n\n{card_data['footer']}",
            quick_replies=[
                {"label": "알겠어요", "text": "비상착륙 확인"},
                {"label": "작은 거 하나 할래요", "text": "실험 재개"}
            ]
        )

    # 3. 비상착륙 재개 요청
    if user_msg == "실험 재개":
        user.sos_until = None
        db.commit()
        return KakaoResponseBuilder.simple_text(
            "가장 작은 것 하나부터 시작할게요. 오늘 하려다 멈춘 과제를 한 줄로 적어주세요.",
            quick_replies=[{"label": "보고서 쓰기", "text": "보고서 쓰기"}, {"label": "공부하기", "text": "공부하기"}]
        )

    # 4. 사용설명서 열람 요청
    if "사용설명서" in user_msg or "내 비법서" in user_msg:
        rules = list(db.scalars(select(Rule).where(Rule.user_id == user.id).order_by(Rule.user_confirmed_at)))
        m = manual_mod.build(rules, user.nickname)
        text = f"📕 {user.nickname} 님의 사용설명서 ({m['progress']['found']}/{m['progress']['total']})\n\n"
        if m["confirmed"]:
            text += "✅ 확정된 법칙:\n" + "\n".join([f"{c['no']} {c['statement']}\n({c['evidence']})" for c in m["confirmed"]])
        else:
            text += "아직 확정된 법칙이 없어요. 관찰 기록이 쌓이면 자동으로 발견됩니다."
        return KakaoResponseBuilder.simple_text(text, quick_replies=[{"label": "오늘의 실험 하기", "text": "새 실험 시작"}])

    # 5. 관찰 기록 처리
    last_exp = recent[0] if recent else None
    if last_exp and not last_exp.outcome:
        # 사다리 크기 조절 명령어 처리
        if user_msg in ["더 작게", "너무 부담돼요"]:
            new_lv = max(0, last_exp.ladder_level - 1)
            steps = ladder_mod.build_ladder(last_exp.task_text, last_exp.task_type)
            last_exp.ladder_level = new_lv
            last_exp.ladder_step_text = steps[new_lv]["text"]
            last_exp.planned_minutes = steps[new_lv]["minutes"]
            db.commit()
            return KakaoResponseBuilder.basic_card(
                title=f"🪜 사다리 하향: {steps[new_lv]['label']}",
                description=f"행동: {steps[new_lv]['text']} ({steps[new_lv]['minutes']}분)\n\n부담을 낮추는 것도 중요한 데이터입니다.",
                quick_replies=[
                    {"label": "⏱️ 이 크기로 시작", "text": "실험 시작"},
                    {"label": "더 작게", "text": "더 작게"} if new_lv > 0 else {"label": "실험 시작", "text": "실험 시작"}
                ]
            )

        if user_msg == "실험 시작":
            return KakaoResponseBuilder.simple_text(
                f"⏱️ 3분 타이머가 시작되었습니다!\n\n과제: {last_exp.ladder_step_text}\n\n시간이 끝나면 아래 버튼을 눌러 무슨 일이 있었는지 알려주세요.",
                quick_replies=[{"label": "🔬 관찰 기록하기", "text": "관찰 기록"}]
            )

        if user_msg == "관찰 기록":
            return KakaoResponseBuilder.simple_text(
                "무슨 일이 일어났나요? (어떤 답이든 유효한 데이터입니다)",
                quick_replies=[
                    {"label": "🛑 시작도 못 함", "text": "시작도 못 함"},
                    {"label": "⏸️ 시작했다 멈춤", "text": "시작했다 멈춤"},
                    {"label": "✅ 3분 완수", "text": "3분 완수"},
                    {"label": "🚀 3분 넘게 함", "text": "3분 넘게 함"}
                ]
            )

        outcome_map = {
            "시작도 못 함": Outcome.NOT_STARTED,
            "시작했다 멈춤": Outcome.STARTED_STOPPED,
            "3분 완수": Outcome.DID_MINIMUM,
            "3분 넘게 함": Outcome.WENT_LONGER
        }
        if user_msg in outcome_map:
            last_exp.outcome = outcome_map[user_msg]
            last_exp.observed_at = datetime.utcnow()
            db.commit()

            feedback = {
                Outcome.NOT_STARTED: "기록해주셔서 고마워요. 시작 못 한 것도 중요한 관찰이에요. 벌 대신 새로운 발견의 데이터가 됩니다.",
                Outcome.STARTED_STOPPED: "시작했다는 게 핵심이에요. 멈춘 지점이 다음 실험의 힌트예요.",
                Outcome.DID_MINIMUM: "계획한 만큼 하셨네요. 이 조합은 기록해둘 만해요.",
                Outcome.WENT_LONGER: "계획보다 더 하셨어요! 시작 크기가 잘 맞았다는 신호예요."
            }[last_exp.outcome]

            # 채굴 가설 탐색
            exps = list(db.scalars(select(Experiment).where(Experiment.user_id == user.id).limit(200)))
            findings = miner.mine(exps)
            if findings:
                f = findings[0]
                return KakaoResponseBuilder.basic_card(
                    title="🔬 기록 완료 & 새로운 가설 발견!",
                    description=f"{feedback}\n\n💡 혹시 이런 걸까요?\n\"{f['statement']}\"\n(근거: {f['evidence_n']}회 관찰)",
                    quick_replies=[
                        {"label": "맞아요", "text": f"가설승인_{f['dimension']}_{f['dim_value']}"},
                        {"label": "아니에요", "text": "가설거절"},
                        {"label": "더 볼래요", "text": "가설보류"}
                    ]
                )

            return KakaoResponseBuilder.simple_text(
                f"{feedback}\n\n(누적 관찰 {len([e for e in exps if e.outcome])}회 완료)",
                quick_replies=[{"label": "📕 내 사용설명서 보기", "text": "사용설명서"}]
            )

    # 6. 기본: 새로운 실험 카드 발급
    task_text = user_msg if user_msg not in ["새 실험 시작", "시작"] else "보고서/과제 시작하기"
    streak = sos.not_started_streak(recent)
    hyps = list(db.scalars(select(Rule).where(Rule.user_id == user.id, Rule.status.in_([RuleStatus.HYPOTHESIS, RuleStatus.TESTING]))))
    
    card_info = designer.design_experiment(
        task_text=task_text,
        experiment_no=len(recent) + 1,
        open_hypotheses=hyps,
        tried_counts={},
        not_started_streak=streak
    )

    suggested = card_info["ladder"][card_info["suggested_level"]]
    exp = Experiment(
        user_id=user.id,
        task_text=task_text,
        task_type=card_info["task_type"],
        hypothesis_id=card_info["hypothesis_id"],
        variation_key=card_info["variation"]["key"],
        ladder_level=card_info["suggested_level"],
        ladder_step_text=suggested["text"],
        planned_minutes=suggested["minutes"],
        ctx_time_bucket="morning" if 8 <= datetime.utcnow().hour < 12 else "night"
    )
    db.add(exp)
    db.commit()

    return KakaoResponseBuilder.basic_card(
        title=f"🧪 실험 #{card_info['experiment_no']} · {card_info['variation']['name']}",
        description=f"가설: {card_info['hypothesis_line']}\n\n검증 행동:\n👉 {suggested['text']} ({suggested['minutes']}분)\n\n방법: {card_info['variation']['howto']}",
        quick_replies=[
            {"label": "⏱️ 실험 시작", "text": "실험 시작"},
            {"label": "🪜 너무 부담돼요 (더 작게)", "text": "더 작게"}
        ]
    )
