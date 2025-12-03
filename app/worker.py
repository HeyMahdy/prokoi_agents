# app/worker.py
from celery import Celery
import os
from langchain.chat_models import init_chat_model   
from app.tools import tools  
from dotenv import load_dotenv
load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

celery_app = Celery(
    "agent_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)
celery_app.autodiscover_tasks(['app'], force=True)


celery_app.conf.task_routes = {"app.tasks.*": {"queue": "agent_queue"}}
