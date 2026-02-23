import uuid
from datetime import datetime,timezone

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Float,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from incident_engine.db.database import Base
from incident_engine.models.timeline import IncidentTimeline


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    service: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    anomaly: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[str] = mapped_column(
        String,
        default="ACTIVE",
        nullable=False,
    )

    occurrence_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        nullable=False,
    )

    last_alerted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    last_alerted_severity: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    timeline: Mapped[list["IncidentTimeline"]] = relationship(
        "IncidentTimeline",
        back_populates="incident",
        cascade="all, delete-orphan",
        order_by="IncidentTimeline.created_at",
    )
