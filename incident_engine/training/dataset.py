from sqlalchemy.orm import Session
from ingestion_api.app.db.database import SessionLocal
from ingestion_api.app.models.metric import MetricSnapshot
import pandas as pd


def load_metric_history(limit: int = 10000) -> pd.DataFrame:
    db: Session = SessionLocal()

    rows = (
        db.query(MetricSnapshot)
        .order_by(MetricSnapshot.timestamp.desc())
        .limit(limit)
        .all()
    )

    db.close()

    return pd.DataFrame(
        [
            {
                "error_rate": r.error_rate,
                "latency_p95": r.latency_p95,
                "request_count": r.request_count,
            }
            for r in rows
        ]
    )
