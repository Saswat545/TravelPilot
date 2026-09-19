from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DiffEntry(BaseModel):
    """Single change in an itinerary repair.
    
    This is the structured contract between backend and frontend.
    The frontend renders these directly — no parsing gymnastics needed.
    """
    type: str  # "removed" | "added" | "modified" | "shifted"
    activity_id: str
    activity_name: str
    field: Optional[str] = None  # which field changed: "time", "location", "activity"
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    reason: str


class RepairResult(BaseModel):
    """Complete repair output with structured diff.
    
    This is the API response shape — frontend renders diff_entries directly.
    """
    success: bool
    original_activity_id: str
    original_activity_name: str
    disruption_type: str
    disruption_reason: str

    # Structured diff — the frontend highlights these
    diff_entries: list[DiffEntry]

    # Human-readable explanation (from LLM, for reasoning trace)
    explanation: str

    # Impact summary
    activities_changed: int
    time_saved_minutes: float  # negative if repair made things tighter
    cost_delta: float  # positive = more expensive, negative = cheaper

    # Edge case: what happens when no alternative exists
    degraded: bool = False  # True if repair couldn't find a good fix
    degradation_reason: Optional[str] = None  # e.g., "No alternative venues found in category"
