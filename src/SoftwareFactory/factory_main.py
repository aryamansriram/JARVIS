"""
This module contains the main logic for the software factory, including the creation of the company graph and the execution of nodes.

Classes:
- SoftwareFactory: Manages the lifecycle of the software factory, including planning and development nodes.
"""

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END
from factory_tools import (
    create_directory,
    delete_directory,
    create_file_with_code,
    read_file,
    delete_file,
)
from company_state import CompanyState
from langgraph.graph import StateGraph
from loguru import logger
from chains import get_planner_chain, get_coder_agent


class SoftwareFactory:
    """
    Represents the software factory managing the lifecycle of projects.

    Methods:
    - planner_node: Executes the planning node using the company state.
    - developer_node: Executes the developer node using the company state.
    - create_company_graph: Creates and compiles the company graph.
    """

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=16000)
        self.company_graph = self.create_company_graph()

    def planner_node(self, CompanyState):
        planner = get_planner_chain(self.llm)
        logger.info("Running planner")
        return {"project_plan": planner.invoke(CompanyState)}

    def developer_node(self, state: CompanyState):
        coder_agent = get_coder_agent(
            self.llm,
            state["tools"],
            state["project_requirements"],
            state["project_plan"],
        )
        return {"agent_messages": coder_agent.invoke(state)}

    def create_company_graph(self):
        graph = StateGraph(CompanyState)

        graph.add_node("planner", self.planner_node)
        graph.add_node("developer", self.developer_node)

        graph.add_edge(START, "planner")
        graph.add_edge("planner", "developer")
        graph.add_edge("developer", END)
        return graph.compile()


if __name__ == "__main__":
    dev_tools = [
        create_directory,
        delete_directory,
        create_file_with_code,
        read_file,
        delete_file,
    ]

    factory = SoftwareFactory()
    factory.company_graph.invoke(
        CompanyState(
            project_requirements="""
            Create a web application where the user can play tic-tac-toe
            The screen should have a 3x3 grid in the center of the page
            The users should be able to place Xs and Os on the grid using alternate mouse clicks
            This means if the current click to a box added an X to a box in the grid, the very next click should add a O to the box which is clicked
            The game always starts with X
            Keep track of the number of games won, by using a scoreboard on the top right corner of the screen
            The game should have a heading with the text "Tic Tac Toe" in the center of the page
            Whenever a game ends, There should be a success message displayed on the center of the page along with a confetti animation
            The game should also have a new game button to start a new game
            Make the UI beautiful following Material Design principles
            The backend code should be written in python using flask
            """,
            tools=dev_tools,
        )
    )
