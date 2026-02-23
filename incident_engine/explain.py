def explain_anomaly(metrics: dict, score: float) -> list[str]:
    explanations = []

    if score < -0.2:
        explanations.append("severe deviation from normal behavior")
    elif score < -0.1:
        explanations.append("moderate deviation from baseline")
    else:
        explanations.append("multi-dimensional anomaly detected")

    if "latency" in metrics and metrics["latency"] > 1000:
        explanations.append("high service latency")

    if "error_rate" in metrics and metrics["error_rate"] > 0.05:
        explanations.append("elevated error rate")

    if not explanations:
        explanations.append("statistical anomaly detected")

    return explanations
