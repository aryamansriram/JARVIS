"""
This module defines the state representations for the company and agents.

Classes:
- CompanyState: Represents the state of the company with project requirements, plan, tools, and agent details.
- AgentState: Represents the state of an agent with messages.
"""

from typing import Annotated, TypedDict

from langgraph.graph import add_messages


class CompanyState(TypedDict):
    project_requirements: str
    project_plan: str
    tools: list
    agent_prompt: str
    agent_messages: list


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
