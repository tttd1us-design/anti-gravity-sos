"""
3분 실험실 - 아침 실험 발송 & 저녁 관찰 알림 스케줄러
시간 기준 (KST):
- 아침 발송: 오전 08:00 (오늘의 3분 실험 카드 도착)
- 저녁 발송: 밤 21:30 (오늘의 관찰 기록 리마인더)
"""
import asyncio
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db import SessionLocal
from app.models import User, Experiment, Outcome
from app.core import sos, safety


async def morning_dispatch_job():
    """아침 실험 발송 로직"""
    db: Session = SessionLocal()
    try:
        users = list(db.scalars(select(User)))
        for user in users:
            # 비상착륙 상태 확인
            recent = list(db.scalars(select(Experiment).where(Experiment.user_id == user.id).limit(10)))
            triggered, reason = sos.should_trigger(user, recent)
            if triggered:
                # 비상착륙 메시지 전송 로직 (실제 카카오톡 알림톡/친구톡 API 발송)
                continue
            # 일반 실험 카드 생성 및 카카오 푸시 발송
    finally:
        db.close()


async def evening_observation_job():
    """저녁 관찰 기록 리마인드 로직"""
    db: Session = SessionLocal()
    try:
        # 오늘 날짜에 생성되었으나 outcome이 없는 실험 대상자 조회
        unobserved = list(db.scalars(select(Experiment).where(Experiment.outcome.is_(None))))
        for exp in unobserved:
            # "오늘 무슨 일이 일어났나요? (시작도 못 함도 유효한 데이터예요)" 푸시 발송
            pass
    finally:
        db.close()


async def scheduler_loop():
    """백그라운드 스케줄러 루프"""
    while True:
        now = datetime.now()
        # 간단한 인터벌 체크 (실제 운영 시 CronTab 또는 Celery/APScheduler 연동)
        await asyncio.sleep(60)
