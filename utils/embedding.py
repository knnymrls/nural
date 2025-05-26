import openai
import numpy as np
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_embedding(text: str) -> np.ndarray:
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def rank_profiles(query: str, profile_texts: list[str], profile_embeddings: list[np.ndarray]) -> list[int]:
    query_embedding = get_embedding(query)
    scores = [cosine_similarity(query_embedding, emb) for emb in profile_embeddings]
    return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
