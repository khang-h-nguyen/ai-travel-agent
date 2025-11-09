import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

from app.tools import (
    validate_destination_tool,
    get_weather_tool,
    get_activities_tool,
    calculate_budget_tool,
    parse_duration_from_text,
)
from app.session_store import create_session, get_session_messages, add_message

AGENT_PROMPT = """You are a travel planning assistant for Canadian destinations.

Help users plan trips by:
1. ALWAYS validate the destination first
2. Check current weather (helps recommend appropriate activities)
3. Get activity recommendations based on interests AND weather
4. Calculate budget

IMPORTANT: Always check weather before recommending activities, so you can suggest 
indoor options if it's raining or winter activities if it's snowing.

Available destinations: Toronto, Vancouver, Montreal, Quebec City, Banff, Victoria, Ottawa, Calgary, Niagara Falls, Whistler

Be helpful and concise."""


def setup_claude():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL")

    if not api_key:
        print("Error: No API key found!")
        return None

    return api_key, model


async def extract_travel_intent(user_message, session_id=None):
    setup_result = setup_claude()
    if not setup_result:
        return {"error": "Could not connect to LLM"}

    api_key, model_name = setup_result

    llm = ChatAnthropic(
        anthropic_api_key=api_key, model_name=model_name, temperature=0.5
    )

    tools = [
        validate_destination_tool,
        get_weather_tool,
        get_activities_tool,
        calculate_budget_tool,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", AGENT_PROMPT),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, max_iterations=10
    )

    # Session management
    if not session_id:
        session_id = create_session()

    try:
        duration = parse_duration_from_text(user_message)
        if duration:
            user_message = f"{user_message} (Duration: {duration} days)"
        add_message(session_id, HumanMessage(content=user_message))
    
        chat_history = get_session_messages(session_id)
        if len(chat_history) == 0:
            # Session expired or invalid, create new one
            session_id = create_session()

        result = await agent_executor.ainvoke(
            {
                "input": user_message,
                "chat_history": chat_history
            }
        )

        output = result.get("output", "")
        if isinstance(output, list):
            text_parts = []
            for item in output:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        text_parts.append(item.get("text", ""))
            output = "\n\n".join(text_parts)

        if not isinstance(output, str):
            output = str(output)

        # Save conversation to chat history
        add_message(session_id, AIMessage(content=output))

        return {"response": output, "session_id": session_id}

    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
