from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean
from incident_engine.db.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class Metric(Base):
    __tablename__ = "metric_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    error_rate = Column(Float)
    latency_p95 = Column(Float)
    request_count = Column(Integer)
    processed = Column(Boolean, default=False )

    
