"""
LLM Handler Module - Manages LLM initialization and configuration
"""
from langchain_community.llms import Ollama

class LLMHandler:
    """Handles LLM initialization and configuration"""
    
    def __init__(self, model_name="mistral", temperature=0):
        """
        Initialize LLM Handler
        
        Args:
            model_name: Name of the Ollama model (mistral, neural-chat, etc)
            temperature: Model temperature (0 = deterministic, 1 = creative)
        """
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Ollama LLM"""
        try:
            self.llm = Ollama(
                model=self.model_name,
                base_url="http://localhost:11434",
                temperature=self.temperature
            )
            print(f"✓ LLM initialized: {self.model_name}")
        except Exception as e:
            print(f"✗ LLM initialization error: {str(e)}")
            raise
    
    def get_llm(self):
        """Get the LLM instance"""
        return self.llm
    
    def invoke(self, prompt):
        """
        Invoke LLM with a prompt
        
        Args:
            prompt: The input prompt
            
        Returns:
            The LLM response
        """
        if self.llm is None:
            raise Exception("LLM not initialized")
        
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            print(f"✗ LLM invocation error: {str(e)}")
            raise
