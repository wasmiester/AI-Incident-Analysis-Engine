from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from ingestion_api.app.db.database import Base, engine, SessionLocal
from ingestion_api.app.models.metric import Metric
from ingestion_api.app.schemas.metric import MetricCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest_metrics(payload: MetricCreate, db: Session = Depends(get_db)):
    metric = Metric(
        service_name=payload.service,
        timestamp=payload.timestamp,
        latency_p95=payload.latency_p95,
        error_rate=payload.error_rate,
        request_count=payload.request_count
    )
    db.add(metric)
    db.commit()
    return {"status": "ingested"}
