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
    result = await extract_travel_intent(message.message)
    
    if "error" in result:
        return {
            "response": f"Sorry, I encountered an error: {result['error']}",
            "steps": result.get("steps", [])
        }
    
    return {
        "response": result["response"],
        "steps": result["steps"]
    }