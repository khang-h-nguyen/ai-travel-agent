import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import BaseCallbackHandler

from app.tools import (
    validate_destination_tool,
    get_weather_tool,
    get_activities_tool,
    calculate_budget_tool,
    parse_duration_from_text,
)


class StepTracker(BaseCallbackHandler):

    def __init__(self):
        self.steps = []

    def on_tool_start(self, tool, input_str, **kwargs):
        tool_name = tool.name if hasattr(tool, "name") else str(tool)

        self.steps.append(
            {"status": "in_progress", "message": f"Using {tool_name}", "data": {}}
        )

    def on_tool_end(self, output, **kwargs):
        if self.steps:
            self.steps[-1]["status"] = "completed"


def setup_claude():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL")

    if not api_key:
        print("Error: No API key found!")
        return None

    print(f"Connected to Claude: {model}")
    return api_key, model


async def extract_travel_intent(user_message):
    print(f"User said: {user_message}")

    setup_result = setup_claude()
    if not setup_result:
        return {"error": "Could not connect to Claude"}

    api_key, model_name = setup_result

    llm = ChatAnthropic(
        anthropic_api_key=api_key, model_name=model_name, temperature=0.3
    )

    tools = [
        validate_destination_tool,
        get_weather_tool,
        get_activities_tool,
        calculate_budget_tool,
    ]

    prompt_template = """You are a travel planning assistant for Canadian destinations.

Help users plan trips by using the available tools to:
1. Validate destination
2. Check weather if needed
3. Get activity recommendations
4. Calculate budget

Available destinations: Toronto, Vancouver, Montreal, Quebec City, Banff, Victoria, Ottawa, Calgary, Niagara Falls, Whistler

You have access to these tools:

{tools}

Use this format:

Question: {input}
Thought: think about what to do
Action: tool to use, must be one of [{tool_names}]
Action Input: input for the tool
Observation: result from tool
... (repeat Thought/Action/Observation as needed)
Thought: I have enough information now
Final Answer: complete response to user

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(prompt_template)
    agent = create_react_agent(llm, tools, prompt)

    tracker = StepTracker()

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, callbacks=[tracker], verbose=True, max_iterations=10
    )

    try:
        duration = parse_duration_from_text(user_message)
        if duration:
            user_message = f"{user_message} (Duration: {duration} days)"

        result = await agent_executor.ainvoke({"input": user_message})

        return {"response": result.get("output", ""), "steps": tracker.steps}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e), "steps": tracker.steps}
