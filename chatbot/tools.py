from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()


def tavily_search(query):
    try:
        tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
        print(type(query))
        response = tavily_client.search(query,max_result = 5)
        final_response = '\n---\n'.join(
            result.get('content', '') for result in response.get('results', [])
        )

        return final_response or "No content found."



        return final_response
    except Exception as err:
        print(f"Error in tavily_search() :::: {err}")
        return "Error"