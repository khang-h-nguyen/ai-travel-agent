from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os

load_dotenv()

from app.agent import extract_travel_intent


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("\n" + "=" * 60)
    print("AI Travel Planner - Starting")
    print("=" * 60)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("Anthropic API key found")
        print(f"Using model: {os.getenv('ANTHROPIC_MODEL', 'claude-haiku-4-5-20251001')}")
    else:
        print("WARNING: No Anthropic API key found!")
        print("Add ANTHROPIC_API_KEY to your .env file")

    print("=" * 60)
    print(f"Server: http://localhost:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print("=" * 60)
    print()

    yield

    print("\nShutting down...")


app = FastAPI(
    title="AI Travel Planner Agent",
    description="Simple travel planning with AI",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str


@app.get("/")
async def root():
    return {
        "message": "AI Travel Planner API",
        "status": "running",
        "docs": "http://localhost:8000/docs"
    }


@app.get("/api/health")
async def health_check():
    has_api_key = bool(os.getenv("ANTHROPIC_API_KEY"))

    return {
        "status": "healthy" if has_api_key else "missing_api_key",
        "api_key_configured": has_api_key,
    }


@app.post("/api/extract-intent")
async def extract_intent(message: ChatMessage):
    print(f"\nReceived request: {message.message}")

    result = extract_travel_intent(message.message)

    if "error" in result:
        return {
            "success": False,
            "error": result["error"]
        }

    return {
        "success": True,
        "intent": result
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)