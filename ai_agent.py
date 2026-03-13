"""
AI Agent Module - Handles question answering using RAG and LLM
"""
from rag_storage import RAGStorage
from llm_handler import LLMHandler

class AIAgent:
    """AI Agent for document Q&A"""
    
    def __init__(self, model_name="orca-mini"):
        """Initialize AI Agent with RAG storage and LLM"""
        self.rag_storage = RAGStorage()
        self.llm_handler = LLMHandler(model_name=model_name, temperature=0)
        self.llm = self.llm_handler.get_llm()
    
    def load_document(self, pdf_path):
        """
        Load a PDF document
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            True if successful, False otherwise
        """
        return self.rag_storage.load_pdf(pdf_path)
    
    def answer_question(self, question):
        """
        Answer a question based on loaded document
        
        Args:
            question: The question to answer
            
        Returns:
            The answer string
        """
        try:
            # Get relevant documents
            relevant_docs = self.rag_storage.search_documents(question, k=2)
            
            if not relevant_docs:
                return "❌ No relevant information found in the document."
            
            # Prepare context
            context = "\n\n".join(
                [f"Document {i+1}:\n{doc.page_content}" 
                 for i, doc in enumerate(relevant_docs)]
            )
            
            # Create prompt - keep it SHORT for fast processing
            prompt = f"""Answer based on context. Be brief (1-2 sentences).

Context: {context}

Q: {question}
A:"""
            
            # Get answer from LLM
            answer = self.llm.invoke(prompt)
            return answer.strip()
            
        except Exception as e:
            print(f"✗ Error answering question: {str(e)}")
            return f"❌ Error: {str(e)}"
    
    def get_document_summary(self):
        """Get a summary of the loaded document"""
        docs = self.rag_storage.search_documents("summary main topics overview")
        if not docs:
            return "No document loaded"
        
        context = "\n".join([doc.page_content[:200] for doc in docs])
        
        prompt = f"""Summarize the following document in 2-3 sentences:

{context}

Summary:"""
        
        return self.llm.invoke(prompt)
