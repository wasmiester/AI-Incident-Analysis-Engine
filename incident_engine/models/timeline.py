import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from incident_engine.db.database import Base


class IncidentTimeline(Base):
    __tablename__ = "incident_timeline"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(
        UUID(as_uuid=True),
        ForeignKey("incidents.id", ondelete="CASCADE"),
        nullable=False,
    )

    event_type = Column(String, nullable=False)
    message = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    incident = relationship("Incident", back_populates="timeline")
from typing import List, Dict

def build_timeline(events: List[Dict]):
    sorted_events = sorted(events, key=lambda e: e["timestamp"])

    timeline = {}
    for event in sorted_events:
        service = event["service"]
        timeline.setdefault(service, []).append(event)

    return timeline
