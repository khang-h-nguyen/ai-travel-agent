# AI Travel Planner

An AI-powered travel planning assistant for Canadian destinations. Built with Claude (Anthropic), FastAPI, and React.

## Overview

Describe your ideal trip in natural language and receive a complete itinerary with budget estimates, activity suggestions, and travel recommendations.

**Supported Destinations:** Toronto, Vancouver, Montreal, Quebec City, Banff, Victoria, Ottawa, Calgary, Niagara Falls, Whistler

## Tech Stack

- **Backend:** FastAPI (Python), Claude API (Anthropic)
- **Frontend:** React, TypeScript, Vite
- **LLM:** Claude Haiku for intent extraction and semantic matching

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Anthropic API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-travel-planner.git
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

### Step 1: User Input

The planner presents a clean interface with example prompts. Users describe their trip in natural language.

![Screenshot: Landing page with input form and example prompts]

**Example inputs:**
- "5-day cultural trip to Toronto on a budget"
- "Family vacation to Victoria, love beaches and adventure"
- "Romantic week in Banff with food and culture"

---

### Step 2: Intent Extraction

The backend receives the request and sends it to Claude for intent extraction.

![Screenshot: Browser console showing API request to /api/chat]

Claude analyzes the message and extracts structured data:
- Destination
- Duration (converts "1 weekend" to "3 days", "1 week" to "7 days")
- Budget level
- Interests (activities the user enjoys)

![Screenshot: Terminal showing Claude's JSON response]

**Server logs show:**
```
Sending to Claude...
User said: Family vacation to Victoria, love beaches and adventure
Claude responded!

Extracted data:
  Destination: Victoria
  Duration: 7 days
  Budget: mid-range
  Interests: ['beaches', 'adventure']
```

---

### Step 3: Destination Validation

The agent validates the destination against the Canadian cities database.

![Screenshot: Terminal showing destination validation]

**Server logs show:**
```
Found: Victoria, British Columbia
Average budget: $140/day
Best time: April, May, June
```

If the destination isn't in the database, the user receives an error with suggestions.

---

### Step 4: Budget Calculation

The system calculates the estimated trip cost based on:
- Destination's average daily budget
- Trip duration in days

![Screenshot: Terminal showing budget calculation]

**Server logs show:**
```
Estimated total: $980
```

Formula: `Daily Rate × Number of Days = Total Budget`

---

### Step 5: Activity Matching

The agent attempts to match user interests to activity categories.

**First: Exact Match**
If interests match existing categories (e.g., "culture", "food"), activities are returned immediately.

![Screenshot: Terminal showing exact match]

**Fallback: Semantic Matching**
If no exact match (e.g., "beaches and adventure" doesn't match "nature"), Claude performs semantic mapping.

![Screenshot: Terminal showing semantic matching with Claude]

**Server logs show:**
```
No exact match for ['beaches', 'adventure'], using semantic matching...
Mapped to categories: ['nature']
```

Claude maps the interests to the closest available categories for that destination.

---

### Step 6: Response Generation

The backend formats all collected data into a readable itinerary.

![Screenshot: Terminal showing final response assembly]

---

### Step 7: Display Results

The frontend displays the complete itinerary with:
- Destination confirmation
- Budget estimate (total and daily)
- 8 suggested activities
- Best months to visit

![Screenshot: Frontend showing complete itinerary results]

Users can click "Plan Another Trip" to start over.

---

## Current Limitations & Future Improvements

**No Conversation Memory**
- Each query is independent
- Cannot handle follow-up questions or refinements
- **Future:** Add chat history and multi-turn conversations

**Static Response Formatting**
- Fixed template structure
- **Future:** Use Claude to generate dynamic, natural responses

**Limited Dataset**
- Only 10 Canadian destinations
- No real-time data (weather, prices, events)
- **Future:** Expand to international destinations, integrate live APIs

**Single Budget Tier**
- Uses only average daily rates
- **Future:** Support budget/mid-range/luxury tiers with different recommendations

**No Persistence**
- Itineraries aren't saved
- **Future:** Add user accounts and itinerary storage

## License

MIT