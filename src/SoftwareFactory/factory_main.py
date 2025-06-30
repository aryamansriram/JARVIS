"""
This module contains the main logic for the software factory, including the creation of the company graph and the execution of nodes.

Classes:
- SoftwareFactory: Manages the lifecycle of the software factory, including planning and development nodes.
"""

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END
from langgraph.prebuilt.chat_agent_executor import AgentState
from factory_tools import (
    create_directory,
    delete_directory,
    list_files_in_directory,
    create_file_with_code,
    read_file,
    delete_file,
)
from langgraph.graph import StateGraph
from chains import get_coder_agent, get_supervisor_agent
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

    def supervisor_node(self, state: AgentState):
        supervisor_agent = get_supervisor_agent(self.llm)
        return {"messages": supervisor_agent.invoke(state)["messages"]}

    def developer_node(self, state: AgentState):
        coder_agent = get_coder_agent(self.llm)
        OUT = coder_agent.invoke(state)
        return {"messages": OUT["messages"]}

    def create_company_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node(
            "supervisor", self.supervisor_node, destinations=["developer", END]
        )
        graph.add_node("developer", self.developer_node)
        graph.add_edge(START, "supervisor")
        graph.add_edge("developer", "supervisor")

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
    for sg, chunk in factory.company_graph.stream(
        AgentState(
            messages=[
                HumanMessage(
                    content="""
            Create a python script that through terminal arguments
            takes three inputs: Two numbers and one of the following operations:
            1. Add
            2. Subtract
            3. Multiply
            4. Divide
            The script should perform the operation on the two numbers and print the result.
            The script should be written in python and should be named calculator.py
            """
                )
            ]
        ),
        config=RunnableConfig(recursion_limit=100),
        subgraphs=True,
    ):
        print("C: ", chunk)
        print("***************")

    # _, out_state = factory.company_graph.invoke(
    #     AgentState(
    #         messages=[
    #             HumanMessage(
    #                 content="""
    #         Create a python script that through terminal arguments
    #         takes three inputs: Two numbers and one of the following operations:
    #         1. Add
    #         2. Subtract
    #         3. Multiply
    #         4. Divide
    #         The script should perform the operation on the two numbers and print the result.
    #         The script should be written in python and should be named calculator.py
    #         """
    #             )
    #         ]
    #     ),
    #     config=RunnableConfig(recursion_limit=100),
    #     subgraphs=True,
    # )
    # pprint([message.content for message in out_state["messages"]])
