from app.db import SessionLocal, init_db
from app.adapters.kakao import handle_kakao_message
from app.models import User, Experiment, Outcome

def test_kakao_fsm_flow():
    init_db()
    db = SessionLocal()
    try:
        user_key = "test_kakao_user_999"

        # 1. 새 실험 요청
        payload1 = {
            "userRequest": {
                "user": {"id": user_key},
                "utterance": "보고서 작성 시작하기"
            }
        }
        res1 = handle_kakao_message(db, payload1)
        assert "version" in res1
        assert "outputs" in res1["template"]
        assert "basicCard" in res1["template"]["outputs"][0]

        # 2. 사다리 내리기 ("더 작게")
        payload2 = {
            "userRequest": {
                "user": {"id": user_key},
                "utterance": "더 작게"
            }
        }
        res2 = handle_kakao_message(db, payload2)
        assert "사다리 하향" in res2["template"]["outputs"][0]["basicCard"]["title"]

        # 3. 관찰 기록 ("시작도 못 함" - 실패가 아닌 데이터)
        payload3 = {
            "userRequest": {
                "user": {"id": user_key},
                "utterance": "시작도 못 함"
            }
        }
        res3 = handle_kakao_message(db, payload3)
        assert "기록해주셔서 고마워요" in res3["template"]["outputs"][0]["simpleText"]["text"]

        # 4. 안전 스크리닝 (위기 언어 감지)
        payload_safety = {
            "userRequest": {
                "user": {"id": user_key},
                "utterance": "다 끝내고 싶어요 사라지고 싶어요"
            }
        }
        res_safety = handle_kakao_message(db, payload_safety)
        assert "지금은 실험보다 사람이 필요해요" in res_safety["template"]["outputs"][0]["simpleText"]["text"]
        assert "자살예방 상담전화" in res_safety["template"]["outputs"][0]["simpleText"]["text"]

    finally:
        db.close()

if __name__ == "__main__":
    test_kakao_fsm_flow()
    print("PASS: test_kakao_fsm_flow")
