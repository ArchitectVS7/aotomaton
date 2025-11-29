"""LangGraph workflow graph construction."""

from langgraph.graph import StateGraph, END
from .state import ThursianState
from .nodes import (
    task_selection_node,
    assignment_node,
    execution_node,
    validation_node,
    completion_node
)
from .routing import route_after_execution, route_after_validation


def create_thursian_workflow() -> StateGraph:
    """Create and compile the Thursian orchestrator workflow graph."""

    workflow = StateGraph(ThursianState)

    # Add all nodes
    workflow.add_node("task_selection", task_selection_node)
    workflow.add_node("assignment", assignment_node)
    workflow.add_node("execution_node", execution_node)
    workflow.add_node("validation_node", validation_node)
    workflow.add_node("completion", completion_node)

    # Set entry point
    workflow.set_entry_point("task_selection")

    # Simple edges (deterministic flow)
    workflow.add_edge("task_selection", "assignment")
    workflow.add_edge("assignment", "execution_node")
    workflow.add_edge("completion", END)

    # Conditional edges (routing based on state)
    workflow.add_conditional_edges(
        "execution_node",
        route_after_execution,
        {
            "execution_node": "execution_node",  # Loop back
            "validation_node": "validation_node"  # Proceed
        }
    )

    workflow.add_conditional_edges(
        "validation_node",
        route_after_validation,
        {
            "validation_node": "validation_node",  # Loop back
            "completion": "completion",            # Approved
            "execution_node": "execution_node"     # Needs revision
        }
    )

    return workflow.compile()
