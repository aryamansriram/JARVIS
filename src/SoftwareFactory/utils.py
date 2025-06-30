"""
This module provides utility functions for the software factory.
"""

from typing import Annotated
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt.chat_agent_executor import AgentState


def create_handoff_tool(next_node: str, task_description: str = ""):
    if task_description == "":
        task_description = "Seek help from {}".format(next_node)

    @tool("transfer_to_{}".format(next_node), description=task_description)
    def handoff_tool(
        tool_call_id: Annotated[str, InjectedToolCallId],
        state: Annotated[AgentState, InjectedState],
    ):
        tool_message = {
            "role": "tool",
            "content": "Successfully transferred to {}".format(next_node),
            "name": next_node,
            "tool_call_id": tool_call_id,
        }

        return Command(
            goto=next_node,
            update={
                **state,
                "messages": state["messages"] + [ToolMessage(**tool_message)],
            },
            graph=Command.PARENT,
        )

    return handoff_tool
