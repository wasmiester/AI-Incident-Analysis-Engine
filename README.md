# AI Incident Analysis Engine

An incident detection and management system that uses **unsupervised machine learning** to detect anomalies in service metrics, correlate them into incidents, escalate severity over time, and automatically resolve incidents once systems recover.

This project simulates how modern SRE / DevOps teams use AI to reduce alert fatigue and respond faster to real production issues.

---

## What This Project Does

- Ingests real-time service metrics via Kafka
- Detects anomalies using **machine learning (Isolation Forest)**
- Correlates repeated anomalies into a single incident
- Escalates severity based on duration & frequency
- Automatically resolves incidents when metrics recover
- Maintains a full incident timeline for auditing & RCA

## Where the AI Is Used

This system uses **unsupervised machine learning**, not hard-coded rules.

### Machine Learning Model
- **Algorithm**: Isolation Forest
- **Type**: Unsupervised anomaly detection
- **Inputs**:
  - error_rate
  - latency_p95
  - request_count

The model learns what *normal behavior* looks like and flags unusual combinations of metrics — even when individual values might appear acceptable in isolation.

### Why This Matters
Traditional alerting systems rely on static thresholds:
if error_rate > 0.5 → alert


This system instead answers:
> “Is this behavior abnormal compared to how this service usually behaves?”

This makes it far more resilient to traffic spikes, seasonal patterns, and noisy metrics.

## Architecture Overview

      ┌────────────────────┐
      │   Test Services    │
      │ (API, DB, Auth)    │
      └─────────┬──────────┘
                │
           Kafka Metrics
                │
                ▼
    ┌──────────────────────────┐
    │ Kafka Consumer           │
    │ (incident_engine)        │
    └─────────┬────────────────┘
              │
    ┌─────────▼──────────┐
    │ ML Anomaly Detector│
    │ Isolation Forest   │
    └─────────┬──────────┘
              │
    ┌─────────▼────────────┐
    │ Incident Management  │
    │ - Deduplication      │
    │ - Escalation         │
    │ - Auto Resolution    │
    └─────────┬────────────┘
              │
    ┌─────────▼────────────┐
    │ PostgreSQL           │
    │ incidents / timeline │
    └──────────────────────┘

## Key Components

- `consumer.py`  
  Kafka consumer that processes metrics in real time

- `detector.py`  
  ML anomaly detection logic

- `service.py`  
  Incident lifecycle management (create, escalate, resolve)

- `severity.py`  
  Time-based severity escalation logic

- `models/incident.py`  
  SQLAlchemy incident model

- `models/timeline.py`  
  Incident timeline (audit trail)

## How to Run & Test

### 1) Create & activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Start the Consumer
```bash
python -m incident_engine.consumer
```
### 4) Emit Test Metrics
#### Normal behavior:
```bash
python services/test_service/producer.py
```

#### Force anomalies:
```bash
FAILURE_MODE=latency python services/test_service/producer.py
FAILURE_MODE=errors python services/test_service/producer.py
FAILURE_MODE=meltdown python services/test_service/producer.py
```

#### Supported failure modes:

none – healthy metrics

latency – high latency

errors – elevated error rate

meltdown – critical system failure

#### Verify Incidents
SELECT service, severity, status, occurrence_count
FROM incidents
ORDER BY last_seen DESC;

# Incident Lifecycle
Anomaly detected

Incident created (or updated if already active)

Severity escalates with repeated failures

Incident auto-resolves when metrics normalize

Timeline records all state changes

# Real-World Use Cases
Microservice health monitoring

SRE alert fatigue reduction

Intelligent incident correlation

AI-assisted observability platforms

Foundation for auto-remediation systems

# Future Enhancements
Model retraining from live metrics

Per-service ML models

Alerting integrations (Slack, PagerDuty)

Auto-remediation hooks

Visualization dashboard
# AI-Incident-Analysis-Engine
