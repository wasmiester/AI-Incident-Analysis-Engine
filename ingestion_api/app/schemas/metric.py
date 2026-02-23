from pydantic import BaseModel
from datetime import datetime

class MetricCreate(BaseModel):
    service: str
    timestamp: datetime
    latency_p95: float
    error_rate: float
    request_count: int
