from dataclasses import dataclass

ERROR_RATE_THRESHOLD = 0.05
LATENCY_THRESHOLD_MS = 500


@dataclass
class MetricSnapshot:
    service: str
    error_rate: float
    latency_p95: float
    request_count: int


def analyze_incident(incident):
    return {
        "service": incident.service,
        "severity": incident.severity,
        "occurrences": incident.occurrence_count,
        "first_seen": incident.first_seen,
        "last_seen": incident.last_seen,
    }


def _severity(signals: list[str]) -> str:
    if "HIGH_ERROR_RATE" in signals and "HIGH_LATENCY" in signals:
        return "CRITICAL"
    if "HIGH_ERROR_RATE" in signals or "HIGH_LATENCY" in signals:
        return "HIGH"
    return "LOW"
