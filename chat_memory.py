import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

embedder = SentenceTransformer("all-MiniLM-L6-v2")
dimension = 384
index = faiss.IndexFlatL2(dimension)
stored_texts = []

def add_to_chat_memory(message: str):
    vector = embedder.encode([message])
    index.add(np.array(vector))
    stored_texts.append(message)

def get_chat_context(current_input: str, k=5):
    if not stored_texts:
        return ""

    query_vector = embedder.encode([current_input])
    _, indices = index.search(query_vector, k)

    retrieved = [stored_texts[i] for i in indices[0] if i < len(stored_texts)]
    return "\n".join(retrieved)
