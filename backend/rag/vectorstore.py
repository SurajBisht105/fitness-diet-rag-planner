# backend/rag/vectorstore.py
"""Pinecone vector store management."""

from typing import List, Dict, Optional
from backend.config import settings
import time


class PineconeManager:
    """Manages Pinecone vector database operations."""
    
    def __init__(self):
        """Initialize Pinecone client."""
        self._pc = None
        self._index = None
        self._vectorstore = None
        self._initialized = False
        
        if settings.PINECONE_API_KEY:
            self._initialize()
    
    def _initialize(self):
        """Initialize Pinecone connection."""
        try:
            from pinecone import Pinecone
            self._pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self._initialized = True
        except Exception as e:
            print(f"Warning: Could not initialize Pinecone: {e}")
            self._initialized = False
    
    @property
    def is_available(self) -> bool:
        """Check if Pinecone is available."""
        return self._initialized and self._pc is not None
    
    def create_index_if_not_exists(self, dimension: int = 768):
        """Create Pinecone index if it doesn't exist."""
        if not self.is_available:
            print("Pinecone not available, skipping index creation")
            return
        
        try:
            from pinecone import ServerlessSpec
            
            existing_indexes = [idx.name for idx in self._pc.list_indexes()]
            
            if settings.PINECONE_INDEX_NAME not in existing_indexes:
                self._pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=settings.PINECONE_ENVIRONMENT
                    )
                )
                # Wait for index to be ready
                while not self._pc.describe_index(settings.PINECONE_INDEX_NAME).status['ready']:
                    time.sleep(1)
            
            self._index = self._pc.Index(settings.PINECONE_INDEX_NAME)
        except Exception as e:
            print(f"Error creating Pinecone index: {e}")
    
    def get_index(self):
        """Get Pinecone index."""
        if not self.is_available:
            return None
        
        if self._index is None:
            try:
                self._index = self._pc.Index(settings.PINECONE_INDEX_NAME)
            except Exception as e:
                print(f"Error getting Pinecone index: {e}")
        return self._index
    
    def get_vectorstore(self, namespace: str = "fitness"):
        """Get LangChain vectorstore wrapper."""
        if not self.is_available:
            return None
        
        try:
            from langchain_pinecone import PineconeVectorStore
            from backend.rag.embeddings import get_embedding_manager
            
            embedding_manager = get_embedding_manager()
            if not embedding_manager.is_available:
                return None
            
            return PineconeVectorStore(
                index=self.get_index(),
                embedding=embedding_manager.embeddings,
                namespace=namespace
            )
        except Exception as e:
            print(f"Error creating vectorstore: {e}")
            return None
    
    def upsert_documents(self, documents: List[Dict], namespace: str = "fitness") -> int:
        """Upsert documents into Pinecone."""
        if not self.is_available:
            print("Pinecone not available, skipping upsert")
            return 0
        
        try:
            from backend.rag.embeddings import get_embedding_manager
            
            embedding_manager = get_embedding_manager()
            if not embedding_manager.is_available:
                return 0
            
            vectors = []
            texts = [doc['text'] for doc in documents]
            embeddings = embedding_manager.embed_documents(texts)
            
            for doc, embedding in zip(documents, embeddings):
                vectors.append({
                    'id': doc['id'],
                    'values': embedding,
                    'metadata': {
                        **doc.get('metadata', {}),
                        'text': doc['text'][:1000]
                    }
                })
            
            # Batch upsert
            index = self.get_index()
            if index:
                batch_size = 100
                for i in range(0, len(vectors), batch_size):
                    batch = vectors[i:i + batch_size]
                    index.upsert(vectors=batch, namespace=namespace)
            
            return len(vectors)
        except Exception as e:
            print(f"Error upserting documents: {e}")
            return 0
    
    def query(self, query: str, top_k: int = 5, namespace: str = "fitness",
              filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Query the vector store."""
        if not self.is_available:
            return []
        
        try:
            from backend.rag.embeddings import get_embedding_manager
            
            embedding_manager = get_embedding_manager()
            if not embedding_manager.is_available:
                return []
            
            query_embedding = embedding_manager.embed_query(query)
            index = self.get_index()
            
            if not index:
                return []
            
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=namespace,
                filter=filter_dict,
                include_metadata=True
            )
            
            return [
                {
                    'id': match['id'],
                    'score': match['score'],
                    'metadata': match.get('metadata', {}),
                    'text': match.get('metadata', {}).get('text', '')
                }
                for match in results.get('matches', [])
            ]
        except Exception as e:
            print(f"Error querying Pinecone: {e}")
            return []
    
    def delete_namespace(self, namespace: str):
        """Delete all vectors in a namespace."""
        if not self.is_available:
            return
        
        try:
            index = self.get_index()
            if index:
                index.delete(delete_all=True, namespace=namespace)
        except Exception as e:
            print(f"Error deleting namespace: {e}")
    
    def get_stats(self) -> Dict:
        """Get index statistics."""
        if not self.is_available:
            return {"status": "unavailable"}
        
        try:
            index = self.get_index()
            if index:
                return index.describe_index_stats()
            return {"status": "no index"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Singleton instance
_pinecone_manager: Optional[PineconeManager] = None


def get_pinecone_manager() -> PineconeManager:
    """Get or create singleton Pinecone manager."""
    global _pinecone_manager
    if _pinecone_manager is None:
        _pinecone_manager = PineconeManager()
    return _pinecone_manager