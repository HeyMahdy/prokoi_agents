from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request # Import Request
from langchain.chat_models import init_chat_model # Import the helper
from app.graph import app_graph
from app.tools import tools
from app.middleware import TokenMiddleware
from langchain_core.messages import HumanMessage
from app.state import AgentState
from app.tasks import run_agent_task
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize the model ONCE at startup
    # model_provider="openai" requires langchain-openai installed
    print("Initializing LLM...")    
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
    token = request.scope["state"].get("token", "")

    task = run_agent_task.delay(project_id, data.input, token)

    return {"task_id": task.id}

@app.get("/task/{task_id}")
def task_status(task_id: str):
    from app.worker import celery_app
    result = celery_app.AsyncResult(task_id)

    if result.state == "PENDING":
        return {"status": "pending"}

    if result.state == "SUCCESS":
        return {"status": "completed", "response": result.result}

    if result.state == "FAILURE":
        return {"status": "failed", "error": str(result.result)}

    return {"status": result.state}
    