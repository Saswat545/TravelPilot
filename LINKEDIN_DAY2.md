# TravelPilot — LinkedIn Day 2 Post

**~1,200 characters**

---

We just shipped TravelPilot — an AI trip planner that doesn't just plan your trip, it breaks it and repairs it on purpose.

Most AI travel apps are one big LLM call: user says "plan my trip to Tokyo" and the model guesses everything from activities to ordering. We built something different — a pipeline of specialists:

1. A Planner Agent that parses intent into structured activities
2. An algorithmic Scheduler that orders them using real distance calculations, not LLM guesses
3. A Resilience Scorer that rates trip fragility before anything goes wrong
4. A Repair Agent that does minimal-diff surgery when something breaks

The moment that sells it: hit "Chaos Mode" and watch the system cancel an activity, then repair the itinerary with a surgical diff showing exactly what changed. No full regeneration. No mystery. Just a clean fix with visual proof.

What I learned building this in 36 hours: the hardest part isn't getting an LLM to plan a trip. It's building the system around the LLM that makes it actually reliable — retry logic for malformed JSON, fallback data for when the API fails, and graceful degradation when no alternative exists.

The resilience score was the surprise hit. Showing users a proactive fragility metric before anything breaks reframes the entire product from "plans trips" to "understands risk in plans."

Live demo: [URL]
GitHub: [URL]

#BuildWithAI #AgentHackathon #TravelTech #AIAgent
