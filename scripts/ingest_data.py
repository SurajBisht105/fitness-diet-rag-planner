# scripts/ingest_data.py
"""Script to ingest all fitness and diet data into Pinecone."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag.ingestion import get_ingester
from backend.rag.vectorstore import get_pinecone_manager


def main():
    """Main ingestion script."""
    print("🚀 Starting data ingestion...")
    
    # Initialize Pinecone
    print("📦 Initializing Pinecone...")
    pm = get_pinecone_manager()
    pm.create_index_if_not_exists(dimension=768)
    print("✅ Pinecone index ready")
    
    # Get ingester
    ingester = get_ingester()
    
    # Ingest all data
    print("📥 Ingesting data from data/raw...")
    stats = ingester.ingest_all("data/raw")
    
    print("\n📊 Ingestion Statistics:")
    print(f"  - Workout files processed: {stats['workouts_processed']}")
    print(f"  - Diet files processed: {stats['diets_processed']}")
    print(f"  - Total chunks created: {stats['total_chunks']}")
    
    # Verify ingestion
    print("\n🔍 Verifying ingestion...")
    index_stats = pm.get_stats()
    print(f"  - Total vectors in index: {index_stats}")
    
    print("\n✅ Data ingestion complete!")


if __name__ == "__main__":
    main()