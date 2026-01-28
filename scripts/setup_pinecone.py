# scripts/setup_pinecone.py
"""Script to set up Pinecone index."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag.vectorstore import get_pinecone_manager
from backend.config import settings


def main():
    """Set up Pinecone index."""
    print("🚀 Setting up Pinecone...")
    print(f"  - Index name: {settings.PINECONE_INDEX_NAME}")
    print(f"  - Environment: {settings.PINECONE_ENVIRONMENT}")
    
    pm = get_pinecone_manager()
    
    # Create index
    print("\n📦 Creating index...")
    pm.create_index_if_not_exists(dimension=768)
    
    # Get stats
    print("\n📊 Index Statistics:")
    stats = pm.get_stats()
    print(f"  {stats}")
    
    print("\n✅ Pinecone setup complete!")


if __name__ == "__main__":
    main()