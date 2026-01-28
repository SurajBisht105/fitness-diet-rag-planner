# backend/rag/embeddings.py
"""Embedding generation using Google GenAI or HuggingFace."""

from typing import List, Optional
from backend.config import settings


class EmbeddingManager:
    """Manages embedding generation with multiple providers."""
    
    def __init__(self, provider: str = "gemini"):
        """
        Initialize embedding manager.
        
        Args:
            provider: Either "gemini" or "huggingface"
        """
        self.provider = provider
        self._embeddings = None
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize the embedding model based on provider."""
        if self.provider == "gemini" and settings.GOOGLE_API_KEY:
            try:
                from langchain_google_genai import GoogleGenerativeAIEmbeddings
                self._embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=settings.GOOGLE_API_KEY
                )
            except Exception as e:
                print(f"Warning: Could not initialize Gemini embeddings: {e}")
                self._use_huggingface_fallback()
        else:
            self._use_huggingface_fallback()
    
    def _use_huggingface_fallback(self):
        """Use HuggingFace embeddings as fallback."""
        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            self._embeddings = HuggingFaceEmbeddings(
                model_name=settings.HF_EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            self.provider = "huggingface"
        except Exception as e:
            print(f"Warning: Could not initialize HuggingFace embeddings: {e}")
            self._embeddings = None
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        if self._embeddings is None:
            raise RuntimeError("No embedding model available")
        return self._embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query."""
        if self._embeddings is None:
            raise RuntimeError("No embedding model available")
        return self._embeddings.embed_query(text)
    
    @property
    def embeddings(self):
        """Get the underlying embeddings object for LangChain integration."""
        return self._embeddings
    
    @property
    def is_available(self) -> bool:
        """Check if embeddings are available."""
        return self._embeddings is not None


# Singleton instance
_embedding_manager: Optional[EmbeddingManager] = None


def get_embedding_manager(provider: str = "gemini") -> EmbeddingManager:
    """Get or create singleton embedding manager."""
    global _embedding_manager
    if _embedding_manager is None:
        _embedding_manager = EmbeddingManager(provider)
    return _embedding_manager