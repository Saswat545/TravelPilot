"""Repair Agent — minimal-diff repair for disrupted itineraries.

The key constraint: NEVER regenerate the full itinerary.
Find the smallest set of changes to fix the broken plan.
Output a structured diff that the frontend renders directly.
"""

from datetime import datetime, timedelta
from scheduler.models import Activity, ScheduledActivity, Itinerary
from scheduler.engine import estimate_travel_minutes, fits_in_window
from .models import DiffEntry, RepairResult


def find_alternative(
    broken_activity: Activity,
    candidate_pool: list[Activity],
    context_location: tuple[float, float],
    context_time: datetime,
    max_travel_minutes: float = 30.0,
) -> Activity | None:
    """Find the best alternative activity from the candidate pool.
    
    Scoring: closer is better, same category is better, fits time window is required.
    Returns None if no suitable alternative exists (edge case).
    """
    if not candidate_pool:
        return None

    best = None
    best_score = float("inf")

    for candidate in candidate_pool:
        # Skip the broken activity itself
        if candidate.id == broken_activity.id:
            continue

        # Must fit in the time window
        if candidate.time_window:
            est_start = context_time
            est_end = est_start + timedelta(minutes=candidate.duration_minutes)
            if not fits_in_window(est_start, est_end, candidate.time_window):
                continue

        # Calculate travel time from context
        travel = estimate_travel_minutes(context_location, candidate.location)

        # Skip if too far
        if travel > max_travel_minutes:
            continue

        # Score: lower is better
        # Prioritize: same category (0 or -10), distance (travel minutes)
        category_bonus = -10 if candidate.category == broken_activity.category else 0
        score = travel + category_bonus

        if score < best_score:
            best_score = score
            best = candidate

    return best


def compute_shifted_times(
    day_activities: list[ScheduledActivity],
    removed_index: int,
    removed_duration: float,
) -> list[tuple[str, datetime, datetime]]:
    """After removing an activity, compute new times for subsequent activities.
    
    Returns list of (activity_id, new_start, new_end) for activities that shifted.
    """
    shifts = []
    if removed_index >= len(day_activities) - 1:
        return shifts  # Nothing after the removed activity

    # Time freed up = removed activity's duration + its travel to next
    removed = day_activities[removed_index]
    time_freed = (removed.scheduled_end - removed.scheduled_start).total_seconds() / 60

    # Shift subsequent activities earlier
    for i in range(removed_index + 1, len(day_activities)):
        act = day_activities[i]
        new_start = act.scheduled_start - timedelta(minutes=time_freed)
        new_end = act.scheduled_end - timedelta(minutes=time_freed)

        # Check if new time is valid (doesn't conflict with previous activity)
        if i > removed_index + 1:
            prev_end = shifts[-1][2] if shifts else day_activities[removed_index - 1].scheduled_end
            gap = (new_start - prev_end).total_seconds() / 60
            if gap < 0:
                # Can't shift that much — partial shift
                new_start = prev_end + timedelta(minutes=5)
                new_end = new_start + timedelta(minutes=act.activity.duration_minutes)

        shifts.append((act.activity.id, new_start, new_end))

    return shifts


def repair_itinerary(
    itinerary: Itinerary,
    disruption_activity_id: str,
    disruption_type: str,
    disruption_reason: str,
    candidate_pool: list[Activity] | None = None,
) -> RepairResult:
    """Perform minimal-diff repair on a disrupted itinerary.
    
    EDGE CASE: If no alternative is found, returns a degraded result
    instead of crashing or silently regenerating everything.
    """
    # Find the broken activity across all days
    broken_activity = None
    broken_day_idx = None
    broken_act_idx = None

    for day_idx, day in enumerate(itinerary.days):
        for act_idx, sched in enumerate(day.activities):
            if sched.activity.id == disruption_activity_id:
                broken_activity = sched.activity
                broken_day_idx = day_idx
                broken_act_idx = act_idx
                break
        if broken_activity:
            break

    if not broken_activity:
        return RepairResult(
            success=False,
            original_activity_id=disruption_activity_id,
            original_activity_name="Unknown",
            disruption_type=disruption_type,
            disruption_reason=disruption_reason,
            diff_entries=[],
            explanation=f"Activity {disruption_activity_id} not found in itinerary.",
            activities_changed=0,
            time_saved_minutes=0,
            cost_delta=0,
            degraded=True,
            degradation_reason="Activity not found in itinerary.",
        )

    day = itinerary.days[broken_day_idx]
    broken_sched = day.activities[broken_act_idx]

    # Use provided candidate pool or empty list
    pool = candidate_pool or []

    # Try to find alternative
    context_time = broken_sched.scheduled_start
    context_location = (
        day.activities[broken_act_idx - 1].activity.location
        if broken_act_idx > 0
        else (0.0, 0.0)
    )

    alternative = find_alternative(
        broken_activity, pool, context_location, context_time
    )

    diff_entries = []

    if alternative:
        # SUCCESS: Found alternative — minimal diff
        travel_change = estimate_travel_minutes(context_location, alternative.location)

        diff_entries.append(DiffEntry(
            type="modified",
            activity_id=broken_activity.id,
            activity_name=broken_activity.name,
            field="activity",
            old_value=broken_activity.name,
            new_value=alternative.name,
            reason=f"Replaced with {alternative.name} — {travel_change:.0f}min travel, same category",
        ))

        # Check if timing changed
        new_end = context_time + timedelta(minutes=alternative.duration_minutes)
        if abs((new_end - broken_sched.scheduled_end).total_seconds() / 60) > 5:
            diff_entries.append(DiffEntry(
                type="shifted",
                activity_id=alternative.id,
                activity_name=alternative.name,
                field="time",
                old_value=f"{broken_sched.scheduled_start.strftime('%H:%M')}-{broken_sched.scheduled_end.strftime('%H:%M')}",
                new_value=f"{context_time.strftime('%H:%M')}-{new_end.strftime('%H:%M')}",
                reason=f"Duration changed from {broken_activity.duration_minutes}min to {alternative.duration_minutes}min",
            ))

        # Check cost difference
        cost_delta = alternative.cost - broken_activity.cost
        if abs(cost_delta) > 1:
            diff_entries.append(DiffEntry(
                type="modified",
                activity_id=alternative.id,
                activity_name=alternative.name,
                field="cost",
                old_value=f"${broken_activity.cost:.0f}",
                new_value=f"${alternative.cost:.0f}",
                reason=f"Cost {'increased' if cost_delta > 0 else 'decreased'} by ${abs(cost_delta):.0f}",
            ))

        # Check if subsequent activities shifted
        shifts = compute_shifted_times(day.activities, broken_act_idx, broken_activity.duration_minutes)
        for act_id, new_start, new_end in shifts:
            orig = next((a for a in day.activities if a.activity.id == act_id), None)
            if orig:
                diff_entries.append(DiffEntry(
                    type="shifted",
                    activity_id=act_id,
                    activity_name=orig.activity.name,
                    field="time",
                    old_value=f"{orig.scheduled_start.strftime('%H:%M')}-{orig.scheduled_end.strftime('%H:%M')}",
                    new_value=f"{new_start.strftime('%H:%M')}-{new_end.strftime('%H:%M')}",
                    reason="Shifted earlier to fill gap",
                ))

        explanation = (
            f"Replaced {broken_activity.name} with {alternative.name}. "
            f"Travel time: {estimate_travel_minutes(context_location, alternative.location):.0f}min. "
            f"{'Cost difference: $' + f'{abs(cost_delta):.0f}' if abs(cost_delta) > 1 else 'Similar cost'}."
        )

        return RepairResult(
            success=True,
            original_activity_id=broken_activity.id,
            original_activity_name=broken_activity.name,
            disruption_type=disruption_type,
            disruption_reason=disruption_reason,
            diff_entries=diff_entries,
            explanation=explanation,
            activities_changed=1 + len(shifts),
            time_saved_minutes=0,
            cost_delta=alternative.cost - broken_activity.cost,
            degraded=False,
        )

    else:
        # EDGE CASE: No alternative found — degrade gracefully
        # Instead of crashing, remove the activity and shift everything up
        shifts = compute_shifted_times(day.activities, broken_act_idx, broken_activity.duration_minutes)

        diff_entries.append(DiffEntry(
            type="removed",
            activity_id=broken_activity.id,
            activity_name=broken_activity.name,
            field="activity",
            old_value=broken_activity.name,
            new_value=None,
            reason=f"No viable alternative found for {broken_activity.category} activity",
        ))

        for act_id, new_start, new_end in shifts:
            orig = next((a for a in day.activities if a.activity.id == act_id), None)
            if orig:
                diff_entries.append(DiffEntry(
                    type="shifted",
                    activity_id=act_id,
                    activity_name=orig.activity.name,
                    field="time",
                    old_value=f"{orig.scheduled_start.strftime('%H:%M')}-{orig.scheduled_end.strftime('%H:%M')}",
                    new_value=f"{new_start.strftime('%H:%M')}-{new_end.strftime('%H:%M')}",
                    reason="Shifted earlier to fill gap",
                ))

        # Calculate freed time
        time_freed = (broken_sched.scheduled_end - broken_sched.scheduled_start).total_seconds() / 60

        explanation = (
            f"No suitable alternative found for {broken_activity.name}. "
            f"Activity removed — {time_freed:.0f}min freed. "
            f"Subsequent activities shifted earlier."
        )

        return RepairResult(
            success=True,
            original_activity_id=broken_activity.id,
            original_activity_name=broken_activity.name,
            disruption_type=disruption_type,
            disruption_reason=disruption_reason,
            diff_entries=diff_entries,
            explanation=explanation,
            activities_changed=1 + len(shifts),
            time_saved_minutes=time_freed,
            cost_delta=-broken_activity.cost,
            degraded=True,
            degradation_reason="No alternative venue found in candidate pool.",
        )
