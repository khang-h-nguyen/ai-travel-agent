DESTINATIONS = {
    "toronto": {
        "name": "Toronto, Ontario",
        "province": "Ontario",
        "avg_daily_budget": 150,  # CAD per day
        "currency": "CAD",
        "timezone": "EST",
        "best_months": ["May", "June", "July", "August", "September"],
        "popular_for": ["culture", "food", "nightlife", "shopping", "diversity"],
        "description": "Canada's largest city with diverse neighborhoods, world-class dining, and vibrant culture",
        "highlights": ["CN Tower", "Royal Ontario Museum", "St. Lawrence Market", "Distillery District"]
    },
    
    "vancouver": {
        "name": "Vancouver, British Columbia",
        "province": "British Columbia",
        "avg_daily_budget": 160,
        "currency": "CAD",
        "timezone": "PST",
        "best_months": ["April", "May", "June", "July", "August", "September"],
        "popular_for": ["nature", "outdoor", "food", "beaches", "mountains"],
        "description": "Stunning coastal city surrounded by mountains and ocean, perfect for outdoor enthusiasts",
        "highlights": ["Stanley Park", "Granville Island", "Capilano Suspension Bridge", "Grouse Mountain"]
    },
    
    "montreal": {
        "name": "Montreal, Quebec",
        "province": "Quebec",
        "avg_daily_budget": 130,
        "currency": "CAD",
        "timezone": "EST",
        "best_months": ["May", "June", "July", "August", "September", "October"],
        "popular_for": ["culture", "food", "history", "festivals", "nightlife"],
        "description": "Bilingual city with European charm, renowned for festivals, food, and joie de vivre",
        "highlights": ["Old Montreal", "Mont Royal", "Notre-Dame Basilica", "Jean-Talon Market"]
    },
    
    "quebec city": {
        "name": "Quebec City, Quebec",
        "province": "Quebec",
        "avg_daily_budget": 120,
        "currency": "CAD",
        "timezone": "EST",
        "best_months": ["May", "June", "July", "August", "September", "December"],
        "popular_for": ["history", "culture", "romance", "architecture", "winter"],
        "description": "Only walled city in North America, European atmosphere with cobblestone streets",
        "highlights": ["Old Quebec", "Château Frontenac", "Montmorency Falls", "Plains of Abraham"]
    },
    
    "banff": {
        "name": "Banff, Alberta",
        "province": "Alberta",
        "avg_daily_budget": 140,
        "currency": "CAD",
        "timezone": "MST",
        "best_months": ["June", "July", "August", "December", "January", "February"],
        "popular_for": ["nature", "outdoor", "skiing", "hiking", "wildlife"],
        "description": "Mountain resort town in the heart of the Canadian Rockies with stunning scenery",
        "highlights": ["Lake Louise", "Moraine Lake", "Banff Gondola", "Hot Springs", "Skiing"]
    },
    
    "victoria": {
        "name": "Victoria, British Columbia",
        "province": "British Columbia",
        "avg_daily_budget": 140,
        "currency": "CAD",
        "timezone": "PST",
        "best_months": ["April", "May", "June", "July", "August", "September"],
        "popular_for": ["gardens", "history", "relaxation", "culture", "nature"],
        "description": "Charming capital of BC with British influence, beautiful gardens, and mild climate",
        "highlights": ["Butchart Gardens", "Inner Harbour", "Royal BC Museum", "Whale watching"]
    },
    
    "ottawa": {
        "name": "Ottawa, Ontario",
        "province": "Ontario",
        "avg_daily_budget": 130,
        "currency": "CAD",
        "timezone": "EST",
        "best_months": ["May", "June", "July", "August", "September", "February"],
        "popular_for": ["history", "culture", "politics", "museums", "winter"],
        "description": "Canada's capital with national museums, Parliament Hill, and Rideau Canal skating in winter",
        "highlights": ["Parliament Hill", "ByWard Market", "National Gallery", "Rideau Canal"]
    },
    
    "calgary": {
        "name": "Calgary, Alberta",
        "province": "Alberta",
        "avg_daily_budget": 135,
        "currency": "CAD",
        "timezone": "MST",
        "best_months": ["June", "July", "August", "September"],
        "popular_for": ["outdoor", "culture", "western", "festivals", "gateway"],
        "description": "Modern city near the Rockies, famous for Calgary Stampede and Western culture",
        "highlights": ["Calgary Stampede", "Heritage Park", "Calgary Tower", "Gateway to Rockies"]
    },
    
    "niagara falls": {
        "name": "Niagara Falls, Ontario",
        "province": "Ontario",
        "avg_daily_budget": 120,
        "currency": "CAD",
        "timezone": "EST",
        "best_months": ["May", "June", "July", "August", "September"],
        "popular_for": ["nature", "adventure", "romance", "family", "iconic"],
        "description": "World-famous waterfalls, one of Canada's most iconic natural wonders",
        "highlights": ["Horseshoe Falls", "Journey Behind the Falls", "Niagara-on-the-Lake", "Wineries"]
    },
    
    "whistler": {
        "name": "Whistler, British Columbia",
        "province": "British Columbia",
        "avg_daily_budget": 170,
        "currency": "CAD",
        "timezone": "PST",
        "best_months": ["December", "January", "February", "June", "July", "August"],
        "popular_for": ["skiing", "outdoor", "adventure", "luxury", "mountains"],
        "description": "World-class ski resort and year-round mountain destination",
        "highlights": ["Whistler Blackcomb", "Peak 2 Peak Gondola", "Village", "Mountain biking"]
    }
}

def find_destination(destination_name):
    if not destination_name:
        return None

    search_term = destination_name.lower().strip()

    if search_term in DESTINATIONS:
        return DESTINATIONS[search_term]

    for key, dest_info in DESTINATIONS.items():
        if search_term in key or search_term in dest_info["name"].lower():
            return dest_info

    return None


def calculate_trip_budget(destination_name, num_days, budget_level="mid-range"):
    dest = find_destination(destination_name)
    if not dest:
        return None

    daily = dest["avg_daily_budget"]
    total = daily * num_days

    return {
        "daily_budget": daily,
        "total": round(total, 2),
        "currency": "CAD"
    }


def validate_destination(destination_name):
    dest = find_destination(destination_name)

    if dest:
        return True, dest
    else:
        error_msg = f"Sorry, we don't have info for {destination_name} yet. Try another Canadian destination."
        return False, error_msg


if __name__ == "__main__":
    print("=" * 60)
    print("CANADIAN DESTINATIONS TEST")
    print("=" * 60)

    print("\n1. Finding Toronto...")
    dest = find_destination("toronto")
    if dest:
        print(f"   Found: {dest['name']}")
        print(f"   Budget: ${dest['avg_daily_budget']}/day CAD")
        print(f"   Best months: {', '.join(dest['best_months'][:3])}")

    print("\n2. Calculating 5-day trip to Vancouver...")
    budget = calculate_trip_budget("vancouver", 5, "mid-range")
    if budget:
        print(f"   Total: ${budget['total']} CAD")
        print(f"   Daily: ${budget['daily_budget']}/day CAD")

    print("\n3. Validating destinations...")
    is_valid, result = validate_destination("montreal")
    print(f"   Montreal: {'Valid' if is_valid else 'Invalid'}")

    is_valid, result = validate_destination("new york")
    print(f"   New York: {'Valid' if is_valid else 'Invalid'}")
    if not is_valid:
        print(f"   Note: {result}")
    