from datetime import datetime
from uuid import uuid4
from incident_engine.models.incident import Incident
from incident_engine.rules import determine_root_service
def correlate(incident):
    if incident.occurrence_count >= 3:
        return "RECURRING"

    return "ISOLATED"
