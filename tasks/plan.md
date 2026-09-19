# TravelPilot — Implementation Plan

## Phase 1: Project Skeleton (Hours 0–2)
- [ ] Task 1: Initialize repo, FastAPI skeleton, React app
  - Acceptance: `uvicorn main:app --reload` serves `/health`, React dev server runs
  - Verify: `curl localhost:8000/health` returns `{"status":"ok"}`
  - Files: `backend/main.py`, `backend/requirements.txt`, `frontend/package.json`, `frontend/vite.config.ts`

- [ ] Task 2: Supabase setup + DB schema
  - Acceptance: `itineraries` table exists with correct columns
  - Verify: Supabase dashboard shows table, API returns empty list
  - Files: `backend/db.py`, `supabase/migrations/`

## Phase 2: Planner Agent (Hours 2–6)
- [ ] Task 3: OpenTripMap client — fetch venues by category + location
  - Acceptance: Returns list of venues with name, coords, hours, cost
  - Verify: Unit test with mock HTTP, manual test for "Tokyo" returns venues
  - Files: `backend/places/client.py`, `backend/tests/test_places.py`

- [ ] Task 4: Planner Agent — LLM intent parsing
  - Acceptance: Given user input (destination, dates, budget, interests), returns structured Activity list
  - Verify: Unit test with canned LLM response, manual test with real Claude API call
  - Files: `backend/planner/agent.py`, `backend/planner/prompts.py`, `backend/tests/test_planner.py`

## Phase 3: Scheduler Engine (Hours 6–12) — CORE DIFFERENTIATOR
- [ ] Task 5: Data models — Activity, TimeWindow, Itinerary
  - Acceptance: Pydantic models validate correctly, serialize to JSON
  - Verify: pytest passes
  - Files: `backend/scheduler/models.py`

- [ ] Task 6: Greedy scheduler — nearest-neighbor + time-window pruning
  - Acceptance: Given activities with time windows, produces ordered itinerary minimizing travel time
  - Verify: Test with 10 activities across 2 days, verify time windows respected, travel time < brute-force baseline
  - Files: `backend/scheduler/engine.py`, `backend/tests/test_scheduler.py`

- [ ] Task 7: Route optimizer — TSP heuristic within each day
  - Acceptance: Activities ordered to minimize total walking/driving distance per day
  - Verify: Test with known coordinates, verify improvement over random ordering
  - Files: `backend/scheduler/optimizer.py`

## Phase 4: Resilience Scorer (Hours 12–16)
- [ ] Task 8: Resilience scoring algorithm
  - Acceptance: Returns score 0-100 based on: buffer time, single-point-of-failures, backup options, time density
  - Verify: Test that an itinerary with no buffers scores lower than one with buffers
  - Files: `backend/resilience/scorer.py`, `backend/resilience/models.py`, `backend/tests/test_resilience.py`

## Phase 5: Repair Agent (Hours 16–22)
- [ ] Task 9: Itinerary diff computation
  - Acceptance: Given two itineraries, returns list of additions/removals/modifications
  - Verify: Test with known changes, verify minimal diff (not full regeneration)
  - Files: `backend/repair/diff.py`, `backend/tests/test_diff.py`

- [ ] Task 10: Minimal-diff repair agent
  - Acceptance: Given disruption + itinerary, produces repaired itinerary with minimal changes
  - Verify: Inject closure → repair replaces only that activity, keeps rest intact
  - Files: `backend/repair/agent.py`, `backend/tests/test_repair.py`

## Phase 6: Chaos Engine (Hours 22–24)
- [ ] Task 11: Disruption injection
  - Acceptance: Given itinerary, randomly cancels/closes one activity, returns disruption event
  - Verify: Test that injection modifies exactly one activity
  - Files: `backend/chaos/engine.py`, `backend/tests/test_chaos.py`

## Phase 7: API Layer (Hours 24–28)
- [ ] Task 12: FastAPI routes — /plan, /repair, /score, /chaos
  - Acceptance: All endpoints accept requests, return correct JSON, handle errors
  - Verify: pytest on all routes, manual curl tests
  - Files: `backend/routes.py`, `backend/main.py`

- [ ] Task 13: Supabase integration — store/retrieve itineraries
  - Acceptance: Plan creates itinerary in DB, can retrieve by ID
  - Verify: Create → retrieve → compare JSON matches
  - Files: `backend/db.py`

## Phase 8: Frontend (Hours 28–32)
- [ ] Task 14: Planning form — destination, dates, budget, interests
  - Acceptance: Form submits to /plan, shows loading state
  - Verify: Manual test — fill form, submit, see itinerary
  - Files: `frontend/src/components/PlanningForm.tsx`

- [ ] Task 15: Itinerary timeline view
  - Acceptance: Activities displayed as vertical timeline with times, locations, costs
  - Verify: Visual check — timeline renders correctly for sample data
  - Files: `frontend/src/components/ItineraryTimeline.tsx`

- [ ] Task 16: Resilience badge
  - Acceptance: Badge shows score 0-100 with color coding (green/yellow/red)
  - Verify: Visual check — badge updates when itinerary changes
  - Files: `frontend/src/components/ResilienceBadge.tsx`

- [ ] Task 17: Diff view + Chaos Mode button
  - Acceptance: Chaos button triggers /chaos → /repair → shows diff-highlighted updated timeline
  - Verify: Click chaos → see activity change → changes highlighted in green/red
  - Files: `frontend/src/components/DiffView.tsx`, `frontend/src/components/ChaosButton.tsx`

## Phase 9: Deploy + Polish (Hours 32–36)
- [ ] Task 18: Deploy backend to Render
  - Acceptance: Live URL serves /health, /plan works end-to-end
  - Verify: curl live URL, test full flow
  - Files: `render.yaml` or Render dashboard config

- [ ] Task 19: Deploy frontend to Render/Vercel
  - Acceptance: Live URL loads, connects to backend API
  - Verify: Full flow in fresh browser
  - Files: `frontend/vite.config.ts` (proxy or production URL)

- [ ] Task 20: Record 3-minute demo video
  - Acceptance: Video shows: generation → resilience score → chaos → repair
  - Verify: Watch full video, check timing
  - Files: Video file

- [ ] Task 21: LinkedIn Day-1 post
  - Acceptance: Post published with project description + link
  - Verify: Post visible on profile
  - Files: LinkedIn post content

## Never Cut (if behind schedule)
1. Scheduler Engine (Task 6-7) — the core differentiator
2. Repair Agent (Task 9-10) — the second differentiator
3. Chaos Mode (Task 11 + 17) — the demo moment

## Cut Order (if behind schedule)
1. Multi-day → single-day only
2. Real places API → curated mock dataset
3. Polished UI → functional but ugly
4. Reasoning trace panel → cut last (cheap to add)
