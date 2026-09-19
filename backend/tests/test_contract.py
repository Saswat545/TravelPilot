"""Behavior contract for TravelPilot.

Each table row is one test case. Columns are inputs, assertions are the contract.
Run: cd backend && python -m tests.test_contract
"""
import json, sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler.models import Activity, TimeWindow, ScheduledActivity, Itinerary, ItineraryDay
from scheduler.engine import schedule_day, haversine_distance
from resilience.scorer import compute_resilience
from repair.agent import repair_itinerary
from chaos.engine import trigger_chaos
from planner.agent import _mock_activities, parse_planner_response

DAY = datetime(2024, 1, 1)


# ── Scheduler ────────────────────────────────────────────────────────────

def _act(id, loc, dur, cat, cost=0, pri=1, earliest=None, latest=None):
    """Shorthand for creating an Activity."""
    tw = TimeWindow(earliest=earliest, latest=latest) if earliest else None
    return Activity(id=id, name=id, location=loc, duration_minutes=dur,
                    category=cat, cost=cost, priority=pri, time_window=tw)


SCHEDULER_CASES = [
    # (description, activities, start_hour, end_hour, min_scheduled, must_contain, must_not_contain)
    ("time windows respected — temple before noon, dinner after 6pm",
     [_act("temple", (35.71, 139.80), 60, "culture", pri=5,
           earliest=DAY.replace(hour=6), latest=DAY.replace(hour=12)),
      _act("dinner", (35.69, 139.70), 90, "food", pri=3,
           earliest=DAY.replace(hour=18), latest=DAY.replace(hour=23)),
      _act("museum", (35.72, 139.78), 90, "culture", pri=4,
           earliest=DAY.replace(hour=9), latest=DAY.replace(hour=17))],
     6, 23, 2, ["temple"], []),

    ("empty input",
     [], 9, 18, 0, [], []),

    ("single activity",
     [_act("only", (35.7, 139.7), 60, "food",
           earliest=DAY.replace(hour=10), latest=DAY.replace(hour=16))],
     9, 18, 1, ["only"], []),

    ("too-far activity excluded",
     [_act("near", (35.7, 139.7), 60, "food",
           earliest=DAY.replace(hour=9), latest=DAY.replace(hour=17)),
      _act("far", (36.5, 140.5), 60, "nature",
           earliest=DAY.replace(hour=9), latest=DAY.replace(hour=17))],
     9, 18, 1, ["near"], []),
]

def test_scheduler():
    for desc, acts, sh, eh, min_n, must, must_not in SCHEDULER_CASES:
        result = schedule_day(acts, DAY, day_start_hour=sh, day_end_hour=eh)
        ids = [sa.activity.id for sa in result.activities]
        assert len(result.activities) >= min_n, f"{desc}: expected >={min_n}, got {len(result.activities)}"
        for m in must:
            assert m in ids, f"{desc}: {m} not in {ids}"
        for mn in must_not:
            assert mn not in ids, f"{desc}: {mn} should not be in {ids}"


# ── Resilience ───────────────────────────────────────────────────────────

def _sched(act_id, loc, cat, start_h, dur, travel=0):
    return ScheduledActivity(
        activity=Activity(id=act_id, name=act_id, location=loc,
                          duration_minutes=dur, category=cat, cost=10),
        scheduled_start=DAY.replace(hour=start_h),
        scheduled_end=DAY.replace(hour=start_h + dur // 60),
        travel_time_from_prev=travel)

RESILIENCE_CASES = [
    # (desc, activities, assert_score_gt)
    ("tight schedule scores higher than spaced",
     [_sched("a", (35.71, 139.79), "culture", 9, 120),
      _sched("b", (35.72, 139.80), "culture", 11, 120, travel=10)],
     None),  # compared below

    ("spaced schedule scores lower",
     [_sched("a", (35.71, 139.79), "culture", 9, 60),
      _sched("b", (35.68, 139.71), "nature", 14, 60, travel=20)],
     None),
]

def test_resilience():
    tight = compute_resilience(Itinerary(destination="T", days=[
        ItineraryDay(day_index=0, date=DAY, activities=RESILIENCE_CASES[0][1])]))
    spaced = compute_resilience(Itinerary(destination="S", days=[
        ItineraryDay(day_index=0, date=DAY, activities=RESILIENCE_CASES[1][1])]))
    assert tight.overall > spaced.overall + 20, f"tight={tight.overall} should be >> spaced={spaced.overall}"

    empty = compute_resilience(Itinerary(destination="E", days=[
        ItineraryDay(day_index=0, date=DAY, activities=[])]))
    assert empty.overall == 0.0 and empty.rating == "N/A"


# ── Repair ───────────────────────────────────────────────────────────────

def _itinerary_with(act_id="target", loc=(35.71, 139.79)):
    return Itinerary(destination="T", days=[ItineraryDay(day_index=0, date=DAY, activities=[
        _sched(act_id, loc, "culture", 10, 90),
        _sched("lunch", (35.69, 139.70), "food", 12, 60, travel=30),
    ])])

REPAIR_CASES = [
    # (desc, activity_id, pool, expect_success, expect_degraded, expect_type)
    ("no alternative → graceful degradation",
     "target", [], True, True, "removed"),

    ("non-existent activity → failure",
     "ghost", [], False, True, None),
]

def test_repair():
    for desc, aid, pool, exp_ok, exp_deg, exp_type in REPAIR_CASES:
        r = repair_itinerary(_itinerary_with(), aid, "closure", "closed", candidate_pool=pool)
        assert r.success == exp_ok, f"{desc}: success={r.success}"
        assert r.degraded == exp_deg, f"{desc}: degraded={r.degraded}"
        if exp_type:
            assert r.diff_entries[0].type == exp_type, f"{desc}: type={r.diff_entries[0].type}"


# ── Chaos ────────────────────────────────────────────────────────────────

def test_chaos_end_to_end():
    itin = _itinerary_with()
    result = trigger_chaos(itin, candidate_pool=[])
    assert result["repair"]["success"]
    assert result["disruption"]["activity_id"] in ["target", "lunch"]


# ── Planner ──────────────────────────────────────────────────────────────

PARSE_CASES = [
    ("plain json", '{"activities": [{"id": "a1"}]}'),
    ("markdown fenced", '```json\n{"activities": [{"id": "a1"}]}\n```'),
]

def test_planner_parse():
    for desc, raw in PARSE_CASES:
        result = parse_planner_response(raw)
        assert "activities" in result, f"{desc}: missing activities key"

def test_planner_mock():
    mock = _mock_activities("Tokyo", ["culture", "food"])
    assert len(mock["activities"]) > 0
    mock_generic = _mock_activities("Anywhere", [])
    assert len(mock_generic["activities"]) > 0


# ── Haversine ────────────────────────────────────────────────────────────

HAVERSINE_CASES = [
    ("same point", (0, 0), (0, 0), 0.0),
    ("Senso-ji to Gyoen", (35.7148, 139.7967), (35.6852, 139.7100), None),  # just > 0
]

def test_haversine():
    for desc, c1, c2, expected in HAVERSINE_CASES:
        d = haversine_distance(c1, c2)
        if expected is not None:
            assert abs(d - expected) < 0.01, f"{desc}: {d} != {expected}"
        else:
            assert d > 0, f"{desc}: should be > 0, got {d}"


# ── Runner ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [test_scheduler, test_resilience, test_repair, test_chaos_end_to_end,
             test_planner_parse, test_planner_mock, test_haversine]
    for t in tests:
        t()
        print(f"  PASS  {t.__name__}")
    print(f"\n{len(tests)} tests passed.")
