"""Planner Agent — LLM-based intent parsing for travel activities.

Uses Gemini API (OpenAI-compatible) to convert user preferences into
structured activity candidates. The LLM does NOT do scheduling — that's
the scheduler engine's job.
"""

import json
import os
from openai import OpenAI
from .prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_PROMPT


def get_client() -> OpenAI:
    """Create OpenAI-compatible client pointing at Gemini."""
    return OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai"),
    )


def parse_planner_response(raw: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (```json and ```)
        lines = [l for l in lines[1:] if not l.strip().startswith("```")]
        text = "\n".join(lines)
    return json.loads(text)


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
            max_tokens=4096,
        )

        raw = response.choices[0].message.content
        result = parse_planner_response(raw)

        # Validate structure
        if "activities" not in result:
            raise ValueError("Missing 'activities' key in response")

        return result

    except Exception as e:
        print(f"Planner Agent failed: {e}, using mock data")
        return _mock_activities(destination, interests)


def _mock_activities(destination: str, interests: list[str]) -> dict:
    """Fallback mock data when LLM fails. Uses real venue data for demo cities."""

    mock_data = {
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

    # Generic fallback
    return {
        "activities": [
            {"id": "city_center", "name": f"{destination} City Center", "category": "culture", "duration_minutes": 120, "cost": 0, "location": {"lat": 0.0, "lng": 0.0}, "time_window": {"earliest": "09:00", "latest": "17:00"}, "priority": 4, "description": "Explore the main city center"},
            {"id": "local_food", "name": "Local Food Market", "category": "food", "duration_minutes": 90, "cost": 25, "location": {"lat": 0.001, "lng": 0.001}, "time_window": {"earliest": "10:00", "latest": "15:00"}, "priority": 4, "description": "Try local cuisine at a popular market"},
            {"id": "park", "name": "Central Park", "category": "nature", "duration_minutes": 60, "cost": 0, "location": {"lat": 0.002, "lng": 0.002}, "time_window": {"earliest": "08:00", "latest": "18:00"}, "priority": 3, "description": "Relax in the main city park"},
        ],
        "reasoning": f"Generic fallback for {destination}. For best results, use Tokyo or Paris as demo destinations.",
    }
