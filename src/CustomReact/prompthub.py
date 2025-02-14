reAct_prompt = """
Answer the following questions as best you can. You have access to the following tools:

web_search(search_term): Searches the web for the given term

Use the following format:

Question: the input question you must answer
Thought: Think about what needs to be done
Action: the action to take, should be one of [web_search]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {question}
{agent_scratchpad}

"""