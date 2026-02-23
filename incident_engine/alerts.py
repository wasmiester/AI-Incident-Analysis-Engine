
from datetime import datetime, timedelta, timezone

_RECENT_ALERTS = {}

DEDUP_WINDOW = timedelta(minutes=5)


def send_alert(service: str, severity: str, explanation):
    print("\n ALERT [{}]".format(severity))
    print(f"Service:".format(service))
    print(f"Explanation: ".format(explanation))



def trigger_alert(incident):
    print(
        f"\n ALERT [{incident.severity}]"
        f"\nService: {incident.service}"
        f"\nCount: {incident.occurrence_count}"
        f"\nStatus: {incident.status}"
    )


def should_alert(incident: dict) -> bool:
    key = (incident["service"], incident["severity"])
    now = datetime.now(timezone.utc)

    last_alert = _RECENT_ALERTS.get(key)
    if last_alert and now - last_alert < DEDUP_WINDOW:
        return False

    _RECENT_ALERTS[key] = now
    return True


def route_by_severity(severity: str) -> str:
    if severity in {"HIGH", "CRITICAL"}:
        return "urgent"
    return "standard"
