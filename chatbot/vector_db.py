from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from dotenv import load_dotenv
import os


load_dotenv()


client = QdrantClient(
    api_key = os.getenv('QDRANT_API_KEY'),
    url = os.getenv('QDRANT_URL')
)

def add_data(collection_name,chunks_data):
    try:
        
        check_collection_exist = client.collection_exist(collection_name=collection_name)

        if not check_collection_exist:
            client.create_collection(
                collection_name=collection_name,
                vector_config = VectorParams(size=3072,distance = Distance.COSINE)
            )
        
        QdrantVectorStore.add_documents(
            documents = chunks_data,
            collection_name = collection_name,
            embedding = "",
            client = client
        )
        print(f'''{'-'*40}INJECTION-DONE{'-'*40}''')
        return "Success"

    except Exception as err:
        print(f"Error in add_data() :::: {err}")
        return "Error"


def get_data(collection_name,query):
    try:
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding="",
            retrieval_mode = RetrievalMode.DENSE
        )

        return vector_store.similarity_search(query)

        
        
    except Exception as err:
        print(f"Error in get_data() :::: {err}")
        return []