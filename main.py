from app.config import PDF_DIR, WEB_URLS, EMAIL_SYSTEM_PROMPT
from app.data_loader import load_pdfs_from_directory, load_from_websites
# from app.vectorstore import build_vectorstore
from app.tools import create_retriever_tool
from app.graph_builder import build_workflow
from app.ui import launch_ui
from app.vectorstore_weaviate import create_or_load_vectorstore
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("Loading documents...")
pdf_docs = load_pdfs_from_directory(PDF_DIR)
web_docs = load_from_websites(WEB_URLS)
all_docs = pdf_docs + web_docs
#
print("Building vector store...")
# retriever = build_vectorstore(all_docs)
retriever = create_or_load_vectorstore(all_docs)

print("Setting up tools...")
tools = create_retriever_tool(retriever)

print("Building LangGraph workflow...")
app = build_workflow(tools, EMAIL_SYSTEM_PROMPT)
config = {"configurable": {"thread_id": "1"}}

print("\n\nLaunching Strategisthub Email Assistant UI...")
ui = launch_ui(app, config)
ui.launch()
