from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from ingestion_api.app.db.database import Base, SessionLocal, engine

class LogEvent(Base):
    __tablename__ = "log_events"

    id = Column(Integer, primary_key=True)
    service_name = Column(String, index=True)
    level = Column(String)
    message = Column(String)
    metadata = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
