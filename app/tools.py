# from langchain_core.tools import tool

# def create_retriever_tool(retriever):
#     @tool(response_format="content_and_artifact")
#     def retrieve_documents(query: str):
#         """Retrieve relevant documents."""
#         docs = retriever.invoke(query)
#         serialized = "\n\n".join(
#             f"Source: {doc.metadata}\nContent: {doc.page_content}"
#             for doc in docs
#         )
#         return serialized, docs

#     return [retrieve_documents]


from langchain_openai import OpenAIEmbeddings
from supabase import create_client
from langchain.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
embeddings = OpenAIEmbeddings()

def create_retriever_tool():
    @tool(response_format="content_and_artifact")
    def retrieve_documents(query: str):
        """Retrieve relevant documents from Supabase."""
        query_embedding = embeddings.embed_query(query)
        print("I am in the tool...")
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": 3
            }
        ).execute()

        if not response.data:
            return "No matching documents found.", []

        print("Got some data...")
        docs = []
        for doc in response.data:
            docs.append({
                "page_content": doc["content"],
                "metadata": doc["metadata"],
                "similarity": doc["similarity"]
            })

        serialized = "\n\n".join(
            f"Similarity: {d['similarity']:.3f}\nSource: {d['metadata']}\nContent: {d['page_content']}"
            for d in docs
        )
        return serialized, docs

    return [retrieve_documents]
