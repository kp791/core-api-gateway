from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import List, Dict, Any

app = FastAPI(title="Data Platform API Gateway")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class LogData(BaseModel):
    source: str = Field(..., example="systemA")
    timestamp: str = Field(..., example="2025-10-07T03:30:00Z")
    records: List[Dict[str, Any]] = Field(..., example=[{"event": "startup"}])

@app.post("/logs", status_code=status.HTTP_202_ACCEPTED)
async def ingest_logs(data: LogData, token: str = Depends(oauth2_scheme)):
    # Only demo token accepted
    if token != "my-demo-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"accepted": True, "source": data.source, "count": len(data.records)}

@app.get("/health")
async def health():
    return {"status": "ok"}
