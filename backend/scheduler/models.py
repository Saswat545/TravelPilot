from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TimeWindow(BaseModel):
    earliest: datetime
    latest: datetime


class Activity(BaseModel):
    id: str
    name: str
    location: tuple[float, float]  # lat, lng
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    time_window: Optional[TimeWindow] = None
    duration_minutes: float = 60.0
    category: str
    cost: float = 0.0
    priority: int = 1
    description: str = ""


class ScheduledActivity(BaseModel):
    activity: Activity
    scheduled_start: datetime
    scheduled_end: datetime
    travel_time_from_prev: float = 0.0  # minutes
    day_index: int = 0


class ItineraryDay(BaseModel):
    day_index: int
    date: datetime
    activities: list[ScheduledActivity]
    total_travel_minutes: float = 0.0
    total_activity_minutes: float = 0.0


class Itinerary(BaseModel):
    destination: str
    days: list[ItineraryDay]
    total_cost: float = 0.0
    total_travel_minutes: float = 0.0
    resilience_score: float = 0.0
