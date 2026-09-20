# TravelPilot

## Intelligent Trip Planning and Disruption Management Agent

---

### The Problem

Most travel tools handle individual bookings well, but fail when something changes mid-trip. They don't continuously reason across the entire itinerary — a cancelled activity means starting from scratch, and you have no idea what actually changed.

### What We Built

An AI agent that plans, scores resilience, stress-tests with chaos mode, and repairs with minimal diffs. Not a trip planner that regenerates everything when something breaks — a system that understands the structure of a plan and surgically fixes only what changed.

### Architecture

| Layer | Technology |
|-------|------------|
| Backend | Python / FastAPI |
| Frontend | React / Vite |
| LLM | Gemini 3.6 Flash (intent parsing, explanation generation — never scheduling) |
| Scheduling | Greedy nearest-neighbor with Haversine distances and time-window pruning |
| Visualization | Chart.js (resilience gauge, budget breakdown, activity mix, time allocation) |
| Icons | Lucide (sourced via better-icons CLI) |
| Design System | Trust & Authority — black/gold/white, Fira Sans + Fira Code |

### Demo Flow

1. Enter destination, dates, budget, and interests
2. Planner Agent generates structured candidate activities via Gemini
3. Scheduler Engine orders them algorithmically — minimizing travel time, respecting opening hours
4. Resilience Score computed on a 0-100 scale **before** anything breaks
5. Click **Chaos Mode** — a disruption is injected, repair runs, and only the affected items change
6. Diff view highlights exactly what changed (removed, added, modified, shifted)
7. Ask natural-language questions via chat ("What is the total cost?", "Which activities are close to my hotel?")

### Key Features

**1. Algorithmic Scheduling** — Not LLM-guessed. Greedy nearest-neighbor construction with Haversine distance calculation and time-window pruning. The scheduler is pure code, not a prompt.

**2. Proactive Resilience Scoring** — A 0-100 fragility score computed before any disruption. Four factors: buffer time, single-point failures, time density, category diversity. The breakdown explains why, not just what.

**3. Chaos Mode Stress-Testing** — A button that injects a real disruption. No fake demos, no pre-baked outcomes. The system reacts live.

**4. Minimal-Diff Repair** — When something breaks, the system doesn't regenerate the entire itinerary. It finds the smallest valid fix — rescheduling around the gap, swapping in an alternative from the candidate pool, or shifting timing. The UI highlights exactly what changed.

### Test Results

| Test Suite | Result |
|-----------|--------|
| Contract tests (7 cases) | 7/7 passing |
| Scheduler (time windows, empty, single, far-activity) | All pass |
| Resilience (tight vs. spaced, empty itinerary) | All pass |
| Repair (no alternative, non-existent activity) | All pass |
| Chaos end-to-end (inject + repair) | Pass |
| Planner parse (plain JSON + markdown fenced) | Pass |
| Planner mock (city-specific + generic fallback) | Pass |

| Stress Test Scenario | Result |
|---------------------|--------|
| Japan, 5 days, $500 | 8 activities, 5 days, $108 |
| Paris, 6 days, $2000 | 8 real LLM venues (Louvre, Eiffel Tower, etc.) |
| USA, 31 days, $100 | 8 activities across 4 days, no crash |
| Empty destination | Graceful fallback, no crash |
| Tokyo, single day | 6 activities packed in one day |

### Documentation

- **Additional Materials:** `ADDITIONAL_MATERIALS.md` — differentiation story, architecture deep-dive, algorithm explanation, test results, verification guide
- Architecture diagrams: `docs/architecture-overview.mmd`, `docs/data-flow.mmd`
- Video script: `VIDEO_SCRIPT.md`
- Brand guidelines: `docs/brand-guidelines.md`
- Stress test report: `docs/stress-test-results.md`
- Evaluator self-assessment: `EVALUATOR_SCORE.md`

### GitHub

https://github.com/Saswat545/TravelPilot
