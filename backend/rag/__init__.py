# backend/rag/__init__.py
"""RAG package initialization - Lazy imports to avoid circular dependencies."""

def get_embedding_manager():
    from backend.rag.embeddings import get_embedding_manager as _get
    return _get()

def get_pinecone_manager():
    from backend.rag.vectorstore import get_pinecone_manager as _get
    return _get()

def get_fitness_retriever():
    from backend.rag.retriever import get_fitness_retriever as _get
    return _get()

def get_rag_chain():
    from backend.rag.chain import get_rag_chain as _get
    return _get()

def get_ingester():
    from backend.rag.ingestion import get_ingester as _get
    return _get()