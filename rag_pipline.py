from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
import shutil

def create_qa_chain(pdf_path):
    """Load PDF and create a QA chain with optimizations"""
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Smaller chunks for faster processing
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    docs = text_splitter.split_documents(documents)

    # Use default 768-dimensional embeddings for consistency
    embeddings = HuggingFaceEmbeddings()

    # Use a temporary Chroma database that gets cleared each time
    persist_directory = "./chroma_db_temp"
    
    # Clear previous database if exists to avoid dimension mismatch
    if os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)
    
    db = Chroma.from_documents(
        docs, 
        embeddings,
        persist_directory=persist_directory
    )

    # Retrieve fewer documents for speed
    retrievers = db.as_retriever(search_kwargs={"k": 2})

    # Use mistral model with output limits for faster responses
    llm = Ollama(
        model="mistral",
        base_url="http://localhost:11434",
        temperature=0.1,
        num_predict=256  # Limit output length for faster responses
    )

    # Create a simple retrieval chain using LCEL with ChatPromptTemplate
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_template(
        """Answer the question based on the context provided. Be concise and direct. Keep answer to 2-3 sentences max.

Context:
{context}

Question: {question}

Answer:"""
    )

    chain = (
        {"context": retrievers | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain