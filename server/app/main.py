"""
FastAPI Main Application

This is the entry point for the AI Travel Planner backend.
It sets up CORS, routes, and basic health check endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Travel Planner Agent",
    description="Intelligent travel planning system with natural language understanding",
    version="0.1.0",
)

# Configure CORS - Allow frontend to communicate with backend
# In development, we allow all origins. In production, restrict this!
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:5173"),
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ============================================
# Health Check Endpoints
# ============================================

@app.get("/")
async def root():
    """
    Root endpoint - Basic API information
    """
    return {
        "message": "AI Travel Planner Agent API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",  # FastAPI auto-generates interactive API docs
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Used to verify the server is running properly.
    Returns server status and configuration info.
    """
    return {
        "status": "healthy",
        "service": "ai-travel-planner",
        "environment": {
            "llm_provider": os.getenv("LLM_PROVIDER", "not_configured"),
            "has_api_key": bool(
                os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
            ),
        },
    }


@app.get("/api/config")
async def get_config():
    """
    Configuration endpoint
    
    Returns non-sensitive configuration information.
    Useful for frontend to know what features are available.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    
    return {
        "llm_provider": llm_provider,
        "model": os.getenv("OPENAI_MODEL") if llm_provider == "openai" else os.getenv("ANTHROPIC_MODEL"),
        "features": {
            "intent_extraction": True,
            "destination_validation": True,
            "itinerary_generation": True,
        },
    }


# ============================================
# Startup Event
# ============================================

@app.on_event("startup")
async def startup_event():
    """
    Runs when the server starts
    
    Good place to:
    - Verify environment variables
    - Initialize connections
    - Load data
    """
    print("=" * 50)
    print("🚀 AI Travel Planner Agent - Starting")
    print("=" * 50)
    
    # Check if API key is configured
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    
    if llm_provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  WARNING: OPENAI_API_KEY not found in .env")
        else:
            print(f"✅ OpenAI API key configured")
            print(f"   Model: {os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')}")
    
    elif llm_provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("⚠️  WARNING: ANTHROPIC_API_KEY not found in .env")
        else:
            print(f"✅ Anthropic API key configured")
            print(f"   Model: {os.getenv('ANTHROPIC_MODEL', 'claude-3-5-sonnet-20241022')}")
    
    print("=" * 50)
    print(f"📡 Server running at: http://localhost:{os.getenv('BACKEND_PORT', '8000')}")
    print(f"📚 API docs at: http://localhost:{os.getenv('BACKEND_PORT', '8000')}/docs")
    print("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the server shuts down
    
    Good place to:
    - Close database connections
    - Clean up resources
    """
    print("\n🛑 AI Travel Planner Agent - Shutting down")


# ============================================
# For Development: Run with `uvicorn app.main:app --reload`
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("BACKEND_PORT", "8000"))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,  # Auto-reload on code changes (development only!)
    )