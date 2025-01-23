from typing import List
from AgentFunctions.home_functions import HomeFunctions
from AgentFunctions.web_functions import WebFunctions
from livekit.agents import llm


class Functions(HomeFunctions, WebFunctions):
    def __init__(self):
        super().__init__()