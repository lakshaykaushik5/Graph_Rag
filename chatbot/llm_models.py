import os
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


def llm_client(model_provider):
    try:
        base_url = NONE
        api_key = NONE
        if model_provider == "gemini":
            base_url = os.getenv('')
            api_key = os.getenv('')
        elif model_provider == "groq":
            base_url = os.getenv('')
            api_key = os.getenv('')
        elif model_provider == "openai":
            base_url = os.getenv('')
            api_key = os.getenv('')
        else:
            return "Invalid model provided"

        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        return client

    except Exception as err:
        print(f"Error in llm_client() :::: ",{err})
        return "failed"