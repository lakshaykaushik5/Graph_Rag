import os
from dotenv import load_dotenv
from prompts import choose_rag_or_not_system_prompt, multiple_query_system_prompt, hyde_system_prompt
from tools import tavily_search
import json


load_dotenv()


def llm_or_rag(query):
    try:
        client = llm_client("gemini")
        messages = [
            {"role": "system", "content": choose_rag_or_not_system_prompt},
            {"role": "user", "content": query}
        ]
        response = client.chat.completions.create(
            model = "",
            response_format = {'type':'json_object'},
            messages = messages
        )

        parsed_output = json.loads(response.choices[0].messages.content)

        return parsed_output

    except Exception as err:
        print(f"Error in llm_or_rag() :::: {err}")
        return "Error"


def multiple_query_generator(query):
    try:
        client = llm_client("gemini")
        messages = [
            {'role':'system','content':multiple_query_system_prompt},
            {'role':'user','content':'query'}
        ]
        response = client.chat.completeions.create(
            model='',
            response_format={'type':'json_object'},
            messages=messages
        )
        parsed_output = json.loads(response.choices[0].messages.content)
        return parsed_output
    except Exception as err:
        print(f"Error in multiple_query_generator() :::: {err}")
        return []


def hyde(query):
    try:
        client = llm_client('gemini')
        messages = [
            {'role':'system','content':hyde_system_prompt},
            {'role':'user','content':query}
        ]
        tools = [{
            'type':'function',
            'name':'tavily_search',
            'description':'Search the query on Internet and return results',
            'parameters':{
                'type':'object',
                'properties':{
                    'query':{'type':'string'}
                },
                'required':'query'
            },
            'strict':True
        }]

        search_result = tavily_search(query)

        messages.append({'role':'system','content':search_result})

        while True:
            response = client.chat.completeions.create(
                model = '',
                response_format= {'type':'json_object'},
                messages = messages,
                tools = tools
            )
        




        parsed_output = json.laods(response.choices[0].messages.content)
        
        return parsed_output 

    except Exception as err:
        print(f"Error in the hyde() :::: {err}")
        return "Error"


    