from sqlalchemy.orm import Session
from incident_engine.models.timeline import IncidentTimeline


def record_timeline_event(
    session,
    incident,
    event_type: str,
    message: str,
):

    event = IncidentTimeline(
        incident_id=incident.id,
        event_type=event_type,
        message=message,
    )

    session.add(event)

def add_timeline_event(
    session: Session,
    incident_id,
    event_type: str,
    message: str,
):
    event = IncidentTimeline(
        incident_id=incident_id,
        event_type=event_type,
        message=message,
    )
    session.add(event)
