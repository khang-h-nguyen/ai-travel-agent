import os
import re
import httpx

from langchain.tools import tool
from app.destinations import validate_destination
from app.data.activities import ACTIVITIES

@tool
def validate_destination_tool(destination: str) -> dict:
    is_valid, dest_info = validate_destination(destination)
    
    if not is_valid:
        return {
            "valid": False,
            "error": dest_info
        }
    
    return {
        "valid": True,
        "name": dest_info["name"],
        "daily_budget": dest_info["avg_daily_budget"],
        "best_months": dest_info["best_months"]
    }

@tool
async def get_weather_tool(city: str) -> dict:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"available": False, "reason": "No API key"}
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},CA&appid={api_key}&units=metric"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "available": True,
                "temperature": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "feels_like": round(data["main"]["feels_like"])
            }
            
    except Exception as e:
        print(f"Weather API error: {e}")
        return {"available": False, "reason": str(e)}

@tool
def get_activities_tool(destination: str, interests: str, weather_description: str = "unknown") -> dict:
    """
    Get available activities for a destination. 
    Returns activities organized by category. You should select appropriate
    activities based on the user's interests AND current weather conditions.
    
    Consider:
    - Winter activities (skiing, snowshoeing) are GOOD in cold/snowy weather
    - Outdoor summer activities (hiking, beaches) might be bad in rain
    - Indoor activities (museums, food tours) work in any weather
    - Some users want outdoor activities even in less-than-perfect weather
    """
    city_activities = ACTIVITIES.get(destination.lower(), {})
    
    if not city_activities:
        return {
            "found": False,
            "reason": f"No activities in database for {destination}"
        }

    result = {
        "found": True,
        "destination": destination,
        "weather_context": weather_description,
        "categories": {}
    }
    
    interest_list = [i.strip().lower() for i in interests.split(",")]
    
    for category, activities in city_activities.items():
        category_meta = {
            "activities": activities[:4], 
            "matches_interest": any(interest in category for interest in interest_list)
        }
        result["categories"][category] = category_meta
    
    return result

@tool
def calculate_budget_tool(daily_rate: int, num_days: int) -> dict:
    total = daily_rate * num_days
    
    return {
        "total": total,
        "daily_rate": daily_rate,
        "num_days": num_days,
        "formatted": f"${total} total (${daily_rate}/day for {num_days} days)"
    }

def parse_duration_from_text(text):
    text_lower = text.lower()
    
    # Check for explicit day counts
    day_match = re.search(r"(\d+)\s*days?", text_lower)
    if day_match:
        return int(day_match.group(1))
    
    # Check for weeks
    week_match = re.search(r"(\d+)\s*weeks?", text_lower)
    if week_match:
        return int(week_match.group(1)) * 7
    
    # Check for weekend
    if "weekend" in text_lower:
        return 3
    
    # Check for common phrases
    if "week" in text_lower:
        return 7
    
    return None