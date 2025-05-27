import openai
import numpy as np
import json
import os
from typing import List, Dict

from config import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


def get_embedding(text: str) -> np.ndarray:
    """Get the OpenAI embedding for a given string."""
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class ChunkStore:
    def __init__(self):
        self.chunks: List[Dict] = []

    def add_chunk(self, chunk: Dict):
        """Embed a single chunk and add it to the store."""
        if "embedding" not in chunk:
            chunk["embedding"] = get_embedding(chunk["text"])
        self.chunks.append(chunk)

    def bulk_add(self, chunks: List[Dict]):
        """Embed and add multiple chunks to the store."""
        for chunk in chunks:
            self.add_chunk(chunk)

    def query(self, question: str, top_k=5) -> List[Dict]:
        """Find the top-k most relevant chunks for a user query, grouping related project information."""
        query_embedding = get_embedding(question)
        
        # First, get all chunks and their similarity scores
        scored_chunks = [
            (chunk, cosine_similarity(query_embedding, chunk["embedding"]))
            for chunk in self.chunks
        ]
        
        # Sort by similarity score
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        # Group chunks by project when the query is about contributors
        if any(word in question.lower() for word in ["who", "working", "contributor", "team", "member"]):
            # Get the top scoring project chunks first
            project_chunks = {}
            for chunk, score in scored_chunks:
                if chunk["object_type"] == "project":
                    project_id = chunk["object_id"]
                    if project_id not in project_chunks:
                        project_chunks[project_id] = []
                    project_chunks[project_id].append(chunk)
            
            # Return all chunks for the most relevant projects
            result = []
            for project_id, chunks in project_chunks.items():
                result.extend(chunks)
                if len(result) >= top_k:
                    break
            
            # If we still have room, add other relevant chunks
            remaining_slots = top_k - len(result)
            if remaining_slots > 0:
                other_chunks = [chunk for chunk, _ in scored_chunks 
                              if chunk["object_id"] not in project_chunks]
                result.extend(other_chunks[:remaining_slots])
            
            return result[:top_k]
        
        # For other queries, return the top-k most similar chunks
        return [chunk for chunk, _ in scored_chunks[:top_k]]

    def exists(self, text: str) -> bool:
        """Check if a chunk with this exact text is already stored."""
        return any(c["text"] == text for c in self.chunks)

    def count(self) -> int:
        return len(self.chunks)

    def clear(self):
        """Reset the store (remove all chunks)."""
        self.chunks = []

    def save(self, filepath: str):
        """Save all chunks (with embeddings) to a JSON file."""
        serializable = [
            {
                k: (v.tolist() if k == "embedding" else v)
                for k, v in chunk.items()
            }
            for chunk in self.chunks
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
        print(f"💾 Saved {len(self.chunks)} chunks to {filepath}")

    def load(self, filepath: str):
        """Load chunks and embeddings from a JSON file."""
        if not os.path.exists(filepath):
            print(f"⚠️ File not found: {filepath}")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.chunks = [
            {
                **chunk,
                "embedding": np.array(chunk["embedding"])
            }
            for chunk in data
        ]
        print(f"📂 Loaded {len(self.chunks)} chunks from {filepath}")
