# Import relevant functionality
from langchain_openai import ChatOpenAI
from langchain_community.tools import BraveSearch 
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.output_parsers import StrOutputParser
import os

# Create the agent
memory = MemorySaver()
model = ChatOpenAI(name='gpt-4o-mini-2024-07-18', temperature=0)
web_search = BraveSearch.from_api_key(
        api_key = os.environ["BRAVE_API_KEY"],
        search_kwargs = {'count': 3}
    )
tools = [web_search]
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
):
    
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats the weather where I live?")]}, config
):
    print(chunk)
    print("----")