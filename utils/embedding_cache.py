import os
import numpy as np
from typing import List, Tuple
from .embedding import get_embedding

CACHE_DIR = "cache"
EMBEDDINGS_FILE = os.path.join(CACHE_DIR, "profile_embeddings.npy")
TEXTS_FILE = os.path.join(CACHE_DIR, "profile_texts.npy")

def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def save_embeddings(texts: List[str], embeddings: List[np.ndarray]):
    """Save texts and their embeddings to cache files."""
    ensure_cache_dir()
    np.save(EMBEDDINGS_FILE, np.array(embeddings))
    np.save(TEXTS_FILE, np.array(texts, dtype=object))

def load_embeddings() -> Tuple[List[str], List[np.ndarray]]:
    """Load texts and their embeddings from cache files."""
    if not os.path.exists(EMBEDDINGS_FILE) or not os.path.exists(TEXTS_FILE):
        return [], []
    
    embeddings = np.load(EMBEDDINGS_FILE, allow_pickle=True)
    texts = np.load(TEXTS_FILE, allow_pickle=True)
    return texts.tolist(), embeddings.tolist()

def get_or_create_embeddings(texts: List[str]) -> Tuple[List[str], List[np.ndarray]]:
    """Get embeddings from cache if they exist, otherwise create and cache them."""
    cached_texts, cached_embeddings = load_embeddings()
    
    # If we have cached embeddings and the texts match, return them
    if len(cached_texts) == len(texts) and all(ct == t for ct, t in zip(cached_texts, texts)):
        return cached_texts, cached_embeddings
    
    # Otherwise, create new embeddings
    print("🔄 Generating new embeddings...")
    embeddings = [get_embedding(text) for text in texts]
    save_embeddings(texts, embeddings)
    return texts, embeddings 