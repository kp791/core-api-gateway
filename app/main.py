from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from .schemas import IngestionPayload, CleanedRecord, SummaryRequest
from .errors import PlatformError, platform_error_handler

app = FastAPI(
    title="Data Platform API Gateway",
    version="0.1",
    description="Validates, cleans, stores and summarizes enterprise data securely"
)
app.add_exception_handler(PlatformError, platform_error_handler)

mock_store = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LogData(BaseModel):
    source: str = Field(
        ..., 
        json_schema_extra={
            "example": "systemA",
            "description": "Source system name"
        }
    )
    timestamp: str = Field(
        ..., 
        json_schema_extra={
            "example": "2025-10-07T03:30:00Z"
        }
    )
    records: list = Field(
        ..., 
        json_schema_extra={
            "example": [{"event": "startup"}]
        }
    )


@app.post("/ingest")
async def ingest_data(payload: IngestionPayload):
    if payload.batch_id in mock_store:
        raise PlatformError(400, "Batch already ingested", "BATCH_DUPLICATE")
    mock_store[payload.batch_id] = payload.records
    return {"status": "accepted", "records": len(payload.records)}

@app.post("/clean")
async def clean_records(batch_id: str):
    records = mock_store.get(batch_id)
    if not records:
        raise PlatformError(404, "Batch not found", "BATCH_NOT_FOUND")
    cleaned = [{"record_id": f"{batch_id}-{i}", "normalized": r, "is_valid": True} for i, r in enumerate(records)]
    return {"batch_id": batch_id, "cleaned": cleaned}

@app.post("/summarize")
async def summarize_records(request: SummaryRequest):
    summary = {
        "batch_id": request.batch_id,
        "mode": request.ai_mode,
        "summary": f"Processed {len(request.clean_records)} validated records into operational insights."
    }
    return summary

@app.post("/logs", status_code=status.HTTP_202_ACCEPTED)
async def ingest_logs(data: LogData, token: str = Depends(oauth2_scheme)):
    # Only demo token accepted
    if token != "my-demo-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"accepted": True, "source": data.source, "count": len(data.records)}

@app.get("/health")
async def health():
    return {"status": "ok"}
