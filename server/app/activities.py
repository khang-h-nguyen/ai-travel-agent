import json
from app.data.activities import ACTIVITIES


def get_activities_for_destination(destination_name, interests=None, limit=10, client=None, model=None):
    dest_key = destination_name.lower().strip()

    if dest_key not in ACTIVITIES:
        return []

    city_activities = ACTIVITIES[dest_key]
    suggestions = []

    if interests and len(interests) > 0:
        # Try exact matching first
        matched_categories = []
        for interest in interests:
            interest_key = interest.lower()
            if interest_key in city_activities:
                matched_categories.append(interest_key)
                suggestions.extend(city_activities[interest_key])

        # If no exact match, ask Claude to map interests to categories
        if not matched_categories and client and model:
            print(f"   No exact match for {interests}, using semantic matching...")

            available_categories = list(city_activities.keys())

            system_prompt = """You are a travel expert. Map user interests to activity categories.
Return ONLY a JSON array of category names.

Example:
User interests: ["beaches", "adventure"]
Available categories: ["nature", "culture", "food", "outdoor"]
Response: ["nature", "outdoor"]"""

            user_prompt = f"""User interests: {interests}
Available categories for {destination_name}: {available_categories}

Map interests to matching categories. Return only a JSON array."""

            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=200,
                    temperature=0.2,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )

                response_text = response.content[0].text

                # Extract JSON array from response
                start = response_text.find("[")
                end = response_text.rfind("]") + 1

                if start != -1 and end > 0:
                    json_text = response_text[start:end]
                    semantic_categories = json.loads(json_text)

                    valid_categories = [c for c in semantic_categories if c in available_categories]

                    if valid_categories:
                        print(f"   Mapped to categories: {valid_categories}")
                        for category in valid_categories:
                            suggestions.extend(city_activities[category])

            except Exception as e:
                print(f"   Error mapping interests: {e}")
    else:
        # No interests specified - return a mix from all categories
        for category_activities in city_activities.values():
            suggestions.extend(category_activities[:2])

    # Remove duplicates and limit results
    unique_suggestions = list(dict.fromkeys(suggestions))
    return unique_suggestions[:limit]
