"""
This module defines the state representations for the company and agents.

Classes:
- CompanyState: Represents the state of the company with project requirements, plan, tools, and agent details.
- AgentState: Represents the state of an agent with messages.
"""

from typing import Annotated, TypedDict

from langgraph.graph import add_messages
from langgraph.prebuilt.chat_agent_executor import AgentState


class CompanyState(AgentState):
    project_requirements: str


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
