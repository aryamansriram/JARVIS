"""
This module provides functions to create agents and chains for coding and planning.

Functions:
- get_coder_agent: Creates a coding agent using the specified language model and tools.
- get_planner_chain: Creates a planning chain using the specified language model.
"""

from langgraph.prebuilt import create_react_agent
from langchain.prompts import PromptTemplate
from prompthub import DEVELOPER_PROMPT, PLANNER_PROMPT
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter


def get_coder_agent(llm, tools, project_requirements, project_plan):
    """
    Creates a coding agent using the specified language model and tools.

    Parameters:
    - llm: The language model to be used.
    - tools: A list of tools available to the agent.
    - project_requirements: The requirements for the project.
    - project_plan: The plan for the project.

    Returns:
    A coding agent configured with the given parameters.
    """
    coder_agent = create_react_agent(
        llm,
        tools=tools,
        prompt=DEVELOPER_PROMPT.format(
            project_requirements=project_requirements, project_plan=project_plan
        ),
    )
    return coder_agent


def get_planner_chain(llm):
    """
    Creates a planning chain using the specified language model.

    Parameters:
    - llm: The language model to be used.

    Returns:
    A planning chain configured with the given language model.
    """
    planner_prompt = PromptTemplate.from_template(PLANNER_PROMPT)
    planner_node = (
        {"project_requirements": itemgetter("project_requirements")}
        | planner_prompt
        | llm
        | StrOutputParser()
    )
    return planner_node
