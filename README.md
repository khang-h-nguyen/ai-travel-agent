# AI Travel Planner

Welcome to the AI Travel Agent repository! This project is an autonomous travel planning assistant for Canadian destinations that uses LangChain's ReAct framework with Claude API to orchestrate tools and generate context-aware itineraries. Built with FastAPI and React (TypeScript).

## Overview

Describe your ideal trip in natural language and receive a complete itinerary with budget estimates, weather-aware activity suggestions, and travel recommendations. The agent maintains conversation memory, allowing you to refine your plans through natural dialogue.

**Supported Destinations:** Toronto, Vancouver, Montreal, Quebec City, Banff, Victoria, Ottawa, Calgary, Niagara Falls, Whistler

## Tech Stack

- **Backend:** FastAPI (Python), LangChain, Claude API
- **Frontend:** React, TypeScript, Vite
- **Agent Framework:** LangChain ReAct pattern with tool calling
- **External APIs:** OpenWeather API for real-time weather data

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Anthropic API key
- OpenWeather API key (optional, for weather-based recommendations)

### Installation

1. Clone the repository
```bash
git clone https://github.com/khang-h-nguyen/ai-travel-agent.git
cd ai-travel-planner
```

2. Backend setup
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create `.env` file in `server/` directory:
```
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=your_model_here
OPENWEATHER_API_KEY=your_key_here  # Optional
```

4. Frontend setup
```bash
cd client
npm install
```

### Running the Application

Open two terminals:

**Terminal 1 - Backend:**
```bash
cd server
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

Open browser to `http://localhost:3001`

## How It Works

### Step 1: User Input & Session Management

The planner presents a clean interface with example prompts. Users describe their trip in natural language. Each conversation creates a session that maintains context for refinements.

<img width="1271" height="854" alt="Screenshot 2025-10-29 at 2 51 57 PM" src="https://github.com/user-attachments/assets/0648683e-600c-4297-9781-2e58b3d4ac1b" />

**Example inputs:**
- "5-day cultural trip to Toronto on a budget"
- "Family vacation to Victoria, love beaches and adventure"
- "Romantic week in Banff with food and culture"

**Follow-up refinements:**
- "Make it 7 days instead"
- "Add more outdoor activities"
- "Change to Vancouver"

---

### Step 2: Agent Orchestration with ReAct Pattern

The backend uses LangChain's ReAct framework where the agent **reasons** about the request and **acts** by calling tools autonomously.

**The agent has 4 tools available:**
1. **validate_destination_tool** - Checks if destination exists
2. **get_weather_tool** - Fetches real-time weather from OpenWeather API
3. **get_activities_tool** - Returns activities filtered by interests AND weather
4. **calculate_budget_tool** - Computes trip costs

---

### Step 3: Tool Execution - Destination Validation

The agent **always validates the destination first** to fail fast if the location isn't supported.

**If valid:**
```
Found: Banff, Alberta
Average budget: $140/day
Best time: June, July, August
```

**If invalid:**

<img width="917" height="279" alt="Screenshot 2025-10-29 at 3 06 49 PM" src="https://github.com/user-attachments/assets/cdeb2761-1320-4e8d-aa92-029db046fd44" />

The agent stops execution and provides clear feedback about available destinations.

---

### Step 4: Tool Execution - Weather Integration

If OpenWeather API is configured, the agent checks current conditions to provide **context-aware recommendations**.

**Weather influences activity selection:**
- Cold/snow → Winter activities (skiing, snowshoeing, hot springs)
- Rain → Indoor activities (museums, food tours, shopping)
- Sunny → Outdoor activities (hiking, beaches, sightseeing)

**Example output:**
```
Current weather: -2°C, light snow
Perfect conditions for: Skiing at Lake Louise, Ice skating, Hot springs at Banff Upper Hot Springs
```

---

### Step 5: Tool Execution - Activity Matching

The agent retrieves activities filtered by both user interests AND current weather conditions.

**The agent reasons about weather context:**
- User wants "hiking" + weather is "snowy" → Suggests snowshoeing as an alternative
- User wants "beaches" + weather is "rainy" → Suggests indoor alternatives or mentions weather consideration

<img width="616" height="36" alt="Screenshot 2025-10-29 at 3 03 20 PM" src="https://github.com/user-attachments/assets/583c52fc-920e-4299-8add-9d6bf48b3942" />

Activities are organized by category with the agent selecting the most relevant ones based on the full context.

---

### Step 6: Tool Execution - Budget Calculation

The agent calculates the estimated trip cost:

```
Formula: Daily Rate × Number of Days = Total Budget
Example: $140/day × 5 days = $700 total
```

Duration is automatically parsed from phrases like:
- "weekend" → 3 days
- "1 week" → 7 days
- "5 days" → 5 days

---

### Step 7: Display Results & Conversation Memory

The frontend displays the complete itinerary with:
- Destination confirmation
- Current weather conditions
- Context-aware activity recommendations
- Budget estimate (total and daily)
- Best months to visit

<img width="917" height="710" alt="Screenshot 2025-10-29 at 3 06 27 PM" src="https://github.com/user-attachments/assets/c87982eb-5b9d-4a93-9b91-7488d8a9889a" />

**Conversation memory enables refinements:**
- Input field remains visible with refinement hints
- Button changes to "Update Plan"
- Session maintains full chat history (30-minute timeout)
- Agent remembers previous destination, interests, and preferences

**Example conversation flow:**
1. "5-day trip to Vancouver, love hiking"
2. "Make it 7 days instead" ← Agent remembers Vancouver and hiking
3. "Add more food activities" ← Agent updates while keeping 7 days and Vancouver

---

## Current Capabilities & Limitations

**✅ Implemented Features**
- **Autonomous agent** with LangChain ReAct framework
- **Tool orchestration** - Agent decides when and how to call tools
- **Real-time weather integration** via OpenWeather API
- **Conversation memory** with session-based chat history (30-minute timeout)
- **Iterative refinement** - Multi-turn dialogues for plan adjustments
- **Validation guardrails** - Fails fast with clear error messages

**⚠️ Current Limitations**

**In-Memory Sessions Only**
- Sessions expire after 30 minutes of inactivity
- No persistent storage across server restarts
- **Future:** Add database persistence with user accounts

**Limited Dataset**
- Only 10 Canadian destinations
- Static activity database
- **Future:** Expand to international destinations, integrate live booking APIs

**Single Budget Tier**
- Uses only average daily rates
- **Future:** Support budget/mid-range/luxury tiers with different recommendations

**No Itinerary Export**
- Results displayed in browser only
- **Future:** Add PDF export, calendar integration, email functionality

## Architecture

```
User Input
    ↓
Frontend (React + TypeScript)
    ↓
FastAPI Backend
    ↓
LangChain ReAct Agent
    ↓
┌─────────────────────────────────┐
│ Tool 1: validate_destination    │
│ Tool 2: get_weather (OpenWeather)│
│ Tool 3: get_activities          │
│ Tool 4: calculate_budget        │
└─────────────────────────────────┘
    ↓
Session Store (In-Memory)
    ↓
Formatted Response → User
```

## License

MIT
