import os
from dotenv import load_dotenv
from llm_calling import llm_or_rag, multiple_query_generator, hyde


while True:
    query = input(" > ")
    if query == "exit":
        break
    response = llm_or_rag(query=query)
    print(response)

    # if response == 'USE_RAG':
        # response = multiple_query_generator(query)
        # print(response)

    hyde_response = hyde(query)
    print(hyde_response)