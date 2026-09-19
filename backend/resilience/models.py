from pydantic import BaseModel


class FragilityFactor(BaseModel):
    """A single factor contributing to itinerary fragility."""
    name: str
    score: float  # 0-100, higher = more fragile
    weight: float  # contribution to overall score
    description: str
    affected_activities: list[str] = []  # activity IDs


class ResilienceScore(BaseModel):
    """Proactive fragility assessment of an itinerary.
    
    Runs BEFORE any disruption — this is a proactive metric, not reactive.
    """
    overall: float  # 0-100, higher = more fragile (less resilient)
    rating: str  # "Strong", "Good", "Fragile", "Critical"
    factors: list[FragilityFactor]
    summary: str  # 1-2 sentence human-readable summary

