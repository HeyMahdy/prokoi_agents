
from app.tools import tools,tools_by_name
from app.prompts import system_message
from app.state import AgentState
from langchain_core.messages import BaseMessage,ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model





def IssueAgent(state: AgentState,config: RunnableConfig):

    llm = config["configurable"]["my_llm"]

    model_react=system_message|llm

    response = model_react.invoke({"agent_scratchpad": state["messages"],"project_id":state["project_id"],"token":state["token"]})
    return {
        "messages": [response]
    }




def tool_node(state: AgentState):
    outputs = []
    
    for tool_call in state["messages"][-1].tool_calls:
        print("these are the agrs")
        print(tool_call["args"])
        tool_result = tools_by_name[tool_call["name"]].invoke(tool_call["args"])
        
        outputs.append(
            ToolMessage(
                content=str(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    
    return {
        "messages": outputs
    }


