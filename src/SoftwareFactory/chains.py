"""
This module provides functions to create agents and chains for coding and planning.

Functions:
- get_coder_agent: Creates a coding agent using the specified language model and tools.
- get_planner_chain: Creates a planning chain using the specified language model.
"""

from langgraph.prebuilt import create_react_agent
from langchain.prompts import PromptTemplate
from prompthub import (
    DEVELOPER_PROMPT,
    DUMMY_TESTER,
    PLANNER_PROMPT,
    SUPERVISOR_PROMPT,
    TEST_GENERATOR_PROMPT,
    TEST_REPORTER_PROMPT,
)
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from factory_tools import (
    create_directory,
    delete_directory,
    list_files_in_directory,
    create_file_with_code,
    read_file,
    delete_file,
    run_terminal_command,
)
from factory_tools import developer_handoff_tool, tester_handoff_tool


DEV_TOOLS = [
    create_directory,
    delete_directory,
    list_files_in_directory,
    create_file_with_code,
    read_file,
    delete_file,
]
TESTER_TOOLS = DEV_TOOLS.copy() + [
    run_terminal_command,
]
TEST_REPORTER_TOOLS = TESTER_TOOLS.copy() + [tester_handoff_tool]

SUPERVISOR_TOOLS = [developer_handoff_tool]


def get_coder_agent(llm, tools=DEV_TOOLS):
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
        prompt=DEVELOPER_PROMPT,
    )
    return coder_agent


def get_tester_agent(llm, project_requirements, tools=TESTER_TOOLS):
    """
    Creates a testing agent using the specified language model and tools.

    Parameters:
    - llm: The language model to be used.
    - tools: A list of tools available to the agent.
    - project_requirements: The requirements for the project.

    Returns:
    A testing agent configured with the given parameters.
    """
    tester_agent = create_react_agent(
        llm,
        tools=tools,
        prompt=DUMMY_TESTER.format(project_requirements=project_requirements),
    )
    return tester_agent


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


def get_supervisor_agent(llm, tools=SUPERVISOR_TOOLS):
    supervisor_agent = create_react_agent(
        llm, tools=tools, prompt=SUPERVISOR_PROMPT, debug=False, name="supervisor_agent"
    )
    return supervisor_agent


def get_test_generator_agent(llm, tools=TESTER_TOOLS):
    tester_agent = create_react_agent(
        llm,
        tools=tools,
        prompt=TEST_GENERATOR_PROMPT,
    )
    return tester_agent


def get_test_reporter_agent(llm, tools=TESTER_TOOLS):
    tester_agent = create_react_agent(
        llm,
        tools=tools,
        prompt=TEST_REPORTER_PROMPT,
    )
    return tester_agent
