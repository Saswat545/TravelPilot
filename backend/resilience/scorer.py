"""Resilience Scorer — proactive fragility assessment of itineraries.

IMPORTANT: This runs on the COMPLETE itinerary BEFORE any disruption happens.
It is NOT reactive — it's a proactive risk metric that shows how fragile
a plan is before anything breaks.
"""

from .models import FragilityFactor, ResilienceScore
from scheduler.models import Itinerary, ScheduledActivity


def score_buffer_time(activities: list[ScheduledActivity]) -> FragilityFactor:
    """Score based on buffer time between consecutive activities.
    
    Tight transitions = fragile. Activities with <15min gap are risky.
    """
    if len(activities) < 2:
        return FragilityFactor(
            name="Buffer Time",
            score=0.0,
            weight=0.25,
            description="Single activity — no transition risk",
            affected_activities=[],
        )

    tight_gaps = []
    for i in range(len(activities) - 1):
        curr_end = activities[i].scheduled_end
        next_start = activities[i + 1].scheduled_start
        gap_minutes = (next_start - curr_end).total_seconds() / 60

        # Account for travel time
        effective_buffer = gap_minutes - activities[i + 1].travel_time_from_prev
        if effective_buffer < 15:
            tight_gaps.append(activities[i].activity.id)

    risk_pct = (len(tight_gaps) / max(1, len(activities) - 1)) * 100

    return FragilityFactor(
        name="Buffer Time",
        score=risk_pct,
        weight=0.25,
        description=f"{len(tight_gaps)}/{len(activities)-1} transitions have <15min buffer",
        affected_activities=tight_gaps,
    )


def score_single_point_failures(activities: list[ScheduledActivity]) -> FragilityFactor:
    """Score based on activities with no backup alternatives nearby.
    
    If an activity is the only one in its category for that time slot,
    it's a single point of failure.
    """
    if not activities:
        return FragilityFactor(
            name="Single-Point Failures",
            score=0.0,
            weight=0.30,
            description="No activities to assess",
            affected_activities=[],
        )

    # Group by time proximity (activities within 2 hours are alternatives)
    single_points = []
    for i, act in enumerate(activities):
        category = act.activity.category
        # Check if any other activity in same category exists within 2 hours
        has_alternative = False
        for j, other in enumerate(activities):
            if i == j:
                continue
            if other.activity.category == category:
                time_diff = abs(
                    (act.scheduled_start - other.scheduled_start).total_seconds() / 60
                )
                if time_diff <= 120:  # within 2 hours
                    has_alternative = True
                    break
        if not has_alternative:
            single_points.append(act.activity.id)

    risk_pct = (len(single_points) / max(1, len(activities))) * 100

    return FragilityFactor(
        name="Single-Point Failures",
        score=risk_pct,
        weight=0.30,
        description=f"{len(single_points)}/{len(activities)} activities have no nearby alternative",
        affected_activities=single_points,
    )


def score_time_density(activities: list[ScheduledActivity]) -> FragilityFactor:
    """Score based on how packed the schedule is.
    
    A fully packed day with no gaps is fragile — one delay cascades.
    """
    if not activities:
        return FragilityFactor(
            name="Time Density",
            score=0.0,
            weight=0.20,
            description="No activities",
            affected_activities=[],
        )

    total_span = 0.0
    total_activity = 0.0

    if len(activities) >= 2:
        first_start = activities[0].scheduled_start
        last_end = activities[-1].scheduled_end
        total_span = (last_end - first_start).total_seconds() / 60

    for act in activities:
        total_activity += (act.scheduled_end - act.scheduled_start).total_seconds() / 60

    if total_span == 0:
        density = 0.0
    else:
        density = (total_activity / total_span) * 100

    # High density = fragile (over 85% packed is risky)
    risk = max(0, density - 70) * (100 / 30)  # scale 70-100% to 0-100
    risk = min(100, risk)

    crowded = [a.activity.id for a in activities if a.travel_time_from_prev < 5]

    return FragilityFactor(
        name="Time Density",
        score=risk,
        weight=0.20,
        description=f"Schedule is {density:.0f}% packed — delays will cascade",
        affected_activities=crowded,
    )


def score_category_diversity(activities: list[ScheduledActivity]) -> FragilityFactor:
    """Score based on over-reliance on one category.
    
    If 50%+ activities are the same category, losing that category
    (e.g., weather cancels all outdoor activities) is catastrophic.
    """
    if not activities:
        return FragilityFactor(
            name="Category Diversity",
            score=0.0,
            weight=0.15,
            description="No activities",
            affected_activities=[],
        )

    category_counts: dict[str, int] = {}
    for act in activities:
        cat = act.activity.category
        category_counts[cat] = category_counts.get(cat, 0) + 1

    if not category_counts:
        return FragilityFactor(
            name="Category Diversity",
            score=0.0,
            weight=0.15,
            description="No categories found",
            affected_activities=[],
        )

    max_count = max(category_counts.values())
    dominant_pct = (max_count / len(activities)) * 100

    # Over-reliance risk: >60% in one category is fragile
    risk = max(0, dominant_pct - 40) * (100 / 60)
    risk = min(100, risk)

    dominant_cat = max(category_counts, key=category_counts.get)
    affected = [
        a.activity.id for a in activities
        if a.activity.category == dominant_cat
    ]

    return FragilityFactor(
        name="Category Diversity",
        score=risk,
        weight=0.15,
        description=f"{dominant_pct:.0f}% of activities are {dominant_cat}",
        affected_activities=affected,
    )


def compute_resilience(itinerary: Itinerary) -> ResilienceScore:
    """Compute proactive resilience score for a complete itinerary.
    
    This runs BEFORE any disruption — it's a proactive risk metric.
    Higher score = more fragile (less resilient).
    """
    all_activities = []
    for day in itinerary.days:
        all_activities.extend(day.activities)

    if not all_activities:
        return ResilienceScore(
            overall=0.0,
            rating="N/A",
            factors=[],
            summary="No activities to assess.",
        )

    factors = [
        score_buffer_time(all_activities),
        score_single_point_failures(all_activities),
        score_time_density(all_activities),
        score_category_diversity(all_activities),
    ]

    # Weighted average
    total_weight = sum(f.weight for f in factors)
    overall = sum(f.score * f.weight for f in factors) / max(0.01, total_weight)

    # Rating
    if overall < 25:
        rating = "Strong"
    elif overall < 50:
        rating = "Good"
    elif overall < 75:
        rating = "Fragile"
    else:
        rating = "Critical"

    # Build summary
    high_risk = [f for f in factors if f.score > 50]
    if high_risk:
        risk_names = ", ".join(f.name for f in high_risk)
        summary = f"Itinerary rated {rating}. Key risks: {risk_names}."
    else:
        summary = f"Itinerary rated {rating} with manageable risk across all factors."

    return ResilienceScore(
        overall=round(overall, 1),
        rating=rating,
        factors=factors,
        summary=summary,
    )
