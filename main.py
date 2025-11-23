from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request # Import Request
from langchain.chat_models import init_chat_model # Import the helper
from app.graph import app_graph
from app.tools import tools
from app.middleware import TokenMiddleware
from langchain_core.messages import HumanMessage
from app.state import AgentState
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize the model ONCE at startup
    # model_provider="openai" requires langchain-openai installed
    print("Initializing LLM...")
    llm = init_chat_model("gpt-5.1", api_key=os.getenv("api_key"))
    
    
    app.state.llm = llm.bind_tools(tools)
    
    yield

    print("Shutting down...")

app = FastAPI(title="Agent API", lifespan=lifespan)
app.add_middleware(TokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

from pydantic import BaseModel

class ChatInput(BaseModel):
    input: str
@app.post("/chat")
async def chat_endpoint(project_id: int, data: ChatInput, request: Request):
    llm = request.app.state.llm

    # get token from ASGI scope
    token = request.scope["state"].get("token", "")
    print("this is the token")
    print(token)

    # LangGraph config
    config = {
        "configurable": {
            "thread_id": "3",
            "my_llm": llm
        }
    }

    # init state for agent run
    init_state: AgentState = {
        "messages": [HumanMessage(content=data.input)],
        "title": "",
        "description": "",
        "story_points": None,
        "status": "open",
        "priority": "medium",
        "project_id": project_id,
        "type_id": None,
        "token": token
    }

    # run agent once and get final output
    result = await app_graph.ainvoke(init_state, config=config)

    # extract assistant output message
    response_msg = result["messages"][-1].content

    return {"response": response_msg}

    