from langchain_core.tools import tool

def create_retriever_tool(retriever):
    @tool(response_format="content_and_artifact")
    def retrieve_documents(query: str):
        """Retrieve relevant documents."""
        docs = retriever.invoke(query)
        serialized = "\n\n".join(
            f"Source: {doc.metadata}\nContent: {doc.page_content}"
            for doc in docs
        )
        return serialized, docs

    return [retrieve_documents]
