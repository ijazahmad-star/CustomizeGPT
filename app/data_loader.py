from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from pathlib import Path

# def load_pdfs_from_directory(directory_path):
#     docs = []
#     for pdf_file in Path(directory_path).glob("*.pdf"):
#         loader = PyPDFLoader(str(pdf_file))
#         docs.extend(loader.load())
#     return docs

def load_pdfs_from_directory(directory_path: str):
    docs = []
    for pdf_file in Path(directory_path).rglob("*.pdf"):
        try:
            # print("Reading data from: ", pdf_file)
            loader = PyPDFLoader(str(pdf_file))
            docs.extend(loader.load())
        except Exception as e:
            print(f"Error loading {pdf_file}: {e}")
    return docs

def load_from_websites(urls):
    docs = []
    for url in urls:
        loader = WebBaseLoader(url)
        docs.extend(loader.load())
    return docs
