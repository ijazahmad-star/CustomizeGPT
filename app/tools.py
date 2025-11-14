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

from sentence_transformers import CrossEncoder
from dotenv import load_dotenv
load_dotenv()


# load cross-encoder
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Helper function to rerank the results
def rerank_with_cross_encoder(query, docs):
    print("Re-Ranking the results...")
    pairs = [(query, d["page_content"]) for d in docs]
    scores = cross_encoder.predict(pairs)
    ranked = [
        {**doc, "rerank_score": float(score)}
        for doc, score in zip(docs, scores)
    ]
    ranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return ranked

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
        print("I am in the tool...") # just to check the agent uses this tool or not
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": 3
            }
        ).execute()

        if not response.data:
            return "No matching documents found.", []

        print("Got some data...") # Just to check if model/agent got some data...
        docs = []
        for doc in response.data:
            docs.append({
                "page_content": doc["content"],
                "metadata": doc["metadata"],
                "similarity": doc["similarity"]
            })

        reranked = rerank_with_cross_encoder(query, docs)
        top_docs = reranked[:3]

        # serialized = "\n\n".join(
        #     f"Similarity: {d['similarity']:.3f}\nSource: {d['metadata']}\nContent: {d['page_content']}"
        #     for d in docs
        # )
        # return serialized, docs
        serialized = "\n\n".join(
            f"Rerank Score: {d['rerank_score']:.3f}\nSource: {d['metadata']}\nContent: {d['page_content']}"
            for d in top_docs
        )
        return serialized, top_docs
    return [retrieve_documents]
