import os
import json
from anthropic import Anthropic
from app.destinations import validate_destination, calculate_trip_budget
import re


def setup_claude():
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: No API key found!")
        print("Make sure ANTHROPIC_API_KEY is in your .env file")
        return None

    client = Anthropic(api_key=api_key)
    model = os.getenv("ANTHROPIC_MODEL")

    print(f"Connected to Claude: {model}")
    return client, model


def ask_claude_to_extract(client, model, user_message):
    system_prompt = """You are a travel assistant. Extract information from travel requests.
Return ONLY a JSON object like this:
{
  "destination": "Paris",
  "duration": "5 days",
  "budget": "budget",
  "interests": ["culture", "food"]
}

If something is missing, use null."""

    user_prompt = f'Extract travel info from: "{user_message}"'

    print(f"\nSending to Claude...")
    print(f"User said: {user_message}")

    response = client.messages.create(
        model=model,
        max_tokens=500,
        temperature=0.3,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    response_text = response.content[0].text

    print(f"Claude responded!")
    return response_text


def parse_json_response(response_text):
    try:
        start = response_text.find("{")
        end = response_text.rfind("}") + 1

        if start == -1 or end == 0:
            print("Warning: No JSON found in response")
            return {}

        json_text = response_text[start:end]
        data = json.loads(json_text)

        print("\nExtracted data:")
        print(f"  Destination: {data.get('destination', 'Not found')}")
        print(f"  Duration: {data.get('duration', 'Not found')}")
        print(f"  Budget: {data.get('budget', 'Not found')}")
        print(f"  Interests: {data.get('interests', [])}")

        return data

    except json.JSONDecodeError as e:
        print(f"Error: Could not parse JSON: {e}")
        print(f"Response was: {response_text[:100]}...")
        return {}


def check_destination(extracted_data):
    destination_name = extracted_data.get("destination")

    if not destination_name:
        print("  No destination specified")
        extracted_data["validation"] = {
            "is_valid": False,
            "error": "No destination provided",
        }
        return extracted_data

    is_valid, result = validate_destination(destination_name)

    if is_valid:
        print(f"  Found: {result['name']}")
        print(f"  Average budget: ${result['avg_daily_budget']}/day")
        print(f"  Best time: {', '.join(result['best_months'][:3])}")

        extracted_data["validation"] = {"is_valid": True, "destination_info": result}

        duration = extracted_data.get("duration")
        if duration:
            days_match = re.search(r"(\d+)", duration)
            if days_match:
                num_days = int(days_match.group(1))
                budget_level = extracted_data.get("budget") or "mid-range"

                budget_calc = calculate_trip_budget(
                    destination_name, num_days, budget_level
                )

                if budget_calc:
                    print(f"  Estimated total: ${budget_calc['total']}")
                    extracted_data["estimated_budget"] = budget_calc

    else:
        print(f"  {result}")
        extracted_data["validation"] = {"is_valid": False, "error": result}

    return extracted_data


def extract_travel_intent(user_message):
    setup_result = setup_claude()
    if not setup_result:
        return {"error": "Could not connect to Claude"}

    client, model = setup_result

    try:
        response_text = ask_claude_to_extract(client, model, user_message)
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return {"error": str(e)}

    extracted_data = parse_json_response(response_text)

    validated_data = check_destination(extracted_data)

    print("=" * 60)

    return validated_data


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    test_messages = [
        "I want a 5-day cultural trip to Paris on a budget",
        "Planning a romantic week in Tokyo with food and culture",
        "Family vacation to Bali, love beaches and adventure",
    ]

    for message in test_messages:
        result = extract_travel_intent(message)
        print(f"\n{'='*60}\n")
        input("Press Enter to continue to next test...\n")
