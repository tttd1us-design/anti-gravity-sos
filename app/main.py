"""3분 실험실 API - 나를 실험해서 나의 사용설명서를 쓰는 앱."""
from __future__ import annotations
from datetime import datetime, date
from collections import Counter
from typing import Dict, Any

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.db import init_db, get_db
from app.models import (User, Experiment, Rule, SafetyEvent,
                        Outcome, RuleStatus)
from app.core import ladder as ladder_mod
from app.core import designer, miner, sos, safety, manual as manual_mod
from app.adapters.kakao import handle_kakao_message

app = FastAPI(title="3분 실험실 (AG Lab)", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
def _startup() -> None:
    init_db()


# ---------- 스키마 ----------
class UserCreate(BaseModel):
    nickname: str = Field(default="연구자", max_length=40)
    consent_emotion_log: bool = False


class TodayRequest(BaseModel):
    user_id: str
    task_text: str = Field(min_length=1, max_length=200)
    energy: int = Field(default=0, ge=0, le=4)
    place: str = "unknown"


class LadderChoice(BaseModel):
    level: int = Field(ge=0, le=4)


class Observation(BaseModel):
    outcome: Outcome
    minutes_actual: float | None = None
    note: str | None = Field(default=None, max_length=500)


class RuleVerdict(BaseModel):
    verdict: str  # yes | no | later


# ---------- 유틸 ----------
def _bucket(dt: datetime) -> str:
    h = dt.hour
    if 5 <= h < 8:
        return "dawn"
    if 8 <= h < 12:
        return "morning"
    if 12 <= h < 17:
        return "afternoon"
    if 17 <= h < 21:
        return "evening"
    return "night"


def _get_user(db: Session, user_id: str) -> User:
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(404, "사용자를 찾을 수 없습니다.")
    return u


def _recent(db: Session, user_id: str, limit: int = 60) -> list[Experiment]:
    return list(db.scalars(
        select(Experiment).where(Experiment.user_id == user_id)
        .order_by(desc(Experiment.created_at)).limit(limit)))


def _open_hypotheses(db: Session, user_id: str) -> list[Rule]:
    return list(db.scalars(
        select(Rule).where(Rule.user_id == user_id,
                           Rule.status.in_([RuleStatus.HYPOTHESIS, RuleStatus.TESTING]))
        .order_by(desc(Rule.evidence_n))))


# ---------- 카카오톡 i-Builder 웹훅 엔드포인트 ----------
@app.post("/api/kakao/webhook")
async def kakao_webhook(request: Request, db: Session = Depends(get_db)):
    """카카오톡 오픈빌더 스킬 웹훅 엔드포인트"""
    payload = await request.json()
    return handle_kakao_message(db, payload)


# ---------- 웹 REST 엔드포인트 ----------
@app.post("/api/users")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    u = User(nickname=payload.nickname, consent_emotion_log=payload.consent_emotion_log)
    db.add(u)
    db.commit()
    return {"user_id": u.id, "nickname": u.nickname, "disclaimer": safety.DISCLAIMER}


@app.post("/api/today")
def today(payload: TodayRequest, db: Session = Depends(get_db)):
    """아침 화면. 비상착륙 조건이면 실험 대신 착륙 카드를 준다."""
    user = _get_user(db, payload.user_id)
    recent = _recent(db, user.id)

    triggered, reason = sos.should_trigger(user, recent)
    if triggered:
        if reason != "active":
            sos.activate(user)
            db.commit()
        return sos.card(reason)

    hyps = _open_hypotheses(db, user.id)
    tried = Counter(e.variation_key for e in recent)
    streak = sos.not_started_streak(recent)
    total = len(recent)

    card = designer.design_experiment(
        task_text=payload.task_text,
        experiment_no=total + 1,
        open_hypotheses=hyps,
        tried_counts=dict(tried),
        not_started_streak=streak,
    )

    now = datetime.utcnow()
    suggested = card["ladder"][card["suggested_level"]]
    exp = Experiment(
        user_id=user.id,
        task_text=payload.task_text,
        task_type=card["task_type"],
        hypothesis_id=card["hypothesis_id"],
        variation_key=card["variation"]["key"],
        ladder_level=card["suggested_level"],
        ladder_step_text=suggested["text"],
        planned_minutes=suggested["minutes"],
        ctx_time_bucket=_bucket(now),
        ctx_energy=payload.energy,
        ctx_place=payload.place,
        ctx_is_weekend=date.today().weekday() >= 5,
        ctx_perfection_word=ladder_mod.has_perfection_word(payload.task_text),
    )
    db.add(exp)
    db.commit()

    return {"mode": "EXPERIMENT", "experiment_id": exp.id, **card}


@app.post("/api/experiments/{exp_id}/ladder")
def choose_ladder(exp_id: str, choice: LadderChoice, db: Session = Depends(get_db)):
    """사용자가 크기를 고른다. 이 선택 자체가 마찰 측정값이다."""
    exp = db.get(Experiment, exp_id)
    if not exp:
        raise HTTPException(404, "실험을 찾을 수 없습니다.")
    if exp.outcome:
        raise HTTPException(400, "이미 기록이 끝난 실험입니다.")

    steps = ladder_mod.build_ladder(exp.task_text, exp.task_type)
    step = steps[choice.level]
    exp.ladder_drops = max(0, exp.ladder_level - choice.level)
    exp.ladder_level = choice.level
    exp.ladder_step_text = step["text"]
    exp.planned_minutes = step["minutes"]
    db.commit()

    msg = "좋아요, 이 크기로 가요." if exp.ladder_drops == 0 else \
          "더 작게 잡는 것도 좋은 판단이에요. 그것도 데이터예요."
    return {"experiment_id": exp.id, "step": step, "message": msg}


@app.post("/api/experiments/{exp_id}/observe")
def observe(exp_id: str, obs: Observation, db: Session = Depends(get_db)):
    """저녁 화면. '했나요?'가 아니라 '무슨 일이 있었나요?'."""
    exp = db.get(Experiment, exp_id)
    if not exp:
        raise HTTPException(404, "실험을 찾을 수 없습니다.")
    user = _get_user(db, exp.user_id)

    level = safety.screen(obs.note)
    if level != "NONE":
        db.add(SafetyEvent(user_id=user.id, level=level))
        sos.activate(user)
        exp.outcome = obs.outcome
        exp.observed_at = datetime.utcnow()
        db.commit()
        return safety.response(level)

    exp.outcome = obs.outcome
    exp.minutes_actual = obs.minutes_actual
    if user.consent_emotion_log:
        exp.note = obs.note
    exp.observed_at = datetime.utcnow()
    db.commit()

    findings = _run_mining(db, user.id)
    return {
        "mode": "OBSERVED",
        "message": _feedback(obs.outcome),
        "new_hypotheses": findings,
        "observed_total": len([e for e in _recent(db, user.id) if e.outcome]),
    }


def _feedback(outcome: Outcome) -> str:
    return {
        Outcome.NOT_STARTED: "기록해주셔서 고마워요. 시작 못 한 것도 중요한 관찰이에요.",
        Outcome.STARTED_STOPPED: "시작했다는 게 핵심이에요. 멈춘 지점이 다음 실험의 힌트예요.",
        Outcome.DID_MINIMUM: "계획한 만큼 하셨네요. 이 조합은 기록해둘 만해요.",
        Outcome.WENT_LONGER: "계획보다 더 하셨어요. 시작 크기가 잘 맞았다는 신호예요.",
    }.get(outcome, "기록됐어요.")


def _run_mining(db: Session, user_id: str) -> list[dict]:
    """관찰 후 채굴. 이미 있는 가설은 근거만 갱신하고, 새 것은 확인 대기로 넣는다."""
    exps = _recent(db, user_id, limit=200)
    candidates = miner.mine(exps)
    existing = {(r.dimension, r.dim_value): r for r in db.scalars(
        select(Rule).where(Rule.user_id == user_id))}

    new_out: list[dict] = []
    for c in candidates:
        key = (c["dimension"], c["dim_value"])
        if key in existing:
            r = existing[key]
            r.evidence_n, r.rate, r.baseline = c["evidence_n"], c["rate"], c["baseline"]
            r.updated_at = datetime.utcnow()
            continue
        r = Rule(user_id=user_id, statement=c["statement"], dimension=c["dimension"],
                 dim_value=c["dim_value"], evidence_n=c["evidence_n"], rate=c["rate"],
                 baseline=c["baseline"], direction=c["direction"],
                 status=RuleStatus.HYPOTHESIS)
        db.add(r)
        db.flush()
        new_out.append({
            "rule_id": r.id,
            "question": f"혹시 이런 걸까요? \"{r.statement}\"",
            "evidence": f"{r.evidence_n}번 관찰 기준 · 해당 상황 {round(r.rate*100)}% vs 평소 {round(r.baseline*100)}%",
            "actions": [{"key": "yes", "label": "맞아요"},
                        {"key": "no", "label": "아니에요"},
                        {"key": "later", "label": "더 볼래요"}],
        })
    db.commit()
    return new_out[:2]


@app.post("/api/rules/{rule_id}/verdict")
def rule_verdict(rule_id: str, v: RuleVerdict, db: Session = Depends(get_db)):
    """사용자가 확정한 것만 비법서에 오른다. AI는 단정하지 않는다."""
    r = db.get(Rule, rule_id)
    if not r:
        raise HTTPException(404, "가설을 찾을 수 없습니다.")
    mapping = {"yes": RuleStatus.CONFIRMED, "no": RuleStatus.REJECTED, "later": RuleStatus.TESTING}
    if v.verdict not in mapping:
        raise HTTPException(400, "verdict는 yes | no | later 중 하나입니다.")
    r.status = mapping[v.verdict]
    r.user_confirmed_at = datetime.utcnow() if v.verdict == "yes" else None
    r.updated_at = datetime.utcnow()
    db.commit()

    body = {"rule_id": r.id, "status": r.status.value}
    if r.status == RuleStatus.CONFIRMED:
        user = _get_user(db, r.user_id)
        body["share_card"] = manual_mod.share_card(r, user.nickname)
        body["message"] = "사용설명서에 등재됐어요."
    return body


@app.get("/api/manual/{user_id}")
def get_manual(user_id: str, db: Session = Depends(get_db)):
    user = _get_user(db, user_id)
    rules = list(db.scalars(select(Rule).where(Rule.user_id == user_id)
                            .order_by(Rule.user_confirmed_at)))
    m = manual_mod.build(rules, user.nickname)
    m["markdown"] = manual_mod.to_markdown(m)
    m["disclaimer"] = safety.DISCLAIMER
    return m


@app.post("/api/sos/{user_id}/resume")
def sos_resume(user_id: str, db: Session = Depends(get_db)):
    user = _get_user(db, user_id)
    user.sos_until = None
    db.commit()
    return {"message": "가장 작은 것 하나만 해요. '열기만'부터 시작할게요.",
            "forced_level": 0}


@app.delete("/api/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """전량 삭제권. 정서 기록을 다루는 제품의 기본 의무."""
    user = _get_user(db, user_id)
    for model in (SafetyEvent, Rule, Experiment):
        for row in db.scalars(select(model).where(model.user_id == user_id)):
            db.delete(row)
    db.delete(user)
    db.commit()
    return {"deleted": True}


app.mount("/", StaticFiles(directory="web", html=True), name="web")
