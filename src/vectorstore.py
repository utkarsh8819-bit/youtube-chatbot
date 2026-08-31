import numpy as np


class SimpleVectorStore:
    """A lightweight local vector store using cosine similarity."""

    def __init__(self, chunks, embeddings):
        self.chunks = chunks
        self.embeddings = np.array(embeddings, dtype=np.float32)

    def similarity_search(self, query, embedding_model, k=3):
        """Return the k most similar chunks to the query."""

        query_embedding = embedding_model.embed_query(query)

        query_embedding = np.array(
            query_embedding,
            dtype=np.float32
        )

        # Cosine similarity
        similarities = np.dot(
            self.embeddings,
            query_embedding
        ) / (
            np.linalg.norm(self.embeddings, axis=1)
            * np.linalg.norm(query_embedding)
            + 1e-10
        )

        # Get indices of the highest similarity scores
        top_indices = np.argsort(similarities)[::-1][:k]

        results = []

        for index in top_indices:
            results.append({
                "chunk": self.chunks[index],
                "score": float(similarities[index])
            })

        return results


def create_vector_store(chunks, embedding_model):
    """Create a local vector store from transcript chunks."""

    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.embed_documents(texts)

    return SimpleVectorStore(
        chunks=chunks,
        embeddings=embeddings
    )