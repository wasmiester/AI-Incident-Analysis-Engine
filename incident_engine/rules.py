from collections import Counter
from typing import List, Dict

def determine_root_service(events: List[Dict]) -> str:
    
    error_events = [e for e in events if e["level"] == "ERROR"]

    if not error_events:
        raise ValueError("Cannot determine root service from empty event list")

    error_events.sort(key=lambda x: x["timestamp"])
    return error_events[0]["service"]
