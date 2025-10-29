from app.data.destinations import DESTINATIONS


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
        "num_days": num_days,
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
