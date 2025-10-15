from pydantic import BaseModel, Field, field_validator, conlist
from typing import List, Literal, Optional

class IngestionPayload(BaseModel):
    source_type: Literal["csv", "json", "logs"]
    records: List[dict]
    batch_id: str = Field(..., description="Unique identifier for ingestion batch")

    @field_validator("records")
    def ensure_nonempty(cls, v):
        if not v:
            raise ValueError("At least one record is required.")
        return v


class CleanedRecord(BaseModel):
    record_id: str
    normalized: dict
    is_valid: bool


class SummaryRequest(BaseModel):
    batch_id: str
    clean_records: conlist(CleanedRecord, min_length=1)
    ai_mode: Optional[str] = Field("standard", description="Mode: standard | compliance | ops")


