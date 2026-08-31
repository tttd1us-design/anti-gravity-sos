# 🛠️ [AG-OS v1.0] 정식 제품 및 엔지니어링 개발 명세서
**문서 식별 번호:** AG-SPEC-V1.0-PRODUCTION  
**제품 정의:** 내가 왜 이것을 계속 미루는지 AI가 찾아주고, 지금 당장 할 수 있는 가장 작은 행동까지 정해주는 개인 성공관리 학습 시스템  
**핵심 슬로건:** *"기록하는 AI가 아니라, 나를 학습하고 변화시키는 AI"*  

---

## 1. 제품 정의 및 핵심 가치 제안 (Product Definition)

### 1.1. 해결하는 단 하나의 절실한 문제 (The One Problem)
* **"해야 할 일을 머리로는 알고 있지만, 시작 순간의 부담감과 미루기 습관 때문에 자책하고 실행하지 못하는 문제"**

### 1.2. 핵심 루프 (Core Learning Loop)
AG-OS는 단순한 메모나 타이머 도구가 아닙니다. **사용자의 행동 데이터를 기반으로 자신만의 성공 모델(Success Model)을 구축하는 피드백 루프**입니다.

```
대화 (Conversation)
       ↓
관찰 (Observation) ➔ "업무 시작 전 핑계를 대며 딴짓을 반복함"
       ↓
가설 (Hypothesis)  ➔ "업무 자체보다 시작 순간의 평가 공포가 높음"
       ↓
행동 (Micro-Action)➔ "보고서 작성 ➔ 파일 열고 제목 1줄 적기로 축소"
       ↓
결과 (Result)      ➔ 3분으로 시작해 25분 몰입 완수
       ↓
학습 (Learning)    ➔ "이 사용자에게는 시작 비용 제거가 가장 효과적"
       ↓
규칙 (Rule)        ➔ 개인 성공 알고리즘 (Personal Rule) 저장
       ↓
다음 행동 개인화에 자동 반영 ♻
```

---

## 2. 5대 AI 엔진 아키텍처 (System Architecture)

```
                 ┌────────────────────────────────┐
                 │       사용자 (User Client)      │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │  ① 대화 인터페이스 (Coach UI)   │
                 │   - 감정/목표 퀵 스타터        │
                 │   - 1-질문 소크라테스 대화      │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ ② Desire Discovery Engine      │
                 │   - 표면 목표 ➔ 진짜 속마음   │
                 │   - 내면 저항(Fear/Blocker) 추출│
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ ③ Personal Pattern Engine      │
                 │   - AG Friction Score™ 산출     │
                 │   - 반복 지연 패턴 & 트리거 탐지│
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ ④ Action Engine                │
                 │   - 최소 실행 양자(3분 미션) 생성│
                 │   - 심리적 진입장벽 제로화      │
                 └───────────────┬────────────────┘
                                 │
                                 ▼
                 ┌────────────────────────────────┐
                 │ ⑤ Learning Engine              │
                 │   - 행동 완료/포기 결과 수집    │
                 │   - User Success Graph 업데이트│
                 └───────────────┬────────────────┘
                                 │
                                 └──────→ 다음 대화/행동에 개인화 반영
```

---

## 3. 사용자 여정 및 화면 설계 (User Journey & UX Wireframe)

### 3.1. 첫 진입 화면 (Zero Blank Page Friction)
복잡한 수식이나 빈 텍스트창을 없애고, 1초 만에 감정과 목표를 선택할 수 있도록 설계합니다.

```text
┌───────────────────────────────────────────────────────────┐
│                    안티그레비티 (AG-OS)                   │
├───────────────────────────────────────────────────────────┤
│                                                           │
│                  오늘 마음 상태가 어떤가요?                │
│                                                           │
│         [ 😫 힘들어요 ]   [ 😐 그냥요 ]                    │
│         [ 🙂 괜찮아요 ]   [ 🔥 하고싶어요 ]                 │
│                                                           │
│                  어떤 일을 시작하고 싶나요?               │
│                                                           │
│   [ 💼 일/업무 ]   [ 📖 공부/시험 ]   [ 💰 부업/돈 ]       │
│   [ 🏃 운동/건강 ] [ ✍️ 글쓰기/책 ]   [ 💬 기타 ]         │
│                                                           │
│   또는 편하게 한 줄로 적어주세요:                         │
│   [                                         ] [전송]     │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 3.2. 소크라테스 탐색 대화 흐름
* **사용자:** "퇴근하고 자격증 공부해야 하는데 피곤해서 유튜브만 보게 돼요."
* **AI Coach (관찰 & 가설):**  
  > *"하루 종일 일하고 오면 쉬고 싶은 게 당연해요. 자책하지 마세요 😊  
  > 그런데 혹시 공부가 귀찮은 걸까요, 아니면 책을 폈을 때 공부할 분량이 너무 많아서 막막한 걸까요?"*
* **사용자:** "분량이 너무 많아서 어디서부터 손대야 할지 모르겠어요."
* **Action Engine (최소 행동 제안):**  
  > *"그렇다면 오늘 2시간 공부할 필요 없습니다.  
  > **'문제집 목차를 펴고 오늘 볼 페이지에 포스트잇 하나 붙이기'**만 해볼까요?  
  > 3분 타이머 맞춰드릴게요. 이것만 하고 바로 덮으셔도 됩니다!"*

---

## 4. 핵심 지표: 3대 상태 대시보드 (3-Axis Status)

복잡한 숫자 대신 사용자가 자신의 상태를 직관적으로 이해할 수 있는 3개 축을 제공합니다.

| 지표명 | 질문 | 설명 |
| :--- | :--- | :--- |
| **🎯 Clarity (방향)** | *"나는 무엇을 원하는가?"* | 목표와 원하는 결과가 얼마나 선명한가 (0~100%) |
| **🧱 Friction (저항)** | *"무엇이 나를 막고 있는가?"* | 시작 순간의 심리적 부담감 (AG Friction Score™, 0~100%) |
| **🚀 Momentum (실행탄력)** | *"나는 실제로 움직이고 있는가?"* | 최근 7일간의 미션 완료 연속성 (0~100%) |

---

## 5. 데이터베이스 스키마 명세 (PostgreSQL + JSONB + Vector)

복잡한 그래프 DB를 섣불리 도입하지 않고, **PostgreSQL (JSONB)와 Vector 임베딩**으로 실용적이고 확장성 높은 스키마를 구성합니다.

```sql
-- 1. 사용자 테이블
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. 목표 (Goals)
CREATE TABLE goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL, -- WORK, STUDY, MONEY, HEALTH, WRITING
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. 추출된 욕망 및 내면 저항 (Desires & Fears)
CREATE TABLE cognitive_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    goal_id UUID REFERENCES goals(id) ON DELETE SET NULL,
    node_type VARCHAR(50) NOT NULL, -- CORE_DESIRE, FEAR, DEFENSE_PATTERN
    statement TEXT NOT NULL,
    confidence_score FLOAT DEFAULT 0.8, -- 0.0 ~ 1.0
    evidence_dialogue TEXT,              -- AI가 이 판단을 내린 대화 근거
    frequency INT DEFAULT 1,             -- 반복 감지 횟수
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. 일일 행동 및 결과 (Actions & Outcomes)
CREATE TABLE action_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    goal_id UUID REFERENCES goals(id) ON DELETE SET NULL,
    original_task TEXT NOT NULL,
    downsized_action TEXT NOT NULL,      -- 3분 마이크로 액션
    friction_score_at_start FLOAT,      -- 시작 시점의 AG Friction Score™
    duration_minutes INT DEFAULT 3,
    status VARCHAR(50) NOT NULL,        -- COMPLETED, ABANDONED, SKIPPED
    actual_spent_minutes INT,           -- 실제 작업 시간 (예: 3분 미션 후 25분 작업)
    user_feedback_emotion VARCHAR(50),  -- RELIEVED, ENERGIZED, TIRED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. 개인 성공 규칙 (Personal Rules - Dalio Principles)
CREATE TABLE personal_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    trigger_condition TEXT NOT NULL,    -- [상황: 결과물 공개를 앞두고 미루고 싶을 때]
    recommended_action TEXT NOT NULL,   -- [원칙: 비공개 초안 1줄 작성으로 시작한다]
    success_rate FLOAT DEFAULT 1.0,     -- 이 규칙을 적용했을 때의 실행 성공률
    sample_count INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 6. AI 에이전트 프롬프트 및 추출 JSON 명세

### 6.1. 인지 분석 및 패턴 추출 JSON 스키마 (RFC 8259 준수)
AI는 대화가 끝날 때마다 사용자의 심리를 단정하지 않고 **신뢰도(Confidence)와 대화 근거(Evidence)**를 포함한 JSON을 출력합니다.

```json
{
  "session_summary": {
    "target_goal": "월 100만원 부업 파이프라인 개설",
    "clarity_score": 0.85,
    "current_friction_score": 0.65,
    "momentum_score": 0.70
  },
  "detected_nodes": [
    {
      "node_type": "CORE_DESIRE",
      "statement": "회사에 종속되지 않는 경제적 자립과 자율성 확보",
      "confidence": 0.92,
      "evidence": "대화 중 '내 시간의 주도권을 되찾고 싶다'는 표현 2회 반복"
    },
    {
      "node_type": "FEAR",
      "statement": "초안의 완성도가 부족해 전문가 그룹에 비판받을 것에 대한 공포",
      "confidence": 0.78,
      "evidence": "글 작성을 앞두고 '완벽하게 준비해야 한다'며 3주간 작성을 중단한 로그"
    }
  ],
  "recommended_micro_action": {
    "action_statement": "스마트폰 메모장을 켜고 상품 아이디어 단어 3개만 적기",
    "time_box_minutes": 3,
    "strategy_type": "ELIMINATE_START_FRICTION",
    "trigger_cue": "침대에 누운 상태에서 즉시 메모장 앱 클릭"
  }
}
```

---

## 7. 초기 킬러 상품: 「나를 이해하는 AI」 14일 성공 프로그램

단순 구독 SaaS가 아닌, 14일 동안 나만의 **My Success Manual (개인 성공 매뉴얼)**을 완성해 주는 고부가가치 프로그램으로 런칭합니다.

```
[14일 여정 로드맵]
Day 1~3  : [Discover] 내가 진짜 원하는 것과 우선순위 찾기
Day 4~6  : [Understand] 나는 어떤 상황에서 미루는가? (내면 저항 지도)
Day 7~10 : [Experiment] 3분 마이크로 행동 실험 (나에게 맞는 시작법 찾기)
Day 11~13: [Rule Mining] 실패 패턴 분석 & 나만의 If-Then 성공 법칙 추출
Day 14   : [Asset] 🌟 My Success Manual 개인 맞춤형 리포트 발급
```

### 14일 완료 산출물: My Success Manual (PDF/Notion)
```markdown
# 📘 [홍길동 님의 성공 매뉴얼: My Success Manual]

1. 나는 [새로운 프로젝트를 시작할 때]
   [완성도에 대한 과도한 기대와 평가 공포] 때문에 멈추는 경향이 있습니다.

2. 그럴 때는 [계획을 더 세우기보다]
   ['비공개 1인 모드에서 3분간 거친 초안 적기'] 방식으로 시작하는 것이 85%의 확률로 효과적이었습니다.

3. 나에게 가장 잘 맞는 첫 행동 단위는
   [거창한 작업이 아닌 '파일 열고 단어 3개 메모']입니다.

4. 나의 절대 행동 원칙:
   "완벽하게 끝내려 하지 말고, 3분 동안 미완성 상태를 시작한다."
```

---

## 8. 100명 베타 검증 프로토콜 (Validation Protocol)

DAU나 체류시간 대신 **사용자의 실제 행동 변화를 입증하는 4대 핵심 KPI**를 측정합니다.

| 지표명 (KPI) | 측정 기준 | 목표 수치 |
| :--- | :--- | :--- |
| **Time to Action** | 고민 발화 시점부터 실제 3분 행동 착수까지 소요 시간 | **120초(2분) 이내** |
| **Action Completion Rate** | AI가 제안한 3분 마이크로 행동의 실제 완료율 | **75% 이상** |
| **Pattern Accuracy** | AI가 도출한 저항 패턴에 대해 사용자가 "맞다"고 인정한 비율 | **80% 이상** |
| **14일 완주율 & 지불 의사** | 14일 프로그램을 완주하고 "유료로 계속 쓰겠다"고 답한 비율 | **20% 이상** |
