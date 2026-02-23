def extract_features(metrics: dict) -> dict:
    return {
        "error_rate": float(metrics["error_rate"]),
        "latency_p95": float(metrics["latency_p95"]),
        "request_count": float(metrics["request_count"]),
    }
