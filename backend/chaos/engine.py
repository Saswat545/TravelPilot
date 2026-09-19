"""Chaos Engine — deterministic disruption injection for demo.

Build a manually-triggerable "Chaos Mode" button for the demo.
Do not rely on real-time disruption feeds — simulate this deterministically
so the demo is reliable.
"""

import random
from scheduler.models import Itinerary
from repair.agent import repair_itinerary


class Disruption:
    """Represents a disruption event."""

    def __init__(self, activity_id: str, activity_name: str,
                 disruption_type: str, reason: str):
        self.activity_id = activity_id
        self.activity_name = activity_name
        self.disruption_type = disruption_type
        self.reason = reason


DISRUPTION_TYPES = [
    ("closure", "Venue unexpectedly closed for maintenance"),
    ("weather", "Severe weather warning — outdoor activity unsafe"),
    ("overbooked", "Fully booked — no remaining availability"),
    ("cancelled", "Event cancelled by organizer"),
]


def inject_disruption(
    itinerary: Itinerary,
    target_activity_id: str | None = None,
) -> Disruption:
    """Inject a disruption into the itinerary.
    
    If target_activity_id is provided, disrupt that specific activity.
    Otherwise, pick a random non-transport activity.
    """
    # Collect all non-transport activities
    candidates = []
    for day in itinerary.days:
        for sched in day.activities:
            if sched.activity.category != "transport":
                candidates.append(sched)

    if not candidates:
        raise ValueError("No activities to disrupt")

    if target_activity_id:
        target = next(
            (c for c in candidates if c.activity.id == target_activity_id),
            None,
        )
        if not target:
            raise ValueError(f"Activity {target_activity_id} not found")
    else:
        target = random.choice(candidates)

    # Pick random disruption type
    dtype, reason = random.choice(DISRUPTION_TYPES)

    return Disruption(
        activity_id=target.activity.id,
        activity_name=target.activity.name,
        disruption_type=dtype,
        reason=reason,
    )


def trigger_chaos(
    itinerary: Itinerary,
    candidate_pool: list = None,
    target_activity_id: str | None = None,
) -> dict:
    """Full chaos pipeline: inject disruption → repair → return result.
    
    Returns dict with disruption info + repair result for the frontend.
    """
    disruption = inject_disruption(itinerary, target_activity_id)

    repair = repair_itinerary(
        itinerary=itinerary,
        disruption_activity_id=disruption.activity_id,
        disruption_type=disruption.disruption_type,
        disruption_reason=disruption.reason,
        candidate_pool=candidate_pool,
    )

    return {
        "disruption": {
            "activity_id": disruption.activity_id,
            "activity_name": disruption.activity_name,
            "type": disruption.disruption_type,
            "reason": disruption.reason,
        },
        "repair": repair.model_dump(),
    }
