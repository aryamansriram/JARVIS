import json
import httpx
from livekit.agents import llm
import logging
from typing import Annotated
from enum import Enum

import os

logger = logging.getLogger("my-worker")
logger.setLevel(logging.INFO)


class Rooms(Enum):
    """ Enum of the rooms whose light status can be queried """

    LIVING_ROOM = "LIVING_ROOM"
    BEDROOM = "BEDROOM"
    KITCHEN = "KITCHEN"


class WebFunctions(llm.FunctionContext):
    """
    This class consists of all functions
    that can be called by the created agent
    """

    def __init__(self):
        super().__init__()

    @llm.ai_callable(
        name='return_stock_data',
        description='Returns the stock price data for a given stock symbol',
    )
    async def return_stock_data(self, stock_symbol: Annotated[str, llm.TypeInfo(description="Stock symbol of the companyto retrieve data for")]):
        logger.info(f"Getting stock data for {stock_symbol}")

        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        url = 'https://www.alphavantage.co/query'

        

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={'function': 'TIME_SERIES_DAILY', 'symbol': stock_symbol, 'apikey': api_key})
            
            data = response.json()
            logger.info('Response: '+str(data))
    
        logger.info(f'Data for {stock_symbol} is {data["Time Series (Daily)"][list(data["Time Series (Daily)"].keys())[0]]}')
        return json.dumps(data['Time Series (Daily)'])
