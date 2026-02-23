from pydantic import BaseModel
from datetime import datetime, UTC

class LogEventCreate(BaseModel):
    service: str
    level: str
    message: str
    timestamp: datetime
