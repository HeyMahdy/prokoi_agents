# app/tasks.py
from app.worker import celery_app
from app.graph import app_graph
from langchain_core.messages import HumanMessage
from app.state import AgentState
from langchain.chat_models import init_chat_model
from app.tools import tools
import os

# Initialize LLM within the task module to avoid circular imports
LLM = init_chat_model(
    "gpt-5.1",
    api_key=os.getenv("api_key")
).bind_tools(tools)

@celery_app.task(name="app.tasks.run_agent_task")
def run_agent_task(project_id: int, user_input: str, token: str):

    # Build initial state
    init_state: AgentState = {
        "messages": [HumanMessage(content=user_input)],
        "title": "",
        "description": "",
        "story_points": None,
        "status": "open",
        "priority": "medium",
        "project_id": project_id,
        "type_id": None,
        "token": token,
    }

    # Pass the LLM to LangGraph config
    config = {
        "configurable": {
            "thread_id": "3",
            "my_llm": LLM   # using the locally initialized LLM instance
        }
    }

    # Run agent inside Celery
    result = app_graph.invoke(init_state, config=config)

    return result["messages"][-1].content