# backend/rag/ingestion.py
"""Data ingestion pipeline for fitness and diet knowledge base."""

import json
from typing import List, Dict, Optional
from pathlib import Path
import hashlib
from datetime import datetime


class FitnessDataIngester:
    """Ingests fitness and diet data into the vector store."""
    
    def __init__(self):
        """Initialize the data ingester."""
        self._pinecone_manager = None
        self._text_splitter = None
    
    @property
    def pinecone_manager(self):
        if self._pinecone_manager is None:
            from backend.rag.vectorstore import get_pinecone_manager
            self._pinecone_manager = get_pinecone_manager()
        return self._pinecone_manager
    
    @property
    def text_splitter(self):
        if self._text_splitter is None:
            from langchain_text_splitters import RecursiveCharacterTextSplitter
            from backend.config import settings
            self._text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
        return self._text_splitter
    
    def ingest_all(self, data_dir: str = "data/raw") -> Dict[str, int]:
        """Ingest all fitness and diet data from the data directory."""
        stats = {
            "workouts_processed": 0,
            "diets_processed": 0,
            "total_chunks": 0
        }
        
        if not self.pinecone_manager.is_available:
            print("Pinecone not available, skipping ingestion")
            return stats
        
        # Ensure index exists
        self.pinecone_manager.create_index_if_not_exists(dimension=768)
        
        # Ingest workout data
        workout_dir = Path(data_dir) / "workouts"
        if workout_dir.exists():
            workout_chunks = self._ingest_directory(workout_dir, "workouts")
            stats["workouts_processed"] = len(list(workout_dir.glob("*.json")))
            stats["total_chunks"] += workout_chunks
        
        # Ingest diet data
        diet_dir = Path(data_dir) / "diets"
        if diet_dir.exists():
            diet_chunks = self._ingest_directory(diet_dir, "diets")
            stats["diets_processed"] = len(list(diet_dir.glob("*.json")))
            stats["total_chunks"] += diet_chunks
        
        return stats
    
    def _ingest_directory(self, directory: Path, namespace: str) -> int:
        """Ingest all files from a directory into specified namespace."""
        total_chunks = 0
        
        for file_path in directory.glob("*.json"):
            try:
                chunks = self._process_json_file(file_path, namespace)
                total_chunks += len(chunks)
                
                if chunks:
                    self.pinecone_manager.upsert_documents(chunks, namespace=namespace)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        
        return total_chunks
    
    def _process_json_file(self, file_path: Path, doc_type: str) -> List[Dict]:
        """Process a JSON file and return document chunks."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = []
        
        if isinstance(data, list):
            for idx, item in enumerate(data):
                item_chunks = self._chunk_json_item(item, file_path.stem, idx, doc_type)
                chunks.extend(item_chunks)
        elif isinstance(data, dict):
            if "items" in data:
                for idx, item in enumerate(data["items"]):
                    item_chunks = self._chunk_json_item(item, file_path.stem, idx, doc_type)
                    chunks.extend(item_chunks)
            else:
                item_chunks = self._chunk_json_item(data, file_path.stem, 0, doc_type)
                chunks.extend(item_chunks)
        
        return chunks
    
    def _chunk_json_item(self, item: Dict, source_file: str, idx: int, doc_type: str) -> List[Dict]:
        """Convert a JSON item to document chunks."""
        text_content = self._json_to_text(item, doc_type)
        text_chunks = self.text_splitter.split_text(text_content)
        
        chunks = []
        for chunk_idx, chunk_text in enumerate(text_chunks):
            chunk_id = self._generate_chunk_id(source_file, idx, chunk_idx)
            
            metadata = {
                "source_file": source_file,
                "doc_type": doc_type,
                "type": item.get("type", doc_type),
                "title": item.get("name", item.get("title", f"{doc_type}_{idx}")),
                "experience_level": item.get("level", item.get("experience_level", "all")),
                "location": item.get("location", "both"),
                "dietary_type": item.get("dietary_type", item.get("preference", "all")),
                "goal": item.get("goal", "general"),
                "chunk_index": chunk_idx,
                "ingested_at": datetime.utcnow().isoformat()
            }
            
            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": metadata
            })
        
        return chunks
    
    def _json_to_text(self, item: Dict, doc_type: str) -> str:
        """Convert a JSON item to readable text format."""
        parts = [f"# {item.get('name', item.get('title', 'Item'))}"]
        
        if item.get('description'):
            parts.append(f"\n{item['description']}")
        
        # Add all relevant fields
        for key in ['level', 'goal', 'location', 'duration', 'calories']:
            if item.get(key):
                parts.append(f"{key.title()}: {item[key]}")
        
        # Handle exercises
        if item.get('exercises'):
            parts.append("\n## Exercises:")
            for exercise in item['exercises']:
                ex_text = f"- {exercise.get('name', 'Exercise')}"
                if exercise.get('sets'):
                    ex_text += f": {exercise['sets']} sets"
                if exercise.get('reps'):
                    ex_text += f" x {exercise['reps']}"
                parts.append(ex_text)
        
        # Handle meals
        if item.get('meals'):
            parts.append("\n## Meals:")
            for meal in item['meals']:
                parts.append(f"\n### {meal.get('name', 'Meal')}")
                if meal.get('items'):
                    for food in meal['items']:
                        if isinstance(food, dict):
                            parts.append(f"- {food.get('name', 'Food')}: {food.get('portion', '')}")
                        else:
                            parts.append(f"- {food}")
        
        return "\n".join(parts)
    
    def _generate_chunk_id(self, source: str, item_idx: int, chunk_idx: int) -> str:
        """Generate a unique chunk ID."""
        content = f"{source}_{item_idx}_{chunk_idx}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def ingest_single_document(self, document: Dict, doc_type: str) -> int:
        """Ingest a single document."""
        if not self.pinecone_manager.is_available:
            return 0
        
        namespace = f"{doc_type}s"
        chunks = self._chunk_json_item(document, "manual_entry", 0, namespace)
        
        if chunks:
            self.pinecone_manager.upsert_documents(chunks, namespace=namespace)
        
        return len(chunks)
    
    def clear_namespace(self, namespace: str):
        """Clear all data from a namespace."""
        if self.pinecone_manager.is_available:
            self.pinecone_manager.delete_namespace(namespace)


# Singleton instance
_ingester: Optional[FitnessDataIngester] = None


def get_ingester() -> FitnessDataIngester:
    """Get or create singleton ingester."""
    global _ingester
    if _ingester is None:
        _ingester = FitnessDataIngester()
    return _ingester