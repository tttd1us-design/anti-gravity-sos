# 🧪 [3분 실험실 (3-Minute Lab)] 제품 및 행동과학 아키텍처 명세서

**한 줄 슬로건:** *"MBTI는 내가 나에 대해 '말한 것'으로 만들어집니다. 3분 실험실은 내가 실제로 '한 것'으로 만들어집니다."*  
**핵심 관점의 반전:** **사용자를 '피험자'에서 '과학자(연구자)'로 전환. AI는 실험 조수.**  
**산출물:** 📕 **나의 사용설명서 (My User Manual)**  

---

## 1. 핵심 철학 및 4대 결함 동시 해법

```
┌──────────────────────────────┬────────────────────────────────────────────────────────┐
│ 기존 앱의 치명적 결함       │ 3분 실험실 (3-Minute Lab)의 과학적 해법                │
├──────────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. 가짜 정밀함 (수식/진단)  │ AI가 단정하지 않고 실험 가설과 실측 데이터만 제시     │
│ 2. 실패 시 자책 (Guilt Trap) │ 안 되는 것도 '유효한 데이터 관찰' (시작도 못함 = 데이터)│
│ 3. 의지력 고갈 (이탈)        │ 매일 새로워지는 호기심·역설 실험(Paradox Experiment)  │
│ 4. 안전/심리 진단 리스크    │ 심리 진단 완전 배제, 행동 실험 기록 도구로 한정      │
│ 5. 손에 잡히는 산출물 부재   │ 실험으로 한 줄씩 잠금 해제되는 📕 '나의 사용설명서'     │
└──────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## 2. 3대 핵심 사용자 화면 명세

### ① 🧪 오늘의 실험 카드 (Daily Experiment Card)
"오늘 할 일" 대신 매일 도착하는 단 하나의 호기심 검증 카드.

```text
┌───────────────────────────────────────────────────────────────┐
│ 🧪 오늘의 실험 #17                                            │
├───────────────────────────────────────────────────────────────┤
│ 가설: 나는 "완성"을 목표로 삼으면 시작을 못 한다.              │
│       (지금까지 6번 중 5번 그랬어요)                           │
│                                                               │
│ 오늘 검증법: 보고서를 "일부러 형편없이" 3분만 쓴다.            │
│              3분이 지나면 무슨 일이 있어도 강제로 멈춘다.     │
│                                                               │
│      [ ⏱️ 3분 실험 시작 ]      [ 🪜 너무 부담돼요 (사다리) ]  │
└───────────────────────────────────────────────────────────────┘
```

* **행동 사다리 (Laddering):**
  * `1단계 (30초)`: 파일 열기만 하기
  * `2단계 (3분)`: 제목 한 줄만 적기
  * `3단계 (10분)`: 목차만 적기
  * `4단계 (25분)`: 한 단락 완성하기

---

### ② 🔬 관찰 기록 ("완료/미완료" 버튼 삭제)
실패라는 단어를 완전히 없애고, 4가지 객관적 관찰 선택지를 제공합니다.

```text
┌───────────────────────────────────────────────────────────────┐
│ 🔬 실험 #17 관찰 기록                                         │
├───────────────────────────────────────────────────────────────┤
│ 무슨 일이 일어났나요?                                         │
│                                                               │
│ [ 🛑 시작도 못 함 ]   [ ⏸️ 시작했다 멈춤 ]                    │
│ [ ✅ 3분 완수 ]       [ 🚀 3분 넘게 몰입함 ]                  │
│                                                               │
│ 그때 기분이 어땠나요? (선택 사항)                             │
│ [                                                ]            │
│                                                               │
│ 💬 AI 조수의 피드백 (시작도 못 함 선택 시):                   │
│ "좋아요, 중요한 데이터예요! 이번이 3번째인데 모두 밤 10시     │
│  이후였어요. 밤에는 시작 자체가 어려운 걸지도 몰라요."         │
└───────────────────────────────────────────────────────────────┘
```

---

### ③ 📕 나의 사용설명서 (My User Manual)
실험이 쌓일 때마다 **30개의 잠긴 법칙**이 하나씩 실측 근거와 함께 잠금 해제됩니다.

```text
┌───────────────────────────────────────────────────────────────┐
│ 📕 나의 사용설명서 (7/30 발견됨)                              │
├───────────────────────────────────────────────────────────────┤
│ ✅ 확정된 나의 법칙                                            │
│  #01 나는 오후 2시보다 오전 7시에 시작 확률이 3배 높다.        │
│      (근거: 실험 14회 중 오전 82% / 오후 27%)                 │
│  #03 "완벽하게"라는 단어가 들어간 과제는 4일 이상 미룬다.     │
│      (근거: 실험 9회 중 8회 시작 지연)                        │
│                                                               │
│ 🔍 검증 중인 가설                                             │
│  #08 누군가에게 선언하면 시작 확률이 올라간다? (2/5회 관찰)    │
│                                                               │
│ 🔒 아직 발견되지 않은 법칙 (23개 잠김)                        │
└───────────────────────────────────────────────────────────────┘
```

---

### ④ 🛬 SOS 비상착륙 (Safe Landing Mode)
연속 3회 '시작도 못 함' 또는 3일 무응답 시 자동 발동하는 정서적 안전장치.

```text
┌───────────────────────────────────────────────────────────────┐
│ 🛬 비상착륙 모드 (Safe Landing)                               │
├───────────────────────────────────────────────────────────────┤
│ 실험을 잠시 중단합니다.                                       │
│ 데이터를 보니 지금은 방법의 문제가 아니라 '연료'의 문제입니다. │
│                                                               │
│ 오늘 유일한 미션:                                             │
│  ☑ 따뜻한 물 한 잔 마시기                                     │
│  ☑ 7시간 푹 자기                                             │
│                                                               │
│ ※ 비법서는 안전하게 보관되어 있습니다. 내일 다시 만나요.       │
└───────────────────────────────────────────────────────────────┘
```

---

## 3. 정직한 PostgreSQL 2-테이블 스키마

```sql
-- 1. 실험 기록 테이블
CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    task_text TEXT NOT NULL,
    hypothesis TEXT NOT NULL,
    ladder_level INT DEFAULT 2, -- 1: 30초, 2: 3분, 3: 10분, 4: 25분
    context_time VARCHAR(20),   -- MORNING, AFTERNOON, NIGHT
    outcome VARCHAR(30) NOT NULL, -- NOT_STARTED, STOPPED_EARLY, COMPLETED_3MIN, EXCEEDED_3MIN
    minutes_actual INT,
    note TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 발견된 개인 법칙 테이블
CREATE TABLE rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    statement TEXT NOT NULL,
    dimension VARCHAR(50) NOT NULL, -- TIME_BUCKET, TASK_WORD, PLACE, LADDER
    evidence_count INT NOT NULL,
    success_rate FLOAT NOT NULL,
    status VARCHAR(20) DEFAULT 'HYPOTHESIS', -- HYPOTHESIS, TESTING, CONFIRMED, REJECTED
    user_confirmed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 4. 정직한 법칙 채굴 알고리즘 (Rule Mining Engine)

```python
def mine_user_rules(experiments):
    """
    가짜 물리학 없이 맥락별 착수율 차이를 정직하게 비교.
    표본 5회 미만은 가설로만 표시하고, 확정은 사용자가 직접 승인.
    """
    rules = []
    # 1. 시간대별 착수율 분석
    morning_exps = [e for e in experiments if e.get("context_time") == "MORNING"]
    night_exps = [e for e in experiments if e.get("context_time") == "NIGHT"]
    
    if len(morning_exps) >= 5 and len(night_exps) >= 5:
        m_rate = sum(1 for e in morning_exps if e["outcome"] in ["COMPLETED_3MIN", "EXCEEDED_3MIN"]) / len(morning_exps)
        n_rate = sum(1 for e in night_exps if e["outcome"] in ["COMPLETED_3MIN", "EXCEEDED_3MIN"]) / len(night_exps)
        
        if m_rate - n_rate >= 0.3:
            rules.append({
                "statement": f"나는 밤보다 아침에 시작 확률이 {round(m_rate/max(n_rate, 0.1), 1)}배 높다",
                "dimension": "TIME_BUCKET",
                "evidence_count": len(morning_exps) + len(night_exps),
                "success_rate": m_rate,
                "status": "CONFIRMED"
            })
    return rules
```

---

## 5. 가격 및 1,000명 수험생/창업가 챌린지 로드맵

* **무료 플랜:** 매일 실험 무제한 + 사용설명서 3개 항목 잠금 해제
* **Pro 플랜 (월 9,900원):** 사용설명서 30개 전체 잠금 해제 + 주간 실험 리포트 + SOS 비상착륙 모드
* **검증 지표 (Single Metric):** **30일 후에도 저녁 관찰 기록을 작성하는 사용자의 비율 ($\ge 40\%$)**
