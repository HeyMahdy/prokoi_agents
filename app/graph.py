from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from app.state import AgentState
from app.nodes import IssueAgent , tool_node


# 1. Initialize the Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
# 'agent' node calls the LLM
workflow.add_node("IssueAgent", IssueAgent)
# 'tools' node executes the tools (LangGraph provides a prebuilt node for this)
workflow.add_node("tool_node", tool_node)

# 3. Define Edges
workflow.set_entry_point("IssueAgent")

def should_continue_03(state):
    """this is for db agent."""
    last_message = state["messages"][-1]
    if not last_message.tool_calls:
        return "END"
    else :
        return "continue"



workflow.add_conditional_edges(
    "IssueAgent",
    should_continue_03,{
        "END":END,
        "continue":"tool_node"
    }
)


workflow.add_edge("tool_node", "IssueAgent")



app_graph = workflow.compile()