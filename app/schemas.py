from pydantic import BaseModel, Field, field_validator
from typing import Any
import datetime


# ── 감정 기록 ───────────────────────────────────────────────

class MoodRecordRequest(BaseModel):
    mood_emoji: str = Field(..., min_length=1, description="감정 이모지 (예: 😊)")
    intensity: int = Field(..., ge=0, le=10, description="감정 강도 0~10")
    mood_text: str | None = Field(None, max_length=500, description="감정 설명 (선택)")
    anon_id: str | None = Field(None, description="비로그인 사용자 익명 ID")

    @field_validator("mood_emoji")
    @classmethod
    def emoji_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("mood_emoji는 비어있을 수 없습니다.")
        return v


class AnalysisResult(BaseModel):
    analysis_text: str


class MoodRecordResponse(BaseModel):
    record_id: int
    record_date: datetime.date
    saved: bool
    analysis: AnalysisResult | None = None
    analysis_status: str  # "success" | "failed"


# ── 이벤트 로그 ─────────────────────────────────────────────

class EventLogRequest(BaseModel):
    event_id: str = Field(..., min_length=1, description="프론트에서 생성한 이벤트 UUID")
    session_id: str = Field(..., min_length=1)
    user_id: str | None = None
    anon_id: str | None = None
    event_name: str = Field(..., min_length=1)
    metadata: dict[str, Any] | None = None


# ── anon_id 연동 ────────────────────────────────────────────

class LinkDataRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    anon_id: str = Field(..., min_length=1)


class LinkDataResponse(BaseModel):
    updated_count: int


# ── 공통 ────────────────────────────────────────────────────

class StatusResponse(BaseModel):
    status: str = "ok"
