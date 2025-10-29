# AI Travel Planner

An AI-powered travel planning assistant for Canadian destinations. Built with FastAPI, and React (TypeScript).

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

<img width="1271" height="854" alt="Screenshot 2025-10-29 at 2 51 57 PM" src="https://github.com/user-attachments/assets/0648683e-600c-4297-9781-2e58b3d4ac1b" />


**Example inputs:**
- "5-day cultural trip to Toronto on a budget"
- "Family vacation to Victoria, love beaches and adventure"
- "Romantic week in Banff with food and culture"

---

### Step 2: Intent Extraction

The backend receives the request and sends it to Claude for intent extraction.

Claude analyzes the message and extracts structured data:
- Destination
- Duration (converts "1 weekend" to "3 days", "1 week" to "7 days")
- Budget level
- Interests (activities the user enjoys)

<img width="741" height="225" alt="Screenshot 2025-10-29 at 2 59 04 PM" src="https://github.com/user-attachments/assets/ac599030-583d-4560-8f75-f052755e14df" />

**Server logs show:**
```
User said: I want a hiking trip to Banff for 5 days. Suggest good food spots too.

Extracted data:
  Destination: Banff
  Duration: 5 days
  Budget: None
  Interests: ['hiking', 'food']
```

---

### Step 3: Destination Validation

The agent validates the destination against the Canadian cities database.

**Server logs show:**
```
Found: Banff, Alberta
Average budget: $140/day
Best time: June, July, August
```

If the destination isn't in the database, the user receives an error with suggestions.

<img width="917" height="279" alt="Screenshot 2025-10-29 at 3 06 49 PM" src="https://github.com/user-attachments/assets/cdeb2761-1320-4e8d-aa92-029db046fd44" />


---

### Step 4: Budget Calculation

The system calculates the estimated trip cost based on:
- Destination's average daily budget
- Trip duration in days

**Server logs show:**
```
Estimated total: $700
```

Formula: `Average Daily Rate × Number of Days = Total Budget`

---

### Step 5: Activity Matching

The agent attempts to match user interests to activity categories.

**First: Exact Match**
If interests match existing categories (e.g., "culture", "food"), activities are returned immediately.

**Fallback: Semantic Matching**
If no exact match (e.g., "beaches and adventure" doesn't match "nature"), Claude performs semantic mapping.

<img width="616" height="36" alt="Screenshot 2025-10-29 at 3 03 20 PM" src="https://github.com/user-attachments/assets/583c52fc-920e-4299-8add-9d6bf48b3942" />


**Server logs show:**
```
No exact match for ['hiking', 'food'], using semantic matching...
Mapped to categories: ['nature', 'outdoor', 'adventure']
```

Claude maps the interests to the closest available categories for that destination.

---

### Step 6: Display Results

The frontend displays the complete itinerary with:
- Destination confirmation
- Budget estimate (total and daily)
- 8 suggested activities
- Best months to visit

<img width="917" height="710" alt="Screenshot 2025-10-29 at 3 06 27 PM" src="https://github.com/user-attachments/assets/c87982eb-5b9d-4a93-9b91-7488d8a9889a" />

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
