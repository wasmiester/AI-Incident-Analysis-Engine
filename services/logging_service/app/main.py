from fastapi import FastAPI
from ingestion_api.app.schemas.log_event import LogEventCreate
from ingestion_api.app.db.database import Base, SessionLocal, engine
from models import LogEvent

app = FastAPI(title="Central Logging Service")

@app.post("/logs")
def ingest_log(event: LogEventCreate):
    db = SessionLocal()
    log = LogEvent(**event.dict())
    db.add(log)
    db.commit()
    return {"status": "logged"}
