from sqlalchemy.orm import Session
from incident_engine.db.database import SessionLocal
from ingestion_api.app.models.metric import Metric
from incident_engine.detector import detect_anomaly
from incident_engine.service import save_incident

def fetch_unprocessed_metrics(limit: int = 10):
    session: Session = SessionLocal()

    try:
        return (
            session.query(Metric)
            .filter(Metric.processed.is_(False))
            .order_by(Metric.timestamp)
            .limit(limit)
            .all()
        )
    finally:
        session.close()


def mark_processed(metric_ids):
    if not isinstance(metric_ids, (list, tuple, set)):
        metric_ids = [metric_ids]

    session = SessionLocal()
    session.query(Metric) \
        .filter(Metric.id.in_(metric_ids)) \
        .update({"processed": True}, synchronize_session=False)
    session.commit()
    session.close()


def process_metrics(batch_size: int = 10):
    rows = fetch_unprocessed_metrics(limit=batch_size)

    if not rows:
        print("No unprocessed metrics found.")
        return

    processed_ids = []

    for row in rows:
        print(
            f"--Processing metric | "
            f"service={row.service_name} "
            f"error_rate={row.error_rate} "
            f"latency_p95={row.latency_p95}"
        )

        detection = detect_anomaly(row)

        if detection.get("anomaly"):
            incident = save_incident(detection)
            print(
                f" INCIDENT | "
                f"service={incident.service} "
                f"severity={incident.severity} "
                f"count={incident.occurrence_count}"
            )

        processed_ids.append(row.id)

    mark_processed(processed_ids)
