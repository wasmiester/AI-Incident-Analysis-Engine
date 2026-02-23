from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from incident_engine.models.incident import Incident

GRACE_PERIOD_SECONDS = 120


def auto_resolve_if_recovered(
    session: Session,
    service: str,
):
    incident = (
        session.query(Incident)
        .filter(
            Incident.service == service,
            Incident.status == "ACTIVE",
        )
        .one_or_none()
    )

    if not incident:
        return None

    now = datetime.now()
    time_since_last_seen = now - incident.last_seen

    if time_since_last_seen < timedelta(seconds=GRACE_PERIOD_SECONDS):
        return None

    incident.status = "RESOLVED"
    incident.last_seen = now

    print(
        f"--INCIDENT AUTO-RESOLVED | "
        f"service={incident.service} "
        f"id={incident.id}"
    )

    return incident
