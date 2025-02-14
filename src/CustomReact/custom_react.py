from operator import itemgetter
from langchain_core.prompts import PromptTemplate
from prompthub import *
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import OpenAI
from langchain_community.tools import BraveSearch,DuckDuckGoSearchResults 
import os
import re
from pprint import pprint
import ast
from langchain_core.tools import tool
from exa_py import Exa

def create_basic_chain():
    prompt = PromptTemplate.from_template(reAct_prompt)
    llm = OpenAI(name="gpt-4o-mini-2024-07-18",
    temperature=0,
    **{"stop":["Observation:","OBSERVATION:"]})
    chain = {
        'question': itemgetter('question'),
        'agent_scratchpad': itemgetter('agent_scratchpad'),
    } | prompt | llm | StrOutputParser()
    return chain

def web_search(search_term,tool):
    
    return tool.invoke(search_term)

def take_action(output):
    if re.search('(action input:.*)', output.lower()):
        action = re.search('(action input:.*)', output.lower()).group()
        
        return web_search(action.split(':')[1].strip(),exa_search)
    else:
        
        return None

@tool
def exa_search(query: str):
    """Search for webpages based on the query and retrieve their contents."""
    # This combines two API endpoints: search and contents retrieval
    print("Q: ", query)
    exa = Exa(
        api_key=os.environ["EXA_API_KEY"]
    )
    return exa.search_and_contents(
        query, use_autoprompt=True, num_results=3, text=True, highlights=True
    )



if __name__=="__main__":
    chain = create_basic_chain()
    scratchpad = ""
    end_flag = 0
    k=0
    while k<100:
        out = chain.invoke(
            {'question': 'What government position was held by the woman who portrayed Corliss Archer in the film Kiss and Tell?',
            'agent_scratchpad': scratchpad
            }
        )
        print("Out{}: ".format(k), out)
        if re.search('(final answer:.*)', out.lower()):
            out = re.search('(final answer:.*)', out.lower()).group()
            end_flag = 1
            break
        
        print("####"*50)
        thought = out.lower().split('thought:')[1].strip()
        action = out.lower().split('action:')[1].strip()
        action_input = out.lower().split('action input:')[1].strip()
        
        observation = take_action(out)
        obs_list = []
        for obs in observation.results:
            obs_list.extend(obs.highlights)
        obs = '\n'.join(obs_list).replace('\n',' ')
        print("OBS: ",obs)
        scratchpad = scratchpad + f"""
        THOUGHT: {thought}
        ACTION: {action}
        ACTION INPUT: {action_input}
        OBSERVATION: {obs}\n
        """
        k+=1
        
    #print("Scratchpad: ", scratchpad)
    print(out)
    