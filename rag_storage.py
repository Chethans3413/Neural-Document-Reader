"""
RAG Storage Module - Handles document loading and embedding storage
"""
import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import time

CHROMA_DB_PATH = "./chroma_db"

class RAGStorage:
    """Handles document storage and retrieval"""
    
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        self.db = None
        self.retriever = None
    
    def clear_storage(self):
        """Clear existing storage"""
        if os.path.exists(CHROMA_DB_PATH):
            try:
                # Close the database connection first
                if self.db is not None:
                    self.db = None
                    self.retriever = None
                
                # Wait a moment for file locks to release
                time.sleep(1)
                
                # Try to remove
                for attempt in range(3):
                    try:
                        shutil.rmtree(CHROMA_DB_PATH)
                        print("✓ Cleared old storage")
                        return
                    except PermissionError:
                        if attempt < 2:
                            time.sleep(1)
                            continue
                        else:
                            raise
            except Exception as e:
                print(f"⚠ Warning: Could not clear old storage: {str(e)}")
                # Continue anyway, we'll try to use existing
    
    def load_pdf(self, pdf_path):
        """Load PDF and create embeddings"""
        try:
            # Verify file exists
            if not os.path.exists(pdf_path):
                print(f"✗ File not found: {pdf_path}")
                return False
            
            print(f"✓ Loading PDF: {pdf_path}")
            
            # Load PDF
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            if not documents:
                print("✗ No pages found in PDF")
                return False
                
            print(f"✓ Loaded {len(documents)} pages from PDF")
            
            # Split text - smaller chunks for speed
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=300,
                chunk_overlap=20
            )
            docs = text_splitter.split_documents(documents)
            print(f"✓ Split into {len(docs)} chunks")
            
            # Clear old storage
            self.clear_storage()
            
            # Create embeddings and store
            print("✓ Creating embeddings...")
            self.db = Chroma.from_documents(
                docs,
                self.embeddings,
                persist_directory=CHROMA_DB_PATH
            )
            print("✓ Created embeddings and storage")
            
            # Create retriever
            self.retriever = self.db.as_retriever(search_kwargs={"k": 2})
            print("✓ Retriever ready")
            
            return True
            
        except Exception as e:
            print(f"✗ Error loading PDF: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return False
    
    def get_retriever(self):
        """Get the retriever"""
        return self.retriever
    
    def search_documents(self, query, k=2):
        """Search for relevant documents"""
        if self.db is None:
            return []
        try:
            results = self.db.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"✗ Search error: {str(e)}")
            return []
