"""API routes for TravelPilot.

Wires the existing backend modules (Planner, Scheduler, Resilience,
Repair, Chaos) into FastAPI endpoints.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from planner.agent import plan_activities
from scheduler.models import (
    Activity as SchedActivity, TimeWindow, Itinerary as SchedItinerary,
)
from scheduler.engine import schedule_itinerary
from resilience.scorer import compute_resilience
from repair.agent import repair_itinerary
from chaos.engine import trigger_chaos
from openai import OpenAI
import os

router = APIRouter()

# In-memory state for demo (good enough for hackathon)
_current_itinerary: SchedItinerary | None = None
_current_candidates: list[SchedActivity] = []
_current_resilience = None


def _scheduled_to_api(sched_itin: SchedItinerary, resilience=None) -> dict:
    """Convert internal ScheduledItinerary to API response format."""
    days = []
    for day in sched_itin.days:
        activities = []
        for sa in day.activities:
            activities.append({
                "id": sa.activity.id,
                "name": sa.activity.name,
                "category": sa.activity.category,
                "cost": sa.activity.cost,
                "description": sa.activity.description,
                "location": {"lat": sa.activity.location[0], "lng": sa.activity.location[1]},
                "scheduled_start": sa.scheduled_start.isoformat(),
                "scheduled_end": sa.scheduled_end.isoformat(),
                "duration_minutes": sa.activity.duration_minutes,
                "travel_time_from_prev": sa.travel_time_from_prev,
                "priority": sa.activity.priority,
            })
        days.append({
            "day_index": day.day_index,
            "date": day.date.isoformat(),
            "activities": activities,
            "total_travel_minutes": day.total_travel_minutes,
            "total_activity_minutes": day.total_activity_minutes,
        })

    result = {
        "destination": sched_itin.destination,
        "days": days,
        "total_cost": sched_itin.total_cost,
        "total_travel_minutes": sched_itin.total_travel_minutes,
    }

    if resilience:
        result["resilience_score"] = {
            "overall": resilience.overall,
            "rating": resilience.rating,
            "summary": resilience.summary,
            "factors": [
                {"name": f.name, "score": f.score, "weight": f.weight, "description": f.description}
                for f in resilience.factors
            ],
        }

    return result


class PlanRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    interests: list[str]
    num_travelers: int = 1


class DisruptionRequest(BaseModel):
    activity_id: Optional[str] = None
    type: str = "closure"
    reason: str = "Venue closed"


@router.post("/api/plan")
async def plan_trip(request: PlanRequest):
    """Generate a complete itinerary from user preferences."""
    global _current_itinerary, _current_candidates, _current_resilience

    try:
        start_date = datetime.fromisoformat(request.start_date)
        end_date = datetime.fromisoformat(request.end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if end_date < start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date.")

    num_days = max(1, (end_date - start_date).days + 1)

    # Step 1: Get candidate activities from Planner Agent (LLM)
    llm_result = plan_activities(
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        budget=request.budget,
        interests=request.interests,
        num_travelers=request.num_travelers,
    )

    # Convert LLM output to scheduler format
    candidates = []
    for act in llm_result.get("activities", []):
        loc = act.get("location", {})
        if isinstance(loc, dict):
            loc_tuple = (loc.get("lat", 0.0), loc.get("lng", 0.0))
        else:
            loc_tuple = tuple(loc) if loc else (0.0, 0.0)

        tw = act.get("time_window", {})
        time_window = None
        if tw and tw.get("earliest") and tw.get("latest"):
            try:
                earliest = datetime.combine(start_date.date(), datetime.strptime(tw["earliest"], "%H:%M").time())
                latest = datetime.combine(start_date.date(), datetime.strptime(tw["latest"], "%H:%M").time())
                time_window = TimeWindow(earliest=earliest, latest=latest)
            except (ValueError, KeyError):
                pass

        candidates.append(SchedActivity(
            id=act.get("id", f"act_{len(candidates)}"),
            name=act.get("name", "Unknown"),
            location=loc_tuple,
            duration_minutes=act.get("duration_minutes", 60),
            category=act.get("category", "general"),
            cost=act.get("cost", 0),
            priority=act.get("priority", 3),
            description=act.get("description", ""),
            time_window=time_window,
        ))

    _current_candidates = candidates

    # Step 2: Schedule using algorithmic engine (NOT LLM)
    itinerary = schedule_itinerary(
        activities=candidates,
        destination=request.destination,
        start_date=start_date,
        num_days=num_days,
    )
    _current_itinerary = itinerary

    # Step 3: Compute resilience score (proactive, BEFORE any disruption)
    _current_resilience = compute_resilience(itinerary)

    return _scheduled_to_api(itinerary, _current_resilience)


@router.get("/api/score")
async def get_resilience_score():
    """Get the current itinerary's resilience score."""
    if not _current_itinerary:
        raise HTTPException(status_code=404, detail="No itinerary. Call /api/plan first.")

    score = compute_resilience(_current_itinerary)
    return {
        "overall": score.overall,
        "rating": score.rating,
        "summary": score.summary,
        "factors": [
            {"name": f.name, "score": f.score, "weight": f.weight, "description": f.description}
            for f in score.factors
        ],
    }


@router.post("/api/chaos")
async def trigger_chaos_mode(target_activity_id: str = None):
    """Trigger Chaos Mode: inject disruption, repair, return diff."""
    global _current_itinerary, _current_candidates

    if not _current_itinerary:
        raise HTTPException(status_code=404, detail="No itinerary. Call /api/plan first.")

    try:
        result = trigger_chaos(
            itinerary=_current_itinerary,
            candidate_pool=_current_candidates,
            target_activity_id=target_activity_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/repair")
async def repair_endpoint(disruption: DisruptionRequest):
    """Manually repair a specific disruption."""
    global _current_itinerary, _current_candidates

    if not _current_itinerary:
        raise HTTPException(status_code=404, detail="No itinerary. Call /api/plan first.")

    result = repair_itinerary(
        itinerary=_current_itinerary,
        disruption_activity_id=disruption.activity_id or _current_itinerary.days[0].activities[0].activity.id,
        disruption_type=disruption.type,
        disruption_reason=disruption.reason,
        candidate_pool=_current_candidates,
    )

    return {
        "success": result.success,
        "degraded": result.degraded,
        "degradation_reason": result.degradation_reason,
        "diff_entries": [d.model_dump() for d in result.diff_entries],
        "explanation": result.explanation,
        "activities_changed": result.activities_changed,
        "cost_delta": result.cost_delta,
    }


@router.post("/api/chat")
async def chat_endpoint(message: str):
    """Natural-language Q&A about the current itinerary."""
    if not _current_itinerary:
        raise HTTPException(status_code=404, detail="No itinerary. Call /api/plan first.")

    # Build context from current itinerary
    context_parts = []
    for day in _current_itinerary.days:
        context_parts.append(f"Day {day.day_index + 1} ({day.date.strftime('%Y-%m-%d')}):")
        for sa in day.activities:
            context_parts.append(
                f"  - {sa.activity.name} ({sa.activity.category}) "
                f"{sa.scheduled_start.strftime('%H:%M')}-{sa.scheduled_end.strftime('%H:%M')} "
                f"${sa.activity.cost:.0f} at ({sa.activity.location[0]:.4f}, {sa.activity.location[1]:.4f})"
            )
        context_parts.append(f"  Total travel: {day.total_travel_minutes:.0f}min")

    itinerary_context = "\n".join(context_parts)

    system_prompt = f"""You are a travel assistant with access to this itinerary:

{itinerary_context}

Answer questions about the trip concisely. Base your answer ONLY on the itinerary data.
Be specific with times, locations, and costs. Keep answers to 2-3 sentences max."""

    try:
        client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai"),
        )
        response = client.chat.completions.create(
            model=os.getenv("GEMINI_MODEL", "gemini-3.6-flash"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        # Fallback: simple keyword-based responses
        msg_lower = message.lower()
        if "tomorrow" in msg_lower or "morning" in msg_lower:
            return {"response": "Check the day-by-day timeline above for tomorrow's scheduled activities. The itinerary is optimized for minimal travel between stops."}
        elif "cancel" in msg_lower or "disrupt" in msg_lower:
            return {"response": "If a booking is cancelled, hit the Chaos Mode button to see the Repair Agent find the minimal fix. It replaces only what's broken, not the whole itinerary."}
        elif "budget" in msg_lower or "cost" in msg_lower:
            total = sum(sa.activity.cost for day in _current_itinerary.days for sa in day.activities)
            return {"response": f"Total estimated cost: ${total:.0f}. The itinerary stays within your budget constraints."}
        else:
            return {"response": f"I can help with questions about your {_current_itinerary.destination} itinerary. Try asking about specific times, costs, or what happens if something changes."}
