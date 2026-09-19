# Capability Map: TravelPilot

| Module id | Responsibility | Depends on |
|---|---|---|
| `planner` | LLM-based intent parsing → candidate activities | — |
| `scheduler` | Constraint-satisfaction algorithm (TSP + time windows) | `planner` |
| `resilience` | Fragility scoring of itineraries | `scheduler` |
| `repair` | Minimal-diff repair on disruptions | `scheduler`, `resilience` |
| `chaos` | Disruption injection engine | `scheduler`, `resilience` |
| `api` | FastAPI routes + data layer | `planner`, `scheduler`, `resilience`, `repair`, `chaos` |
| `ui` | React dashboard, timeline, diff view, chaos button | `api` |

Build order: `planner` → `scheduler` → `resilience` → `repair` → `chaos` → `api` → `ui`

**ASSUMPTIONS I'M MAKING:**
1. Backend: FastAPI + Python (you know this from SentinelX)
2. Scheduler: greedy nearest-neighbor + time-window pruning (not ILP solver)
3. LLM: Claude API for intent parsing and explanation generation — NOT for scheduling math
4. Places data: OpenTripMap free API for real venues, synthetic chaos for disruptions
5. Frontend: React/Next.js dashboard
6. DB: Supabase for itinerary storage
7. Deploy: Render
8. 36-hour timebox starting Sept 19 8AM
→ Correct me now or I'll proceed with these.

## Phase 1: Spec

Saving the full spec now.<tool_call>
<function=write_file>
<parameter=content># Spec: TravelPilot

## Objective
Build a multi-agent travel itinerary planner that combines LLM intent understanding with algorithmic optimization. Unlike single-prompt solutions, TravelPilot uses a visible pipeline: Planner Agent → Scheduler Engine → Resilience Scorer → Repair Agent. The key differentiator is the algorithmic scheduler (not LLM-guessed ordering) and minimal-diff repair (not full regeneration on disruption).

**User stories:**
1. As a traveler, I enter my destination, dates, budget, and interests → I get a time-optimized day-by-day itinerary with opening hours respected.
2. As a traveler, I see a resilience score showing how fragile my plan is (buffer time, single-point-of-failures, backup options).
3. As a traveler, I click "Chaos Mode" → something breaks → the system repairs with minimal changes highlighted as a diff.

## Tech Stack
- **Backend:** Python 3.11+, FastAPI, uvicorn
- **Scheduler:** Pure Python — greedy nearest-neighbor + time-window pruning
- **LLM:** Claude API (anthropic SDK) for intent parsing + explanation generation
- **Places API:** OpenTripMap (free tier) for real venue data
- **Frontend:** React 18+, Vite, Tailwind CSS
- **DB:** Supabase (PostgreSQL) for itinerary storage
- **Deploy:** Render (web service + static frontend)
- **Testing:** pytest, React Testing Library

## Commands
```
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
pytest tests/ -v

# Frontend
cd frontend
npm install
npm run dev
npm run build
npm test

# Deploy
git push origin main  # Render auto-deploys
```

## Project Structure
```
travelpilot/
├── backend/
│   ├── main.py              # FastAPI app entry
│   ├── planner/
│   │   ├── agent.py         # LLM intent parsing
│   │   └── prompts.py       # Prompt templates
│   ├── scheduler/
│   │   ├── engine.py        # Core scheduling algorithm
│   │   ├── models.py        # Activity, Itinerary, TimeWindow
│   │   └── optimizer.py     # Route optimization (TSP heuristic)
│   ├── resilience/
│   │   ├── scorer.py        # Fragility scoring
│   │   └── models.py        # ResilienceScore model
│   ├── repair/
│   │   ├── agent.py         # Minimal-diff repair logic
│   │   └── diff.py          # Itinerary diff computation
│   ├── chaos/
│   │   └── engine.py        # Disruption injection
│   ├── places/
│   │   └── client.py        # OpenTripMap API client
│   ├── models.py            # Shared Pydantic models
│   ├── routes.py            # API route definitions
│   ├── db.py                # Supabase client
│   ├── requirements.txt
│   └── tests/
│       ├── test_scheduler.py
│       ├── test_resilience.py
│       ├── test_repair.py
│       └── test_chaos.py
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── ItineraryTimeline.tsx
│   │   │   ├── ResilienceBadge.tsx
│   │   │   ├── DiffView.tsx
│   │   │   ├── ChaosButton.tsx
│   │   │   └── PlanningForm.tsx
│   │   ├── hooks/
│   │   └── lib/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Code Style
```python
# Backend: snake_case, type hints, Pydantic models
class Activity(BaseModel):
    id: str
    name: str
    location: tuple[float, float]  # lat, lng
    start_time: datetime
    end_time: datetime
    category: str
    cost: float
    priority: int = 1
```

```typescript
// Frontend: TypeScript strict, functional components, named exports
interface ItineraryDay {
  day: number;
  activities: Activity[];
  travelTime: number;
  resilienceScore: number;
}
```

## Testing Strategy
- **Unit tests (pytest):** Scheduler algorithm, resilience scorer, repair diff logic
- **Integration tests:** FastAPI routes with mock places data
- **Manual tests:** End-to-end flow through UI, Chaos Mode button
- **Coverage target:** 80%+ on scheduler, resilience, repair modules

## Boundaries
- **Always:** Run tests before commits, validate API inputs, handle API failures gracefully
- **Ask first:** Database schema changes, adding new dependencies, changing scheduler algorithm
- **Never:** Commit API keys, hardcode venue data, skip the scheduler for LLM-only ordering

## Success Criteria
1. Planner Agent returns structured activity list from user input
2. Scheduler produces time-ordered itinerary respecting opening hours and travel time
3. Resilience score is computed and displayed as a badge
4. Chaos Mode injects disruption → repair produces minimal diff → UI highlights changes
5. Full pipeline works end-to-end on Render
6. 3-minute demo video shows: generation → resilience score → chaos → repair

## Open Questions
1. Which LLM to use — Claude (your default) or GPT? Claude recommended since you know the API.
2. Supabase project — existing one from SentinelX or new?
3. Single-day or multi-day MVP? Recommend single-day first, multi-day as stretch goal.
