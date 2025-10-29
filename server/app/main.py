from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

from app.agent import extract_travel_intent


app = FastAPI(title="AI Travel Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str


@app.post("/api/chat")
async def chat(message: ChatMessage):
    result = extract_travel_intent(message.message)

    if "error" in result:
        return {"response": f"Sorry, I encountered an error: {result['error']}"}

    response_parts = []

    validation = result.get("validation", {})
    if not validation.get("is_valid"):
        error_msg = validation.get("error", "Unknown error")
        return {
            "response": f"❌ {error_msg}\n\nPlease try a Canadian destination like Toronto, Vancouver, Montreal, etc."
        }

    dest_info = validation.get("destination_info", {})
    response_parts.append(f"✈️ Great choice! {dest_info.get('name', 'Your destination')} is perfect!")

    if "estimated_budget" in result:
        budget = result["estimated_budget"]
        response_parts.append(f"\n💰 Budget: ${budget['total']} ({budget['num_days']} days)")
        response_parts.append(f"   ${budget['daily_budget']}/day")

    if "suggested_activities" in result:
        activities = result["suggested_activities"]
        response_parts.append(f"\n🎯 Suggested Activities:")
        for i, activity in enumerate(activities, 1):
            response_parts.append(f"   {i}. {activity}")

    if dest_info.get("best_months"):
        months = dest_info["best_months"][:3]
        response_parts.append(f"\n📅 Best time: {', '.join(months)}")

    return {"response": "\n".join(response_parts)}
