# TravelPilot — Demo Video Script

**Total runtime: ~2 minutes**

---

## Opening Hook (0:00 - 0:10)

**[Screen: Black with white text fading in]**

> "What if your travel agent could stress-test your trip before you book?"

**[Text fades out, app loads]**

---

## Problem Statement (0:10 - 0:25)

**[Screen: Split view — left shows a phone with a cancelled flight notification, right shows a static itinerary]**

> "Travel plans break. Flights cancel. Venues close. And when something changes, most travel apps just regenerate your entire itinerary from scratch — you lose all context, and you have no idea what actually changed."

**[Text overlay: "Most tools plan trips. None of them manage them."]**

---

## Demo Walkthrough (0:25 - 1:25)

### Step 1: Plan a Trip (0:25 - 0:40)

**[Screen: TravelPilot app, form visible]**

> "Watch. I'll plan a trip to India — 3 days, culture and food interests."

**[Action: Type 'India', set dates to Jan 1-3, click 'Plan My Trip']**

**[Screen: Loading animation showing pipeline stages: Planner Agent, Scheduler Engine, Resilience Score, Repair Agent]**

> "Behind the scenes, four specialized stages are working: the Planner Agent parses my intent, the Scheduler Engine orders everything using real algorithms — not LLM guesses — and the Resilience Scorer evaluates how fragile this plan is before anything even goes wrong."

**[Screen: Timeline loads with 8 activities across 3 days, resilience badge shows 46/100]**

> "Eight real venues, scheduled across 3 days, with actual travel times between stops. And right there — a resilience score of 46. The system is already telling me this plan has risks."

### Step 2: Resilience Score (0:40 - 0:50)

**[Screen: Sidebar showing resilience breakdown — Buffer Time: 71, Single-Point Failures: 50, Category Diversity: 58]**

> "The resilience score breaks down into four factors: buffer time between activities, whether any single point of failure exists, time density, and category diversity. This isn't reactive — it scores your plan before anything breaks."

### Step 3: Chaos Mode (0:50 - 1:10)

**[Screen: Cursor hovers over 'CHAOS MODE' button]**

> "Now here's the part that matters. Watch what happens when something goes wrong."

**[Action: Click 'CHAOS MODE']**

**[Screen: Timeline updates, Chandni Chowk Market shows as removed, diff panel appears with 'CHANGES APPLIED']**

> "Chaos Mode just cancelled Chandni Chowk Market. The Repair Agent found the smallest possible fix — not a full regeneration, a surgical repair. Look at the diff: one activity replaced, timing shifted, cost updated. It changed exactly what needed to change and nothing else."

**[Screen: Diff panel shows: MODIFIED Chandni Chowk Market -> Humayun's Tomb, SHIFTED timing, MODIFIED cost $15 -> $7]**

> "This is what makes it different. Other tools would show you a brand-new itinerary and you'd have no idea what changed. TravelPilot shows you exactly what broke and exactly what fixed it — like a git diff for your trip."

### Step 4: Chat Q&A (1:10 - 1:25)

**[Screen: Chat panel]**

**[Action: Type 'What is the total cost?']**

**[Screen: Response appears with cost breakdown]**

> "And if you have questions — 'What's the total cost?', 'Can I fit another activity?', 'What happens if this booking is cancelled?' — natural language, powered by the live itinerary context."

---

## Technical Highlights (1:25 - 1:45)

**[Screen: Side-by-side of pipeline flow diagram and code]**

> "Three things make this technically different:

> First, the scheduler is a real algorithm — greedy nearest-neighbor with Haversine distance calculations and time-window pruning. Not an LLM guessing at ordering.

> Second, the resilience score is proactive, not reactive. It evaluates fragility before anything breaks.

> Third, the repair agent does minimal-diff repair. It computes the smallest set of changes needed to fix a broken plan, and the UI highlights exactly what changed."

---

## Closing + Call to Action (1:45 - 2:00)

**[Screen: App fully visible with itinerary, resilience score, and diff panel]**

> "TravelPilot: AI-powered trip planning that doesn't just plan your trip — it manages it, stress-tests it, and repairs it when things go wrong. Built in 36 hours. Deployed live. Try it now."

**[Screen: URL displayed prominently]**

**[End card: TravelPilot logo + URL + GitHub link]**
