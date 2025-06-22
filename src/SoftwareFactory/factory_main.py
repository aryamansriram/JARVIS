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
    list_files_in_directory,
    create_file_with_code,
    read_file,
    delete_file,
)
from company_state import CompanyState
from langgraph.graph import StateGraph
from loguru import logger
from chains import get_planner_chain, get_coder_agent, get_tester_agent
from langchain_core.runnables.config import RunnableConfig


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

    def planner_node(self, state: CompanyState):
        planner = get_planner_chain(self.llm)
        logger.info("Running planner")
        print(state.keys())
        return {
            "project_plan": planner.invoke(state),
            "planner_counter": state["planner_counter"] + 1,
        }

    def developer_node(self, state: CompanyState):
        print("PLAN: ", state["project_plan"])

        coder_agent = get_coder_agent(
            self.llm,
            state["project_requirements"],
            state["project_plan"],
        )
        return {"agent_messages": coder_agent.invoke(state)}

    def tester_node(self, state: CompanyState):
        logger.info("Running tester")
        tester_agent = get_tester_agent(
            self.llm,
            state["project_requirements"],
        )
        return {
            "project_requirements": tester_agent.invoke(state)["messages"][-1].content
        }

    def create_company_graph(self):
        graph = StateGraph(CompanyState)

        graph.add_node("planner", self.planner_node)
        graph.add_node("developer", self.developer_node)
        graph.add_node("tester", self.tester_node)

        graph.add_edge(START, "planner")
        graph.add_conditional_edges(
            "planner",
            lambda x: "developer"
            if x["planner_counter"] <= 5 and x["project_plan"] != "__end__"
            else END,
        )
        graph.add_edge("planner", "developer")
        graph.add_edge("developer", "tester")
        graph.add_edge("tester", "planner")
        graph.add_edge("planner", END)

        return graph.compile()


if __name__ == "__main__":
    dev_tools = [
        create_directory,
        delete_directory,
        list_files_in_directory,
        create_file_with_code,
        read_file,
        delete_file,
    ]

    factory = SoftwareFactory()
    for subgraph, chunk in factory.company_graph.stream(
        CompanyState(
            project_requirements="""
            Create an api service in flask which allows users to talk to an LLM. 
            The api should have a single endpoint /chat that returns a chat response. Users can call this endpoint using curl or any http client.
            Users will also have the ability to send follow up messages to the api service to improve the chat experience 
            The application should maintain a conversation history with the user to improve the chat experience over time
            Write the api service in flask and langchain.
            Remember, do not create placeholder code, build the complete api service 
            Assume that all API keys are set up correctly in ~/.zshrc
            """,
            planner_counter=0,
        ),
        config=RunnableConfig(recursion_limit=100),
        subgraphs=True,
    ):
        print(chunk)
