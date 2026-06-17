"""RAG engine — embeddings, FAISS index, retrieval."""

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP


class RAGEngine:
    def __init__(self):
        self._model = None
        self.index = None
        self.chunks: list[dict] = []

    @property
    def model(self):
        if self._model is None:
            self._model = SentenceTransformer(EMBEDDING_MODEL)
        return self._model

    def build_index(self, chunks: list[dict]):
        """Embed all chunks and build a FAISS index."""
        self.chunks = chunks
        texts = [c["text"] for c in chunks]

        # Split long chunks further if needed
        split_chunks = []
        for chunk in chunks:
            t = chunk["text"]
            if len(t) > CHUNK_SIZE:
                # Simple split by lines to stay under chunk size
                lines = t.split("\n")
                current = ""
                for line in lines:
                    if len(current) + len(line) > CHUNK_SIZE and current:
                        split_chunks.append({"text": current.strip(), "metadata": chunk["metadata"]})
                        # Keep overlap
                        overlap_lines = current.split("\n")[-2:]
                        current = "\n".join(overlap_lines) + "\n" + line + "\n"
                    else:
                        current += line + "\n"
                if current.strip():
                    split_chunks.append({"text": current.strip(), "metadata": chunk["metadata"]})
            else:
                split_chunks.append(chunk)

        self.chunks = split_chunks
        texts = [c["text"] for c in self.chunks]

        embeddings = self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
        embeddings = np.array(embeddings, dtype="float32")

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # Inner product (cosine since normalized)
        self.index.add(embeddings)

        return len(self.chunks)

    def retrieve(self, query: str, top_k: int = 5, module_filter: str = None) -> list[dict]:
        """Retrieve top-k relevant chunks for a query."""
        if self.index is None or not self.chunks:
            return []

        q_emb = self.model.encode([query], normalize_embeddings=True).astype("float32")

        # Search more if we need to filter
        search_k = top_k * 3 if module_filter else top_k
        scores, indices = self.index.search(q_emb, min(search_k, len(self.chunks)))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = self.chunks[idx]
            if module_filter and chunk["metadata"].get("module", "") != module_filter:
                continue
            results.append({
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "score": float(score)
            })
            if len(results) >= top_k:
                break

        return results
