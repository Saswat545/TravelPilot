"""Planner Agent — LLM-based intent parsing for travel activities.

Uses Gemini API (OpenAI-compatible) to convert user preferences into
structured activity candidates. The LLM does NOT do scheduling — that's
the scheduler engine's job.
"""

import json
import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from .prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_PROMPT

# Ensure .env is loaded regardless of cwd
_project_root = Path(__file__).parent.parent.parent
load_dotenv(_project_root / ".env")


def get_client() -> OpenAI:
    """Create OpenAI-compatible client pointing at Gemini."""
    return OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai"),
    )


def parse_planner_response(raw: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences and truncation."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (```json and ```)
        lines = [l for l in lines[1:] if not l.strip().startswith("```")]
        text = "\n".join(lines)

    # Try parsing as-is first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Repair truncated JSON: try closing unclosed arrays/objects
    repaired = text.rstrip()
    # Count open brackets
    open_brackets = repaired.count('[') - repaired.count(']')
    open_braces = repaired.count('{') - repaired.count('}')
    open_quotes = repaired.count('"') % 2  # odd = unclosed quote

    if open_quotes:
        # Truncated mid-string — cut back to last complete activity
        last_brace = repaired.rfind('}')
        if last_brace > 0:
            repaired = repaired[:last_brace + 1]
            # Check if we're inside the activities array
            # Add closing brackets/braces as needed
            open_brackets = repaired.count('[') - repaired.count(']')
            open_braces = repaired.count('{') - repaired.count('}')

    repaired += '\n' + ']' * open_brackets + '}' * open_braces

    try:
        result = json.loads(repaired)
        if 'activities' in result and isinstance(result['activities'], list):
            print(f"Repaired truncated JSON: recovered {len(result['activities'])} activities")
            return result
    except json.JSONDecodeError:
        pass

    # Last resort: try to extract just the activities array
    import re
    match = re.search(r'\[\s*\{[^\]]*\}\s*\]', text, re.DOTALL)
    if match:
        try:
            activities = json.loads(match.group())
            return {'activities': activities, 'reasoning': 'Extracted from partial response'}
        except json.JSONDecodeError:
            pass

    raise json.JSONDecodeError('Could not parse response', text, 0)


def plan_activities(
    destination: str,
    start_date: str,
    end_date: str,
    budget: float,
    interests: list[str],
    num_travelers: int = 1,
) -> dict:
    """Call LLM to generate candidate activities for a trip.

    Returns dict with 'activities' list and 'reasoning' string.
    On failure, returns mock data fallback.
    """
    from datetime import datetime

    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    num_days = max(1, (end - start).days + 1)
    daily_budget = budget / num_days

    user_msg = PLANNER_USER_PROMPT.format(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        num_days=num_days,
        budget=budget,
        daily_budget=daily_budget,
        interests=", ".join(interests),
        num_travelers=num_travelers,
    )

    for attempt in range(2):
        try:
            client = get_client()
            model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.7,
                max_tokens=16384,
            )

            raw = response.choices[0].message.content
            result = parse_planner_response(raw)

            if "activities" not in result:
                raise ValueError("Missing 'activities' key in response")

            return result

        except Exception as e:
            if attempt == 0:
                print(f"Planner Agent attempt {attempt + 1} failed: {e}, retrying...")
                continue
            print(f"Planner Agent failed after 2 attempts: {e}, using mock data")
            return _mock_activities(destination, interests)


def _mock_activities(destination: str, interests: list[str]) -> dict:
    """Fallback mock data when LLM fails. Uses real venue data for demo cities."""

    mock_data = {
        "india": [
            {"id": "red_fort", "name": "Red Fort (Lal Qila)", "category": "culture", "duration_minutes": 120, "cost": 8, "location": {"lat": 28.6562, "lng": 77.2410}, "time_window": {"earliest": "09:30", "latest": "17:00"}, "priority": 5, "description": "Massive red sandstone fortress in Delhi, UNESCO World Heritage Site"},
            {"id": "chandni_chowk", "name": "Chandni Chowk Market", "category": "food", "duration_minutes": 120, "cost": 15, "location": {"lat": 28.6506, "lng": 77.2334}, "time_window": {"earliest": "09:00", "latest": "21:00"}, "priority": 4, "description": "One of Delhi's oldest and busiest markets, famous for street food"},
            {"id": "india_gate", "name": "India Gate", "category": "culture", "duration_minutes": 60, "cost": 0, "location": {"lat": 28.6129, "lng": 77.2295}, "time_window": {"earliest": "00:00", "latest": "23:59"}, "priority": 4, "description": "War memorial arch in New Delhi, 42 meters tall"},
            {"id": "lotus_temple", "name": "Lotus Temple", "category": "culture", "duration_minutes": 60, "cost": 0, "location": {"lat": 28.5535, "lng": 77.2588}, "time_window": {"earliest": "09:00", "latest": "17:30"}, "priority": 4, "description": "Bahai House of Worship shaped like a lotus flower, open to all"},
            {"id": "humayun_tomb", "name": "Humayun's Tomb", "category": "culture", "duration_minutes": 90, "cost": 7, "location": {"lat": 28.5933, "lng": 77.2507}, "time_window": {"earliest": "06:00", "latest": "18:00"}, "priority": 5, "description": "Mughal garden tomb, precursor to the Taj Mahal"},
            {"id": "akshardham", "name": "Akshardham Temple", "category": "culture", "duration_minutes": 180, "cost": 0, "location": {"lat": 28.6127, "lng": 77.2773}, "time_window": {"earliest": "10:00", "latest": "18:00"}, "priority": 5, "description": "Hindu temple complex with intricate carvings and boat ride"},
            {"id": "qutub_minar", "name": "Qutub Minar", "category": "culture", "duration_minutes": 90, "cost": 7, "location": {"lat": 28.5244, "lng": 77.1855}, "time_window": {"earliest": "07:00", "latest": "17:00"}, "priority": 4, "description": "73-meter tall minaret, tallest brick minaret in the world"},
            {"id": "connaught_place", "name": "Connaught Place", "category": "shopping", "duration_minutes": 120, "cost": 30, "location": {"lat": 28.6315, "lng": 77.2167}, "time_window": {"earliest": "10:00", "latest": "21:00"}, "priority": 3, "description": "Colonial-era commercial hub with shops, restaurants, and theaters"},
            {"id": "nizamuddin", "name": "Nizamuddin Dargah", "category": "culture", "duration_minutes": 60, "cost": 0, "location": {"lat": 28.5931, "lng": 77.2445}, "time_window": {"earliest": "05:00", "latest": "22:00"}, "priority": 3, "description": "Sufi shrine with evening qawwali music performances"},
            {"id": "taj_mahal", "name": "Taj Mahal (Day Trip)", "category": "culture", "duration_minutes": 240, "cost": 14, "location": {"lat": 27.1751, "lng": 78.0421}, "time_window": {"earliest": "06:00", "latest": "15:00"}, "priority": 5, "description": "Day trip to Agra — iconic white marble mausoleum, one of the Seven Wonders"},
        ],
        "tokyo": [
            {"id": "sensoji", "name": "Senso-ji Temple", "category": "culture", "duration_minutes": 90, "cost": 0, "location": {"lat": 35.7148, "lng": 139.7967}, "time_window": {"earliest": "06:00", "latest": "17:00"}, "priority": 5, "description": "Ancient Buddhist temple in Asakusa, Tokyo's oldest temple"},
            {"id": "tsukiji", "name": "Tsukiji Outer Market", "category": "food", "duration_minutes": 120, "cost": 30, "location": {"lat": 35.6654, "lng": 139.7707}, "time_window": {"earliest": "05:00", "latest": "14:00"}, "priority": 4, "description": "Famous food market with fresh sushi and street food"},
            {"id": "shibuya", "name": "Shibuya Crossing & Hachiko", "category": "entertainment", "duration_minutes": 60, "cost": 0, "location": {"lat": 35.6595, "lng": 139.7004}, "time_window": {"earliest": "00:00", "latest": "23:59"}, "priority": 4, "description": "World's busiest pedestrian crossing and the famous Hachiko statue"},
            {"id": "meiji", "name": "Meiji Shrine", "category": "culture", "duration_minutes": 90, "cost": 0, "location": {"lat": 35.6764, "lng": 139.6993}, "time_window": {"earliest": "05:00", "latest": "18:00"}, "priority": 5, "description": "Peaceful Shinto shrine in a forested area near Harajuku"},
            {"id": "harajuku", "name": "Harajuku & Takeshita Street", "category": "shopping", "duration_minutes": 120, "cost": 50, "location": {"lat": 35.6702, "lng": 139.7026}, "time_window": {"earliest": "10:00", "latest": "20:00"}, "priority": 3, "description": "Trendy fashion district with unique shops and cafes"},
            {"id": "shinjuku", "name": "Shinjuku Gyoen National Garden", "category": "nature", "duration_minutes": 90, "cost": 5, "location": {"lat": 35.6852, "lng": 139.7100}, "time_window": {"earliest": "09:00", "latest": "16:30"}, "priority": 4, "description": "Beautiful park with Japanese, English, and French gardens"},
            {"id": "akihabara", "name": "Akihabara Electric Town", "category": "entertainment", "duration_minutes": 120, "cost": 40, "location": {"lat": 35.6984, "lng": 139.7731}, "time_window": {"earliest": "10:00", "latest": "21:00"}, "priority": 3, "description": "Hub for anime, manga, and electronics"},
            {"id": "teamlab", "name": "teamLab Borderless", "category": "entertainment", "duration_minutes": 150, "cost": 32, "location": {"lat": 35.6264, "lng": 139.7838}, "time_window": {"earliest": "10:00", "latest": "21:00"}, "priority": 5, "description": "Immersive digital art museum"},
        ],
        "paris": [
            {"id": "eiffel", "name": "Eiffel Tower", "category": "culture", "duration_minutes": 120, "cost": 26, "location": {"lat": 48.8584, "lng": 2.2945}, "time_window": {"earliest": "09:30", "latest": "23:00"}, "priority": 5, "description": "Iconic iron lattice tower, symbol of Paris"},
            {"id": "louvre", "name": "Louvre Museum", "category": "culture", "duration_minutes": 180, "cost": 22, "location": {"lat": 48.8606, "lng": 2.3376}, "time_window": {"earliest": "09:00", "latest": "18:00"}, "priority": 5, "description": "World's largest art museum, home to the Mona Lisa"},
            {"id": "notre_dame", "name": "Notre-Dame Cathedral", "category": "culture", "duration_minutes": 60, "cost": 0, "location": {"lat": 48.8530, "lng": 2.3499}, "time_window": {"earliest": "08:00", "latest": "18:45"}, "priority": 4, "description": "Medieval cathedral, masterpiece of French Gothic architecture"},
            {"id": "montmartre", "name": "Montmartre & Sacre-Coeur", "category": "culture", "duration_minutes": 120, "cost": 0, "location": {"lat": 48.8867, "lng": 2.3431}, "time_window": {"earliest": "06:00", "latest": "22:30"}, "priority": 4, "description": "Historic hilltop neighborhood with basilica and artists' square"},
            {"id": "seine_cruise", "name": "Seine River Cruise", "category": "entertainment", "duration_minutes": 60, "cost": 15, "location": {"lat": 48.8600, "lng": 2.3400}, "time_window": {"earliest": "10:00", "latest": "22:30"}, "priority": 3, "description": "Scenic boat tour along the Seine past major landmarks"},
            {"id": "champs", "name": "Champs-Elysees & Arc de Triomphe", "category": "shopping", "duration_minutes": 120, "cost": 30, "location": {"lat": 48.8738, "lng": 2.2950}, "time_window": {"earliest": "10:00", "latest": "21:00"}, "priority": 4, "description": "Famous avenue with luxury shops and triumphal arch"},
            {"id": "orangerie", "name": "Musee de l'Orangerie", "category": "culture", "duration_minutes": 90, "cost": 12, "location": {"lat": 48.8608, "lng": 2.3225}, "time_window": {"earliest": "09:00", "latest": "18:00"}, "priority": 3, "description": "Monet's Water Lilies in oval galleries"},
            {"id": "latin_quarter", "name": "Latin Quarter & Shakespeare & Co", "category": "entertainment", "duration_minutes": 90, "cost": 10, "location": {"lat": 48.8499, "lng": 2.3473}, "time_window": {"earliest": "10:00", "latest": "20:00"}, "priority": 3, "description": "Historic student district with famous English bookshop"},
        ],
    }

    dest_lower = destination.lower()
    for key in mock_data:
        if key in dest_lower:
            return {
                "activities": mock_data[key],
                "reasoning": f"Selected top attractions in {destination} based on popularity and category variety.",
            }

    # Generic fallback — generates plausible activities around a seed coordinate
    # so the scheduler has something to work with even without LLM data
    base_lat, base_lng = _destination_coords(destination)
    spread = 0.02  # ~2km spread
    activities = [
        {"id": "landmark", "name": f"{destination} Main Landmark", "category": "culture", "duration_minutes": 120, "cost": 10, "location": {"lat": base_lat, "lng": base_lng}, "time_window": {"earliest": "09:00", "latest": "17:00"}, "priority": 5, "description": f"The most famous landmark in {destination}"},
        {"id": "market", "name": f"{destination} Central Market", "category": "food", "duration_minutes": 90, "cost": 20, "location": {"lat": base_lat + spread * 0.3, "lng": base_lng + spread * 0.2}, "time_window": {"earliest": "08:00", "latest": "20:00"}, "priority": 4, "description": "Local market with street food and crafts"},
        {"id": "museum", "name": f"{destination} National Museum", "category": "culture", "duration_minutes": 120, "cost": 8, "location": {"lat": base_lat - spread * 0.2, "lng": base_lng + spread * 0.4}, "time_window": {"earliest": "10:00", "latest": "17:00"}, "priority": 4, "description": "Museum showcasing local history and art"},
        {"id": "park", "name": f"{destination} City Park", "category": "nature", "duration_minutes": 60, "cost": 0, "location": {"lat": base_lat + spread * 0.5, "lng": base_lng - spread * 0.3}, "time_window": {"earliest": "06:00", "latest": "19:00"}, "priority": 3, "description": "Green space for walks and relaxation"},
        {"id": "restaurant", "name": f"Local Restaurant Row", "category": "food", "duration_minutes": 90, "cost": 25, "location": {"lat": base_lat - spread * 0.1, "lng": base_lng - spread * 0.5}, "time_window": {"earliest": "11:00", "latest": "22:00"}, "priority": 3, "description": "Popular dining area with local cuisine"},
        {"id": "temple", "name": f"{destination} Historic Temple", "category": "culture", "duration_minutes": 60, "cost": 0, "location": {"lat": base_lat + spread * 0.4, "lng": base_lng + spread * 0.6}, "time_window": {"earliest": "06:00", "latest": "18:00"}, "priority": 4, "description": "Historic religious site with architectural beauty"},
        {"id": "shopping", "name": f"{destination} Shopping District", "category": "shopping", "duration_minutes": 120, "cost": 40, "location": {"lat": base_lat - spread * 0.4, "lng": base_lng + spread * 0.1}, "time_window": {"earliest": "10:00", "latest": "21:00"}, "priority": 3, "description": "Main commercial area with shops and cafes"},
        {"id": "viewpoint", "name": f"{destination} Scenic Viewpoint", "category": "nature", "duration_minutes": 45, "cost": 5, "location": {"lat": base_lat + spread * 0.6, "lng": base_lng - spread * 0.4}, "time_window": {"earliest": "06:00", "latest": "19:00"}, "priority": 4, "description": "Elevated spot with panoramic views of the city"},
    ]
    return {
        "activities": activities,
        "reasoning": f"Generated fallback activities for {destination}. For best results, ensure the Gemini API key is configured.",
    }


def _destination_coords(destination: str) -> tuple[float, float]:
    """Return approximate coordinates for common destinations.
    Falls back to (28.6, 77.2) — Delhi — for unknown destinations.
    """
    known = {
        "delhi": (28.6139, 77.2090),
        "agra": (27.1767, 78.0081),
        "mumbai": (19.0760, 72.8777),
        "bangalore": (12.9716, 77.5946),
        "jaipur": (26.9124, 75.7873),
        "kolkata": (22.5726, 88.3639),
        "chennai": (13.0827, 80.2707),
        "goa": (15.2993, 74.1240),
        "varanasi": (25.3176, 82.9739),
        "tokyo": (35.6762, 139.6503),
        "paris": (48.8566, 2.3522),
        "london": (51.5074, -0.1278),
        "new york": (40.7128, -74.0060),
        "rome": (41.9028, 12.4964),
        "bangkok": (13.7563, 100.5018),
        "dubai": (25.2048, 55.2708),
        "singapore": (1.3521, 103.8198),
        "sydney": (-33.8688, 151.2093),
        "beijing": (39.9042, 116.4074),
        "istanbul": (41.0082, 28.9784),
    }
    dest_lower = destination.lower()
    for key, coords in known.items():
        if key in dest_lower:
            return coords
    return (28.6, 77.2)  # Default: Delhi
