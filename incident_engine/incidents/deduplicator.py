from datetime import timedelta
from sqlalchemy import func
from incident_engine.models.incident import Incident


def count_recent_incidents(session, service: str, window_minutes: int = 15) -> int:
    cutoff = func.now() - timedelta(minutes=window_minutes)

    return (
        session.query(func.count(Incident.id))
        .filter(
            Incident.service == service,
            Incident.timestamp >= cutoff,
        )
        .scalar()
    )
