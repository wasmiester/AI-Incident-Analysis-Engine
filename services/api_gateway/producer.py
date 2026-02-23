import json
from kafka import KafkaProducer
from datetime import datetime, timezone
import uuid

SERVICE_NAME = "api_service"
TOPIC = "metrics"
FAILURE_MODE = "none" #options: none | latency | errors | traffic | mixed

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

def build_metric():
    metric = {
        "id": str(uuid.uuid4()),
        "service": SERVICE_NAME,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error_rate": 0.01,
        "latency_p95": 120.0,
        "request_count": 1000,
    }

    if FAILURE_MODE == "latency":
        metric["latency_p95"] = 2500.0

    elif FAILURE_MODE == "errors":
        metric["error_rate"] = 0.65

    elif FAILURE_MODE == "traffic":
        metric["request_count"] = 15000

    elif FAILURE_MODE == "mixed":
        metric["error_rate"] = 0.7
        metric["latency_p95"] = 3000.0
        metric["request_count"] = 20000

    return metric


def emit_metric():
    metric = build_metric()
    producer.send(TOPIC, metric)
    producer.flush()

    print(
        f" METRIC SENT | service={metric['service']} "
        f"error_rate={metric['error_rate']} "
        f"latency_p95={metric['latency_p95']} "
        f"request_count={metric['request_count']}"
    )


if __name__ == "__main__":
    emit_metric()
