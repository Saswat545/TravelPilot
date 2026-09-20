# TravelPilot — Additional Materials

**Agent Hackathon Submission**

---

## 1. Why TravelPilot is Different

Every other team will build: "User gives preferences → LLM plans trip → Done."

We built: **A system that plans your trip, stress-tests it, breaks it on purpose, and repairs it with a surgical diff you can see.**

| What everyone else does | What TravelPilot does |
|------------------------|----------------------|
| One LLM call plans everything | Multi-stage pipeline: LLM for understanding + real algorithm for optimization |
| Full regeneration on change | Minimal-diff repair — only what broke gets fixed |
| "Here's your itinerary" | "Here's your itinerary + its fragility score + why it matters" |
| Demo: show a static plan | Demo: hit Chaos Mode, watch something break, watch it heal |

---

## 2. Architecture: Why It Matters

The key insight: **LLMs are bad at spatial/temporal constraint reasoning.** They hallucinate distances, ignore opening hours, and can't order 8 activities to minimize travel.

Our solution: separate concerns.

```
┌─────────────────────────────────────────────────────────────────┐
│                        TravelPilot Pipeline                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Planner Agent │───▶│   Scheduler  │───▶│  Resilience  │       │
│  │  (Gemini)     │    │   Engine     │    │   Scorer     │       │
│  │              │    │              │    │              │       │
│  │ "What does   │    │ "How should  │    │ "How fragile │       │
│  │  the user    │    │  we order    │    │  is this     │       │
│  │  want?"      │    │  this?"      │    │  plan?"      │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  Structured JSON    Ordered Itinerary    Fragility Score        │
│  (activities)       (with times)         (0-100)                │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │ Chaos Engine │───▶│ Repair Agent │                           │
│  │              │    │              │                           │
│  │ "Break       │    │ "Fix it with │                           │
│  │  something"  │    │  minimal     │                           │
│  │              │    │  changes"    │                           │
│  └──────────────┘    └──────────────┘                           │
│                              │                                   │
│                              ▼                                   │
│                       Structured Diff                            │
│                       (removed/modified/shifted)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**The LLM does:** Intent parsing, explanation generation, natural-language Q&A.

**The code does:** Scheduling, optimization, resilience scoring, repair logic.

This distinction matters because it's the difference between "AI that guesses" and "AI that works."

---

## 3. The Scheduler: Real Algorithm, Not LLM Magic

```python
# This is the actual scheduling algorithm (simplified)
def schedule_day(activities, day_date):
    current_time = day_date.replace(hour=9)  # Start at 9 AM
    current_location = (0.0, 0.0)
    scheduled = []
    
    while activities and current_time < day_end:
        best = None
        best_distance = float('inf')
        
        for act in activities:
            # 1. Calculate travel time from current position
            travel = haversine_distance(current_location, act.location)
            
            # 2. Check if activity fits in its time window
            arrival = current_time + travel_minutes(travel)
            if not fits_in_window(arrival, act.time_window):
                continue
            
            # 3. Pick the nearest feasible activity
            if travel < best_distance:
                best = act
                best_distance = travel
        
        if best is None:
            break  # No more activities fit
        
        # 4. Schedule it, advance time
        scheduled.append(ScheduledActivity(
            activity=best,
            scheduled_start=arrival,
            scheduled_end=arrival + best.duration,
            travel_time=travel
        ))
        current_time = arrival + best.duration
        current_location = best.location
    
    return scheduled
```

**Why this matters:** The LLM might order activities randomly or by popularity. Our algorithm minimizes actual travel distance using real coordinates. A judge can verify this by checking the travel times between activities.

---

## 4. Resilience Scoring: Proactive, Not Reactive

Most systems score risk AFTER something breaks. We score it BEFORE.

**The four factors:**

| Factor | What it measures | Why it matters |
|--------|-----------------|----------------|
| **Buffer Time** | Transitions with <15min gap | One delay cascades through the day |
| **Single-Point Failures** | Activities with no nearby alternative | If it cancels, you lose that category entirely |
| **Time Density** | How packed the schedule is | A 95% full day has zero slack for delays |
| **Category Diversity** | Over-reliance on one type | If it rains, all outdoor activities die |

**Example output:**
```json
{
  "overall": 46.0,
  "rating": "Good",
  "factors": [
    {"name": "Buffer Time", "score": 71.0, "weight": 0.25},
    {"name": "Single-Point Failures", "score": 50.0, "weight": 0.30},
    {"name": "Time Density", "score": 0.0, "weight": 0.20},
    {"name": "Category Diversity", "score": 58.0, "weight": 0.15}
  ]
}
```

**Why this matters:** A judge testing your app can see the resilience score BEFORE hitting Chaos Mode. This proves the system is genuinely proactive, not just reactive.

---

## 5. Chaos Mode + Minimal-Diff Repair

This is the demo moment that makes judges remember you.

**What happens:**
1. User clicks "CHAOS MODE"
2. System picks a random activity (or user-targeted)
3. Disruption is injected (closure/weather/overbooked/cancelled)
4. Repair Agent finds the smallest valid fix
5. UI highlights exactly what changed

**The diff output:**
```json
{
  "diff_entries": [
    {
      "type": "modified",
      "activity_name": "Chandni Chowk Market",
      "old_value": "Chandni Chowk Market",
      "new_value": "Humayun's Tomb",
      "reason": "Replaced with Humayun's Tomb — 14min travel, same category"
    },
    {
      "type": "shifted",
      "activity_name": "Humayun's Tomb",
      "old_value": "15:50-17:50",
      "new_value": "15:50-17:20",
      "reason": "Duration changed from 120.0min to 90.0min"
    },
    {
      "type": "modified",
      "activity_name": "Humayun's Tomb",
      "old_value": "$15",
      "new_value": "$7",
      "reason": "Cost decreased by $8"
    }
  ]
}
```

**Why this matters:** The diff is structured JSON, not free text. The frontend renders it visually with color coding. A judge can see exactly what changed and why — no mystery, no "here's a new list."

---

## 6. Test Results

### Contract Tests (7/7 Passing)

| Test | What it verifies | Status |
|------|-----------------|--------|
| test_scheduler | Time windows respected, empty input, single activity, far-activity excluded | PASS |
| test_resilience | Tight > spaced by 20+, empty = 0.0/N/A | PASS |
| test_repair | No alternative → graceful degradation, non-existent → failure | PASS |
| test_chaos_end_to_end | End-to-end inject + repair succeeds | PASS |
| test_planner_parse | Plain JSON + markdown fenced both parse | PASS |
| test_planner_mock | Tokyo mock + generic fallback both return activities | PASS |
| test_haversine | Same point = 0, Senso-ji to Gyoen > 0 | PASS |

### Stress Tests (5/5 Passing)

| Scenario | Input | Result |
|----------|-------|--------|
| Japan, 5 days, $500 | 2 travelers, food + culture | 8 activities, 5 days, $108 |
| Paris, 6 days, $2000 | 2 travelers, art + history | 8 real LLM venues (Louvre, Eiffel Tower) |
| USA, 31 days, $100 | 1 traveler, nature + adventure | 8 activities across 4 days, no crash |
| Empty destination | "" | Graceful fallback, no crash |
| Tokyo, single day | 1 day, $100 | 6 activities packed in one day |

---

## 7. Code Quality

### Backend (1,825 lines)

| Module | Lines | Responsibility |
|--------|-------|---------------|
| routes.py | 283 | API endpoints, request/response handling |
| planner/agent.py | 241 | LLM integration, mock fallback |
| resilience/scorer.py | 241 | 4-factor fragility scoring |
| repair/agent.py | 288 | Minimal-diff repair logic |
| scheduler/engine.py | 232 | Greedy nearest-neighbor algorithm |
| planner/prompts.py | 75 | System/user prompt templates |

### Frontend (1,528 lines)

| Component | Lines | Responsibility |
|-----------|-------|---------------|
| App.jsx | 146 | State orchestration |
| Sidebar.jsx | 200 | Resilience card, 4 charts, budget, chat |
| PlanningForm.jsx | 86 | Input form |
| Timeline.jsx | 62 | Day-by-day activity view |
| DiffPanel.jsx | 49 | Chaos repair diff view |
| icons.jsx | 73 | Data-driven Lucide SVG icons |

### Design Decisions

1. **Single state owner:** `App.jsx` owns all itinerary state. Components receive props, emit callbacks. No context, no stores — simplest structure.

2. **Algorithmic scheduling:** The scheduler is pure code, not an LLM call. This is the core differentiator.

3. **Structured diff output:** Repair returns JSON with `type`, `old_value`, `new_value`, `reason`. Frontend renders it directly — no parsing, no guessing.

4. **Graceful degradation:** If LLM fails, mock data kicks in. If repair has no alternative, it degrades gracefully. The demo never crashes.

---

## 8. What We'd Build Next

With more time:

1. **Real Places API** — OpenTripMap or Google Places for actual venue data
2. **Constraint Modification** — Let users change budget/dates and regenerate
3. **Conflict Detection** — Detect overlapping activities automatically
4. **Multi-user Auth** — Supabase integration for saved trips
5. **Real-time Disruption Feeds** — Connect to weather APIs, flight status APIs

---

## 9. Links

| Resource | URL |
|----------|-----|
| GitHub | https://github.com/Saswat545/TravelPilot |
| Live Demo | https://your-app-url.render.com (deploying) |
| Video Script | VIDEO_SCRIPT.md |
| LinkedIn Post | LINKEDIN_POST.md |

---

## 10. How to Verify This Works

**Fastest way (2 minutes):**

1. Open the live URL
2. Enter "Tokyo", dates Jan 1-3, budget $200, interests: culture + food
3. Click "Plan My Trip"
4. Wait for timeline to load (watch the pipeline visualization)
5. Note the resilience score (should be 40-60 range)
6. Click "CHAOS MODE"
7. Watch the diff panel appear with change highlights
8. Ask a question in the chat: "What is the total cost?"

**What to look for:**
- Activities are real venues (Senso-ji, Tsukiji, Shibuya, etc.)
- Travel times between activities are reasonable (5-20 min)
- Resilience score has 4 factors with explanations
- Chaos Mode changes exactly 1-2 items, not the whole itinerary
- Diff panel shows old → new values with reasons
