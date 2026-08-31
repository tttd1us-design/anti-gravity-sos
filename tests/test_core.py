from datetime import datetime

from app.core import ladder, miner, sos, safety
from app.models import Experiment, Outcome, User


def _e(**kw):
    base = dict(user_id="u", task_text="보고서 쓰기", task_type="WRITING",
                variation_key="PLAIN", ladder_level=1, ctx_time_bucket="morning",
                ctx_energy=3, ctx_place="home", ctx_perfection_word=False,
                outcome=Outcome.DID_MINIMUM, observed_at=datetime.utcnow())
    base.update(kw)
    return Experiment(**base)


def test_ladder_is_task_aware_not_hardcoded():
    """기존 결함: 무슨 과제든 'Obsidian 열고 쓰기'가 나왔다."""
    for task in ["스쿼트 30개", "설거지하기", "엄마한테 전화하기", "보고서 쓰기"]:
        steps = ladder.build_ladder(task)
        assert len(steps) == 5
        assert all("Obsidian" not in s["text"] for s in steps)
        assert steps[0]["minutes"] < steps[4]["minutes"]
    assert ladder.detect_task_type("스쿼트 30개") == "EXERCISE"
    assert ladder.detect_task_type("설거지하기") == "CHORE"


def test_miner_silent_below_min_sample():
    assert miner.mine([_e() for _ in range(5)]) == []


def test_miner_finds_time_pattern_with_evidence():
    exps = [_e(ctx_time_bucket="morning", outcome=Outcome.DID_MINIMUM) for _ in range(6)]
    exps += [_e(ctx_time_bucket="night", outcome=Outcome.NOT_STARTED) for _ in range(6)]
    found = miner.mine(exps)
    assert found
    top = found[0]
    assert top["evidence_n"] >= miner.MIN_SAMPLE
    assert 0.0 <= top["rate"] <= 1.0


def test_sos_triggers_on_three_not_started():
    recent = [_e(outcome=Outcome.NOT_STARTED) for _ in range(3)]
    fired, reason = sos.should_trigger(User(id="u"), recent)
    assert fired and reason == "streak"


def test_safety_screens_and_offers_resources():
    assert safety.screen("그냥 좀 지쳤어요") == "ELEVATED"
    high = safety.response(safety.screen("다 끝내고 싶어요 사라지고 싶어요"))
    assert high["suppress_experiments"] and high["resources"]
