import os
from dotenv import load_dotenv
from prompts import choose_rag_or_not_system_prompt, multiple_query_system_prompt, hyde_system_prompt, collection_routing_prompt
from tools import tavily_search
from vector_db import get_data
from config import CHAT_MODEL
from llm_models import llm_client
import json


load_dotenv()


def llm_or_rag(query): # DONE TESTING
    try:
        client = llm_client("gemini")
        messages = [
            {"role": "system", "content": choose_rag_or_not_system_prompt},
            {"role": "user", "content": query}
        ]
        response = client.chat.completions.create(
            model = CHAT_MODEL,
            response_format = {'type':'json_object'},
            messages = messages
        )

        parsed_output = json.loads(response.choices[0].message.content)

        return parsed_output

    except Exception as err:
        print(f"Error in llm_or_rag() :::: {err}")
        return "Error"


def multiple_query_generator(query):
    try:
        client = llm_client("gemini")
        messages = [
            {'role':'system','content':multiple_query_system_prompt},
            {'role':'user','content':query}
        ]
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            response_format={'type':'json_object'},
            messages=messages
        )
        parsed_output = json.loads(response.choices[0].message.content)
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
        "type": "function",
        "function": {
            "name": "tavily_search",
            "description": "Search the query on Internet and return results",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": { "type": "string" }
                },
                "required": ["query"]
            }
        }
        }]

        response = client.chat.completions.create(
            model = CHAT_MODEL,
            # response_format= {'type':'json_object'},
            messages = messages,
            tools = tools,
            tool_choice="auto"
        )
        


        tool_call = response.choices[0].message.tool_calls[0] if response.choices[0].message.tool_calls else None


        print(tool_call)
        if tool_call:
            print
            fn_name = tool_call.function.name
            fn_args = tool_call.function.arguments
            print(fn_name,'\n\n\n',fn_args,'\n\n\n')
            if isinstance(fn_args, str):
                fn_args = json.loads(fn_args)  

            query_result = fn_args.get('query')
            if fn_name == "tavily_search":
                search_result = tavily_search(query_result)
                # print(type(search_result))
                # print('_'*100)
                messages.append({'role':'user','content':search_result})

                final_response = client.chat.completions.create(
                    model=CHAT_MODEL,
                    response_format={'type':'json_object'},
                    messages=messages
                )
                

                parsed_output = json.loads(final_response.choices[0].message.content)
                return  parsed_output.get('hypothetical_document')
        else:
            parsed_output = json.loads(response.choices[0].message.content)
            return parsed_output    


    except Exception as err:
        print(f"Error in the hyde() :::: {err}")
        return "Error"


def collections_to_search(query):
    try:
        messages = [
            {'role':'system','content':collection_routing_prompt},
            {'role':'user','content':query}
        ]
        client = llm_client('gemini')
        response = client.chat.completions.create(
            model="",
            response_format={'type':'json_object'},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].messages.content)
        vector_result = []
        for collection in parsed_output:
            collection_result = get_data(collection_name=query)
            vector_result.append(collection_result)
        
        return vector_result

    except Exception as err:
        print(f"Error in collection_to_search() :::: {err}")
        return []


def parallel_query_retreival(mulltiple_queries):
    try:
        vector_result = set()
        for query in mulltiple_queries:
            db_result = collections_to_search(query)
            for result in db_result:
                for chunks in result:
                    vector_result.add(chunks.page_content)
        

        seperator = '\n---\n'
        final_vector_result = seperator.join(vector_result)
        return final_vector_result
            

    except Exception as err:
        print(f"Error in parallel_query_retreival() :::: {err}")
        return "Error"


def reciprocate_rank_fusion(multiple_queries,k=60):
    try:
        scores = {}
        data_chunks = {}
        for query in multiple_queries:
            db_result = collections_to_search(qury)
            for result in db_result:
                for rank,chunks in enumerate(result):
                    doc_id = chunks.metadata['_id']
                    scores[doc_id] = scores.get(doc_id,0) + 1/(k+rank+1)
        
        sorted(scores.items(),key=lambda x:x[1],reverse=True)
        n = len(data_chunks)/2 + 1

        ranked_data = []

        for i,score in enumerate(scores):
            if i<=n:   
                ranked_data.append(data_chunks[score])


        final_ranked_data =  '\n---\n'.join(ranked_data)
        return final_ranked_data

        
    except Exception as err:
        print(f"Error in reciprocate_rank_fusion() :::: {err}")
        return "Error"