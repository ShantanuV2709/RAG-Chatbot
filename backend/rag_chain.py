from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
import os
import sys
import logging
from config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Check if data files exist
if not os.path.exists(settings.txt_file_path):
    logger.warning(f"⚠️  {settings.txt_file_path} not found. Continuing without it.")
if not os.path.exists(settings.pdf_file_path):
    logger.warning(f"⚠️  {settings.pdf_file_path} not found. Continuing without it.")

# Load documents with error handling
all_docs = []
try:
    if os.path.exists(settings.txt_file_path):
        loader = TextLoader(settings.txt_file_path)
        docs = loader.load()
        all_docs.extend(docs)
        logger.info(f"✅ Loaded {len(docs)} documents from {settings.txt_file_path}")
except Exception as e:
    logger.error(f"⚠️  Error loading {settings.txt_file_path}: {e}")

try:
    if os.path.exists(settings.pdf_file_path):
        pdf_loader = PyPDFLoader(settings.pdf_file_path)
        pdf_docs = pdf_loader.load()
        all_docs.extend(pdf_docs)
        logger.info(f"✅ Loaded {len(pdf_docs)} documents from {settings.pdf_file_path}")
except Exception as e:
    logger.error(f"⚠️  Error loading {settings.pdf_file_path}: {e}")

# Verify we have documents to process
if not all_docs:
    logger.error("❌ No documents loaded. Please add knowledge.txt or Knowledge.pdf to the data/ directory.")
    sys.exit(1)

# Split documents using config values
splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.chunk_size, 
    chunk_overlap=settings.chunk_overlap
)
split_docs = splitter.split_documents(all_docs)
logger.info(f"✅ Total chunks created: {len(split_docs)}")

# Initialize embeddings using config
embedding = GoogleGenerativeAIEmbeddings(
    model=settings.embedding_model, 
    google_api_key=settings.google_api_key
)

# Use persistent ChromaDB to save embeddings to disk
persist_directory = "chroma_db"

# Check if vector store already exists
if os.path.exists(persist_directory):
    logger.info(f"📁 Loading existing vector store from {persist_directory}")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    logger.info("✅ Vector store loaded from disk (no API calls needed)")
else:
    logger.info(f"🆕 Creating new vector store in {persist_directory}")
    vectorstore = Chroma.from_documents(
        split_docs, 
        embedding=embedding,
        persist_directory=persist_directory
    )
    logger.info(f"✅ Vector store created and saved to {persist_directory}")

retriever = vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k})
logger.info("✅ Retriever initialized successfully")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

# Initialize LLM using config
llm = GoogleGenerativeAI(
    model=settings.llm_model, 
    google_api_key=settings.google_api_key
)
logger.info("✅ LLM initialized successfully")


qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    output_key="answer",
)