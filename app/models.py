"""3분 실험실 - 데이터 모델
설계 원칙: '실패' 상태를 스키마에 두지 않는다. 모든 결과는 관찰(observation)이다.
"""
from __future__ import annotations
import enum
import uuid
from datetime import datetime, date

from sqlalchemy import (String, Integer, Float, Boolean, DateTime, Date,
                        Enum, ForeignKey, Text)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _uid() -> str:
    return str(uuid.uuid4())


class Outcome(str, enum.Enum):
    """의도적으로 SUCCESS/FAIL이 없다. 네 가지 모두 유효한 관찰 결과."""
    NOT_STARTED = "NOT_STARTED"          # 시작도 못 함  -> 실패가 아니라 데이터
    STARTED_STOPPED = "STARTED_STOPPED"  # 시작했다 멈춤
    DID_MINIMUM = "DID_MINIMUM"          # 계획한 만큼 함
    WENT_LONGER = "WENT_LONGER"          # 계획보다 더 함
    NO_RESPONSE = "NO_RESPONSE"          # 기록 안 함 (시스템 자동)


STARTED_OUTCOMES = {Outcome.STARTED_STOPPED, Outcome.DID_MINIMUM, Outcome.WENT_LONGER}


class RuleStatus(str, enum.Enum):
    HYPOTHESIS = "HYPOTHESIS"   # 채굴됨, 사용자 확인 대기
    TESTING = "TESTING"         # 사용자가 '더 볼래요' 선택
    CONFIRMED = "CONFIRMED"     # 사용자가 '맞아요' 확정 -> 비법서 등재
    REJECTED = "REJECTED"       # 사용자가 '아니에요'


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uid)
    nickname: Mapped[str] = mapped_column(String(40), default="연구자")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # 비상착륙 모드 해제 예정일
    sos_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    # 민감정보(정서 기록) 저장 동의 - 미동의 시 note 컬럼 저장 자체를 생략
    consent_emotion_log: Mapped[bool] = mapped_column(Boolean, default=False)


class Experiment(Base):
    __tablename__ = "experiments"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)

    task_text: Mapped[str] = mapped_column(String(200))
    task_type: Mapped[str] = mapped_column(String(20), default="GENERIC")

    # 이 실험이 검증하려는 가설 (없으면 탐색적 실험)
    hypothesis_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    variation_key: Mapped[str] = mapped_column(String(30), default="PLAIN")

    # 사용자가 직접 고른 사다리 단계 = 그 순간의 진짜 마찰 신호
    ladder_level: Mapped[int] = mapped_column(Integer, default=1)
    ladder_step_text: Mapped[str] = mapped_column(String(300), default="")
    planned_minutes: Mapped[float] = mapped_column(Float, default=3.0)
    # 사다리를 몇 칸 내렸는지 (제안 대비) - 저항 강도의 대리 지표
    ladder_drops: Mapped[int] = mapped_column(Integer, default=0)

    # 맥락 (채굴 차원)
    ctx_time_bucket: Mapped[str] = mapped_column(String(12), default="unknown")
    ctx_energy: Mapped[int] = mapped_column(Integer, default=0)      # 1~4
    ctx_place: Mapped[str] = mapped_column(String(12), default="unknown")
    ctx_is_weekend: Mapped[bool] = mapped_column(Boolean, default=False)
    ctx_perfection_word: Mapped[bool] = mapped_column(Boolean, default=False)

    outcome: Mapped[Outcome | None] = mapped_column(Enum(Outcome), nullable=True)
    minutes_actual: Mapped[float | None] = mapped_column(Float, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    observed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Rule(Base):
    __tablename__ = "rules"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)

    statement: Mapped[str] = mapped_column(String(300))
    dimension: Mapped[str] = mapped_column(String(30))
    dim_value: Mapped[str] = mapped_column(String(40))

    evidence_n: Mapped[int] = mapped_column(Integer, default=0)
    rate: Mapped[float] = mapped_column(Float, default=0.0)      # 해당 맥락 착수율
    baseline: Mapped[float] = mapped_column(Float, default=0.0)  # 전체 착수율
    direction: Mapped[str] = mapped_column(String(4), default="up")  # up | down

    status: Mapped[RuleStatus] = mapped_column(Enum(RuleStatus), default=RuleStatus.HYPOTHESIS)
    user_confirmed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SafetyEvent(Base):
    """원문은 저장하지 않는다. 수준과 시각만 남긴다."""
    __tablename__ = "safety_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uid)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), index=True)
    level: Mapped[str] = mapped_column(String(12))   # ELEVATED | HIGH
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
