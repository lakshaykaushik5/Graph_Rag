from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


def tavily_search(query):
    try:
        tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
        response = tavily_client.search(query,max_result = 5)

        #  ----tools-----

        return response
    except Exception as err:
        print(f"Error in tavily_search() :::: {err}")
        return "Error"