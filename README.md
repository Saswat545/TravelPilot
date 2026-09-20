# TravelPilot

**Intelligent Trip Planning and Disruption Management Agent**

Most travel tools handle individual bookings well, but fail when something changes mid-trip. TravelPilot continuously reasons across the entire itinerary — planning, scoring resilience, stress-testing with chaos mode, and repairing with minimal diffs.

## Demo

1. Enter a destination, dates, budget, and interests
2. Get a scheduled itinerary with a resilience score (0-100)
3. Hit **Chaos Mode** — watch an activity get cancelled and the system repair itself
4. See exactly what changed via the diff panel
5. Ask natural-language questions about your trip

## Architecture

```
User → React/Vite Frontend → FastAPI Backend
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
              Planner Agent   Scheduler Engine   Resilience Scorer
              (Gemini LLM)    (Greedy NN +       (4-factor fragility)
                               Haversine)
                    │               │               │
                    └───────┬───────┘               │
                            │                       │
                      Repair Agent ←──── Chaos Engine
                      (Minimal-diff)    (Disruption injection)
```

| Layer | Technology |
|-------|------------|
| Backend | Python / FastAPI |
| Frontend | React / Vite |
| LLM | Gemini 3.6 Flash (intent parsing, explanations — never scheduling) |
| Scheduling | Greedy nearest-neighbor with Haversine distances + time-window pruning |
| Visualization | Chart.js (resilience gauge, budget breakdown, activity mix, time allocation) |
| Icons | Lucide (via better-icons CLI) |

## Key Features

### Algorithmic Scheduling

The scheduler is a real algorithm, not an LLM guess. It uses:
- **Haversine distance** for accurate lat/lng calculations
- **Greedy nearest-neighbor** to minimize travel between consecutive stops
- **Time-window pruning** to respect opening hours
- **Multi-day distribution** to spread activities across the trip

### Proactive Resilience Scoring

Before anything breaks, the system scores your itinerary's fragility on a 0-100 scale across four factors:

| Factor | Weight | What it measures |
|--------|--------|-----------------|
| Buffer Time | 25% | Transitions with <15min gap |
| Single-Point Failures | 30% | Activities with no nearby alternative |
| Time Density | 20% | How packed the schedule is (delays cascade) |
| Category Diversity | 15% | Over-reliance on one activity type |

### Chaos Mode Stress-Testing

A button that injects a real disruption (closure, weather, overbooking, cancellation) and runs the repair pipeline live. No pre-baked outcomes.

### Minimal-Diff Repair

When something breaks, the system finds the smallest valid fix:
- Swaps in an alternative from the candidate pool (prefers same category, closest location)
- Shifts subsequent activities to fill gaps
- Outputs a structured diff (removed/modified/shifted) — like git for your trip

## Project Structure

```
TravelPilot/
├── backend/
│   ├── main.py                 # FastAPI entry, CORS, static serving
│   ├── routes.py               # API endpoints: /plan, /chaos, /repair, /chat, /score
│   ├── planner/
│   │   ├── agent.py            # LLM intent parsing + mock fallback
│   │   └── prompts.py          # System/user prompt templates
│   ├── scheduler/
│   │   ├── engine.py           # Greedy nearest-neighbor + time-window pruning
│   │   └── models.py           # Activity, TimeWindow, Itinerary models
│   ├── resilience/
│   │   ├── scorer.py           # 4-factor fragility scoring
│   │   └── models.py           # FragilityFactor, ResilienceScore models
│   ├── repair/
│   │   ├── agent.py            # Minimal-diff repair + find_alternative
│   │   └── models.py           # DiffEntry, RepairResult models
│   ├── chaos/
│   │   └── engine.py           # Deterministic disruption injection
│   └── tests/
│       └── test_contract.py    # 7 behavioral tests
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main orchestrator (state owner)
│   │   ├── Pipeline.jsx        # Pipeline flow visualization
│   │   ├── PlanningForm.jsx    # Input form
│   │   ├── Timeline.jsx        # Day-by-day activity view
│   │   ├── Sidebar.jsx         # Resilience card, charts, budget, chat
│   │   ├── DiffPanel.jsx       # Chaos repair diff view
│   │   ├── icons.jsx           # Lucide SVG icons (data-driven)
│   │   └── charts.js           # Shared Chart.js config
│   └── vite.config.js          # Proxy to backend
├── docs/
│   ├── architecture-overview.mmd
│   ├── data-flow.mmd
│   ├── stress-test-results.md
│   └── brand-guidelines.md
├── SUBMISSION.md
├── EVALUATOR_SCORE.md
├── VIDEO_SCRIPT.md
├── LINKEDIN_POST.md
└── render.yaml                 # Render deployment config
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Gemini API key (free tier works)

### Setup

```bash
# Clone
git clone https://github.com/Saswat545/TravelPilot.git
cd TravelPilot

# Backend
cd backend
pip install -r requirements.txt
cd ..

# Frontend
cd frontend
npm install
cd ..

# Environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Run Locally

```bash
# Terminal 1: Backend (port 8001)
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8001

# Terminal 2: Frontend (port 3001, proxies to 8001)
cd frontend
npm run dev
```

Open http://localhost:3001

### Run Tests

```bash
cd backend
python -m tests.test_contract
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/plan` | Generate itinerary from preferences |
| POST | `/api/chaos` | Trigger disruption + repair |
| POST | `/api/repair` | Manually repair a specific disruption |
| POST | `/api/chat` | Natural-language Q&A about the itinerary |
| GET | `/api/score` | Get current resilience score |
| GET | `/health` | Health check |

## Deploy to Render

1. Push to GitHub (already done)
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your GitHub repo
4. Set `GEMINI_API_KEY` in the environment variables
5. Deploy

The `render.yaml` config handles build and start commands automatically.

## Test Results

| Suite | Cases | Status |
|-------|-------|--------|
| Scheduler | Time windows, empty input, single activity, far-activity exclusion | All pass |
| Resilience | Tight vs. spaced itinerary, empty itinerary | All pass |
| Repair | No alternative found, non-existent activity | All pass |
| Chaos | End-to-end inject + repair | Pass |
| Planner | Plain JSON + markdown fenced parsing | Pass |
| Mock | City-specific + generic fallback | Pass |
| Haversine | Same point = 0, distance > 0 | Pass |

**Stress tests:** Japan (5 days), Paris (6 days), USA (31 days), empty destination, single day — all produce valid output, no crashes.

## Tech Decisions

**Why algorithmic scheduling instead of LLM?** LLMs are bad at spatial/temporal constraint reasoning. The scheduler uses greedy nearest-neighbor with Haversine distances — deterministic, fast, and correct. The LLM handles intent parsing and explanation generation where it excels.

**Why minimal-diff repair instead of full regeneration?** Regenerating the entire itinerary on every change loses context and makes it impossible to see what changed. The repair agent finds the smallest valid fix and outputs a structured diff.

**Why a resilience score before anything breaks?** Proactive risk assessment is more valuable than reactive repair. Knowing your plan is fragile before you leave is better than discovering it mid-trip.

## License

MIT
