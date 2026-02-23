import json
import argparse
from kafka import KafkaConsumer
from datetime import datetime

from incident_engine.detector import detect_anomaly
from incident_engine.metrics import process_metrics
from incident_engine.service import save_incident


TOPIC = "metrics"
BOOTSTRAP_SERVERS = "localhost:9092"


def run_kafka_consumer():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True,
        group_id="incident-engine",
    )

    print("--Incident consumer started (Kafka mode)... Press Ctrl+C to stop.")

    try:
        for message in consumer:
            metric = message.value
            if isinstance(metric.get("timestamp"), str):
                metric["timestamp"] = datetime.fromisoformat(metric["timestamp"])
            print(f"\n METRIC RECEIVED: {metric}")

            try:
                detection = detect_anomaly(metric)
            except Exception as e:
                print(f"Detection failed: {e}")
                continue

            if not detection.get("anomaly"):
                print("ℹNo anomaly detected — skipping")
                continue

            try:
                incident = save_incident(detection)
                print(
                    f"--INCIDENT | "
                    f"service={incident.service} "
                    f"severity={incident.severity} "
                    f"count={incident.occurrence_count}"
                )
            except Exception as e:
                print(f" Failed to save incident: {e}")

    except KeyboardInterrupt:
        print("\n Consumer interrupted by user. Shutting down")

    finally:
        consumer.close()
        print("Kafka consumer closed.")



def run_batch():
    print("Running batch processor (DB metrics)...")
    process_metrics()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Incident Engine Runner")
    parser.add_argument(
        "--mode",
        choices=["consumer", "batch"],
        default="consumer",
        help="Run mode",
    )
    args = parser.parse_args()

    if args.mode == "batch":
        run_batch()
    else:
        run_kafka_consumer()
