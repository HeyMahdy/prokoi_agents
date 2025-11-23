from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage,ToolMessage
from typing import (Annotated,Sequence,TypedDict)
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]  
    title: str
    description: str
    story_points: int | None
    status: str
    priority: str
    project_id: int
    type_id: int | None
    token : str
                                 
