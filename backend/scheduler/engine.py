"""Core scheduling engine — greedy nearest-neighbor + time-window pruning.

This is the algorithmic differentiator: LLMs are bad at spatial/temporal
constraint reasoning. We use a real algorithm here.
"""

from datetime import datetime, timedelta
from .models import (
    Activity,
    ScheduledActivity,
    ItineraryDay,
    Itinerary,
    TimeWindow,
)
import math


def haversine_distance(
    coord1: tuple[float, float], coord2: tuple[float, float]
) -> float:
    """Calculate distance in km between two lat/lng points."""
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    return 2 * 6371 * math.asin(math.sqrt(a))


def estimate_travel_minutes(
    coord1: tuple[float, float], coord2: tuple[float, float],
    speed_kmh: float = 30.0
) -> float:
    """Estimate travel time in minutes between two points."""
    dist_km = haversine_distance(coord1, coord2)
    return (dist_km / speed_kmh) * 60


def fits_in_window(
    start: datetime, end: datetime, window: TimeWindow
) -> bool:
    """Check if a time slot fits within the activity's time window."""
    return start >= window.earliest and end <= window.latest


def schedule_day(
    activities: list[Activity],
    day_date: datetime,
    day_start_hour: int = 9,
    day_end_hour: int = 21,
    speed_kmh: float = 30.0,
) -> ItineraryDay:
    """Schedule activities for a single day using greedy nearest-neighbor.

    Algorithm:
    1. Start at day_start_hour
    2. From current position, pick the nearest activity that fits in its time window
    3. Schedule it, move to its location, advance time
    4. Repeat until no more activities fit
    """
    current_time = day_date.replace(hour=day_start_hour, minute=0, second=0)
    day_end = day_date.replace(hour=day_end_hour, minute=0, second=0)
    current_location = (0.0, 0.0)  # Will be set to first activity

    scheduled = []
    remaining = list(activities)

    # Sort by priority (highest first), then by time window earliest
    remaining.sort(key=lambda a: (-a.priority, a.time_window.earliest if a.time_window else day_date))

    if remaining:
        # Start with the highest-priority activity
        first = remaining.pop(0)
        first_start = max(current_time, first.time_window.earliest if first.time_window else current_time)
        first_end = first_start + timedelta(minutes=first.duration_minutes)

        if first_end <= day_end:
            scheduled.append(ScheduledActivity(
                activity=first,
                scheduled_start=first_start,
                scheduled_end=first_end,
                travel_time_from_prev=0.0,
                day_index=0,
            ))
            current_time = first_end
            current_location = first.location

    while remaining and current_time < day_end:
        best_activity = None
        best_start = None
        best_end = None
        best_travel = float("inf")

        for act in remaining:
            # Estimate travel time from current location
            travel = estimate_travel_minutes(current_location, act.location, speed_kmh)
            earliest_arrival = current_time + timedelta(minutes=travel)

            # If activity has a time window, wait for it to open if needed
            if act.time_window and earliest_arrival < act.time_window.earliest:
                earliest_arrival = act.time_window.earliest

            act_start = earliest_arrival
            act_end = act_start + timedelta(minutes=act.duration_minutes)

            # Check if it fits in the day and in the activity's time window
            if act_end > day_end:
                continue
            if act.time_window and not fits_in_window(act_start, act_end, act.time_window):
                continue

            # Pick the nearest feasible activity
            if travel < best_travel:
                best_activity = act
                best_start = act_start
                best_end = act_end
                best_travel = travel

        if best_activity is None:
            break

        remaining.remove(best_activity)
        scheduled.append(ScheduledActivity(
            activity=best_activity,
            scheduled_start=best_start,
            scheduled_end=best_end,
            travel_time_from_prev=best_travel,
            day_index=0,
        ))
        current_time = best_end
        current_location = best_activity.location

    total_travel = sum(s.travel_time_from_prev for s in scheduled)
    total_activity = sum(
        (s.scheduled_end - s.scheduled_start).total_seconds() / 60
        for s in scheduled
    )

    return ItineraryDay(
        day_index=0,
        date=day_date,
        activities=scheduled,
        total_travel_minutes=total_travel,
        total_activity_minutes=total_activity,
    )


def schedule_itinerary(
    activities: list[Activity],
    destination: str,
    start_date: datetime,
    num_days: int = 1,
    day_start_hour: int = 9,
    day_end_hour: int = 21,
) -> Itinerary:
    """Schedule a multi-day itinerary.

    Distributes activities across days, then schedules each day.
    """
    # Sort all activities by priority (highest first)
    sorted_acts = sorted(activities, key=lambda a: -a.priority)

    # Group by day based on time window dates
    day_groups: dict[int, list[Activity]] = {}
    for act in sorted_acts:
        if act.time_window:
            day_num = (act.time_window.earliest.date() - start_date.date()).days
        else:
            day_num = 0
        day_num = max(0, min(day_num, num_days - 1))
        day_groups.setdefault(day_num, []).append(act)

    # If one day has too many activities and other days are empty,
    # redistribute evenly and reassign time windows to target day
    max_per_day = 5
    if num_days > 1:
        for day_idx in list(day_groups.keys()):
            if len(day_groups[day_idx]) > max_per_day:
                overflow = day_groups[day_idx][max_per_day:]
                day_groups[day_idx] = day_groups[day_idx][:max_per_day]
                for i, act in enumerate(overflow):
                    target = (day_idx + 1 + i) % num_days
                    # Reassign time window to target day so schedule_day can place it
                    if act.time_window:
                        target_date = start_date + timedelta(days=target)
                        orig_time = act.time_window.earliest.time()
                        act.time_window = TimeWindow(
                            earliest=target_date.replace(hour=orig_time.hour, minute=orig_time.minute),
                            latest=target_date.replace(hour=act.time_window.latest.hour, minute=act.time_window.latest.minute),
                        )
                    day_groups.setdefault(target, []).append(act)

    days = []
    total_travel = 0.0

    for day_idx in range(num_days):
        day_date = start_date + timedelta(days=day_idx)
        day_acts = day_groups.get(day_idx, [])

        if not day_acts:
            # Empty day
            days.append(ItineraryDay(
                day_index=day_idx,
                date=day_date,
                activities=[],
                total_travel_minutes=0.0,
                total_activity_minutes=0.0,
            ))
            continue

        day = schedule_day(
            day_acts, day_date, day_start_hour, day_end_hour
        )
        day.day_index = day_idx
        days.append(day)
        total_travel += day.total_travel_minutes

    total_cost = sum(
        act.activity.cost
        for day in days
        for act in day.activities
    )

    return Itinerary(
        destination=destination,
        days=days,
        total_cost=total_cost,
        total_travel_minutes=total_travel,
    )
