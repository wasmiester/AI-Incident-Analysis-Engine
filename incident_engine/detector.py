from datetime import timezone, timedelta, datetime
from pathlib import Path
from typing import Optional
import joblib
import pandas as pd

MODEL_PATH = Path("models/anomaly_model.joblib")
SEVERITY_ORDER = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
ALERT_COOLDOWN_MINUTES = 10

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Anomaly model not found at {MODEL_PATH}. Train the model first."
        )
    return joblib.load(MODEL_PATH)


model = load_model()


def _normalize_metrics(metrics):
    if isinstance(metrics, dict):
        return metrics

    return {
        "service": metrics.service_name,
        "error_rate": metrics.error_rate,
        "latency_p95": metrics.latency_p95,
        "request_count": metrics.request_count,
        "timestamp": metrics.timestamp,
    }


def detect_anomaly(metrics: dict) -> dict:
    metrics = _normalize_metrics(metrics)

    features = pd.DataFrame(
    [[
        metrics["error_rate"],
        metrics["latency_p95"],
        metrics["request_count"],
    ]],
    columns=["error_rate", "latency_p95", "request_count"]
)

    score = model.decision_function(features)[0]
    prediction = model.predict(features)[0]

    is_anomaly = prediction == -1

    explanation = []
    if is_anomaly:
        explanation.append("multi-dimensional anomaly detected")

    return {
        "service": metrics["service"],
        "timestamp": metrics["timestamp"].replace(tzinfo=timezone.utc),
        "anomaly": is_anomaly,
        "score": float(score),
        "explanation": explanation,
        "severity": _severity_from_score(score),
    }


def _severity_from_score(score: float) -> str:
    if score < -0.2:
        return "CRITICAL"
    if score < -0.1:
        return "HIGH"
    if score < -0.05:
        return "MEDIUM"
    return "LOW"

def severity_rank(severity: str) -> int:
    try:
        return SEVERITY_ORDER.index(severity)
    except ValueError:
        return 0


def escalate_severity(
    current_severity: str,
    occurrence_count: int,
    first_seen: datetime,
    now: Optional[datetime] = None,
) -> str:
    """
    Escalation rules:
    - >= 3 occurrences   → MEDIUM
    - >= 7 occurrences   → HIGH
    - >= 15 occurrences  → CRITICAL
    - >= 10 minutes open → +1 level
    - >= 30 minutes open → CRITICAL
    Severity never downgrades.
    """
    if first_seen.tzinfo is None:
        first_seen = first_seen.replace(tzinfo=timezone.utc)

    now = now or datetime.now(timezone.utc)
    duration = now - first_seen
    proposed = current_severity

    if occurrence_count >= 15:
        proposed = "CRITICAL"
    elif occurrence_count >= 7:
        proposed = "HIGH"
    elif occurrence_count >= 3:
        proposed = "MEDIUM"

    if duration >= timedelta(minutes=30):
        proposed = "CRITICAL"
    elif duration >= timedelta(minutes=10):
        rank = min(
            severity_rank(proposed) + 1,
            severity_rank("CRITICAL"),
        )
        proposed = SEVERITY_ORDER[rank]

    if severity_rank(proposed) < severity_rank(current_severity):
        return current_severity

    return proposed