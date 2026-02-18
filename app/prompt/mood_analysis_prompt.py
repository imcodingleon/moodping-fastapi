"""
LLM 프롬프트 빌더.

intensity 범위에 따라 3가지 톤으로 분기:
  - 7~10 : 긍정/칭찬 (업무 성과 연결, MP-B-22 검증 조건 반영)
  - 0~4  : 공감 위주 (CBT 재프레이밍, moodping 원본 feedback.py 구조 참고)
  - 5~6  : 중립 (균형 있는 메타인지 안내)
"""

from app.models import MoodRecord

SYSTEM_PROMPT = (
    "당신은 인지행동치료(CBT)와 메타인지(Metacognition) 이론에 정통한 심리 분석 전문가입니다. "
    "사용자의 감정을 구조적으로 분석하여 따뜻하고 친근한 어조로 응답합니다. "
    "반드시 아래 JSON 형식으로만 응답하세요: {\"analysis_text\": \"내용\"} "
    "제목, 번호, bullet, 라벨 없이 완전히 자연스러운 한 문단(최대 2~3문단)으로만 작성합니다."
)


def build(record: MoodRecord) -> str:
    """MoodRecord를 받아 intensity 기반 프롬프트 문자열을 반환합니다."""
    note = record.mood_text if record.mood_text and record.mood_text.strip() else "별도의 메모 없음"

    if record.intensity >= 7:
        return _positive(record, note)
    elif record.intensity <= 4:
        return _empathy(record, note)
    else:
        return _neutral(record, note)


def _positive(record: MoodRecord, note: str) -> str:
    return (
        f"[사용자 감정 데이터]\n"
        f"- 감정 이모지: {record.mood_emoji}\n"
        f"- 감정 강도: {record.intensity}점 / 10점\n"
        f"- 감정 메모: {note}\n\n"
        f"[분석 방향]\n"
        f"사용자가 높은 긍정 감정({record.intensity}점)을 기록했습니다. "
        f"이 밝은 에너지가 업무나 일상의 성과에 어떻게 긍정적 영향을 미칠 수 있는지 구체적으로 칭찬하세요. "
        f"이 상태를 유지하거나 발전시킬 수 있는 실천 가능한 한 마디도 덧붙이세요. "
        f"친근하고 부드러운 어조로 2~3문단 이내로 작성하세요. "
        f'반드시 {{"analysis_text": "내용"}} JSON 형식으로만 응답하세요.'
    )


def _empathy(record: MoodRecord, note: str) -> str:
    return (
        f"[사용자 감정 데이터]\n"
        f"- 감정 이모지: {record.mood_emoji}\n"
        f"- 감정 강도: {record.intensity}점 / 10점\n"
        f"- 감정 메모: {note}\n\n"
        f"[분석 방향]\n"
        f"사용자가 낮거나 부정적인 감정({record.intensity}점)을 기록했습니다. "
        f"아래 순서로 분석하세요:\n"
        f"1) 이 감정이 현재 상황에서 매우 자연스럽고 타당한 반응임을 먼저 충분히 공감하세요.\n"
        f"2) CBT 관점으로, 이 감정이 개인의 결함이 아니라 특정 상황과 조건에서 비롯된 것임을 부드럽게 재프레이밍하세요.\n"
        f"3) 과도한 자기비판을 완화하는 따뜻한 한 마디로 마무리하세요.\n"
        f"친근하고 부드러운 어조로 2~3문단 이내로 작성하세요. "
        f'반드시 {{"analysis_text": "내용"}} JSON 형식으로만 응답하세요.'
    )


def _neutral(record: MoodRecord, note: str) -> str:
    return (
        f"[사용자 감정 데이터]\n"
        f"- 감정 이모지: {record.mood_emoji}\n"
        f"- 감정 강도: {record.intensity}점 / 10점\n"
        f"- 감정 메모: {note}\n\n"
        f"[분석 방향]\n"
        f"사용자가 중간 강도({record.intensity}점)의 감정을 기록했습니다. "
        f"이 중립적 상태를 인정하고, 자기 감정을 인식했다는 것 자체가 메타인지의 좋은 출발점임을 알려주세요. "
        f"이 상태에서 에너지를 소비하지 않고 자신을 돌볼 수 있는 작은 방법을 제안하세요. "
        f"친근하고 부드러운 어조로 2~3문단 이내로 작성하세요. "
        f'반드시 {{"analysis_text": "내용"}} JSON 형식으로만 응답하세요.'
    )
