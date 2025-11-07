import os
import httpx
from typing import Dict, Optional


async def get_weather(city: str) -> Optional[Dict]:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Warning: No OpenWeather API key found")
        return None
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},CA&appid={api_key}&units=metric"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url) 
            response.raise_for_status()
            data = response.json()
            
            return {
                "temperature": round(data["main"]["temp"]),  
                "description": data["weather"][0]["description"],
                "feels_like": round(data["main"]["feels_like"]),
            }
            
    except httpx.HTTPStatusError as e:
        print(f"Weather API HTTP error: {e.response.status_code}")
        return None
    except httpx.TimeoutException:
        print("Weather API timeout - took longer than 10 seconds")
        return None
    except Exception as e:
        print(f"Weather API error: {e}")
        return None
    