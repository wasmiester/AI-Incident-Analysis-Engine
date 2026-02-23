from datetime import datetime, timezone
from sqlalchemy.orm import Session

from incident_engine.db.database import SessionLocal
from incident_engine.models.incident import Incident
from incident_engine.timeline.service import add_timeline_event
from incident_engine.detector import escalate_severity


def upsert_incident(session: Session, incident_data: dict) -> Incident:
    incident = (
        session.query(Incident)
        .filter(Incident.service == incident_data["service"])
        .order_by(Incident.last_seen.desc())
        .first()
    )

    now = datetime.now(timezone.utc)

    if not incident or incident.status == "RESOLVED":
        incident = Incident(
            service=incident_data["service"],
            timestamp=now,
            anomaly=True,
            score=incident_data["score"],
            severity=incident_data["severity"],
            explanation=incident_data["explanation"],
            status="ACTIVE",
            occurrence_count=1,
            first_seen=now,
            last_seen=now,
        )
        session.add(incident)
        session.flush()

        add_timeline_event(
            session,
            incident.id,
            event_type="DETECTED",
            message=f"Incident detected for service {incident.service}",
        )

        return incident

    incident.last_seen = now
    incident.occurrence_count += 1

    previous_severity = incident.severity
    new_severity = escalate_severity(
        current_severity=previous_severity,
        first_seen=incident.first_seen,
        now=now,
        occurrence_count=incident.occurrence_count
    )

    if new_severity != previous_severity:
        incident.severity = new_severity

        add_timeline_event(
            session,
            incident.id,
            event_type="SEVERITY_ESCALATED",
            message=f"Severity escalated from {previous_severity} to {new_severity}",
        )
    else:
        add_timeline_event(
            session,
            incident.id,
            event_type="REOCCURRED",
            message="Anomaly detected again while incident is active",
        )

    return incident


def resolve_incident_if_recovered(
    session: Session,
    incident: Incident,
    recovered: bool,
):
    if incident.status != "ACTIVE" or not recovered:
        return

    incident.status = "RESOLVED"
    incident.last_seen = datetime.now(timezone.utc)

    add_timeline_event(
        session,
        incident.id,
        event_type="RESOLVED",
        message="Service metrics returned to healthy levels",
    )

def save_incident(incident_data: dict):
    session: Session = SessionLocal()
    try:
        incident = upsert_incident(session, incident_data)
        session.commit()
        session.refresh(incident)
        return incident
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()