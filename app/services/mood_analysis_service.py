import json
import logging
import re
from sqlalchemy.orm import Session
from app.models import MoodRecord, MoodAnalysis
from app.schemas import AnalysisResult
from app.llm.factory import get_llm_client
from app.prompt import mood_analysis_prompt

logger = logging.getLogger(__name__)


async def analyze_and_save(record: MoodRecord, db: Session) -> AnalysisResult | None:
    """
    LLM 분석을 실행하고 mood_analysis 테이블에 저장합니다.
    실패 시 None을 반환합니다 (기록 저장은 이미 완료된 상태).
    """
    llm = get_llm_client()
    system_prompt = mood_analysis_prompt.SYSTEM_PROMPT
    user_prompt = mood_analysis_prompt.build(record)

    raw = await llm.complete(system_prompt, user_prompt)
    if not raw:
        return None

    analysis_text = _parse_analysis_text(raw)
    if not analysis_text:
        return None

    owner_id = record.user_id or record.anon_id
    analysis = MoodAnalysis(
        record_id=record.id,
        user_id=owner_id,
        analysis_text=analysis_text,
    )
    db.add(analysis)
    db.commit()

    return AnalysisResult(analysis_text=analysis_text)


def _parse_analysis_text(content: str) -> str | None:
    """
    LLM 응답에서 analysis_text를 추출합니다.
    JSON 블록(```json ... ```) 또는 순수 JSON 모두 처리합니다.
    """
    try:
        cleaned = re.sub(r"```json\s*", "", content, flags=re.IGNORECASE)
        cleaned = re.sub(r"```\s*", "", cleaned).strip()
        data = json.loads(cleaned)
        text = data.get("analysis_text", "")
        return text if text else None
    except (json.JSONDecodeError, AttributeError):
        logger.warning("analysis_text JSON 파싱 실패, 원본 텍스트 사용")
        return content[:1000] if content else None
