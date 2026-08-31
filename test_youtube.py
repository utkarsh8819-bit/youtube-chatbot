from src.youtube import get_transcript
from src.transcript import create_chunks
from src.embeddings import get_embedding_model
from src.vectorstore import create_vector_store
from src.retriever import retrieve_documents


url = "https://www.youtube.com/watch?v=J5_-l7WIO_w"

# 1. Get transcript
transcript = get_transcript(url)

# 2. Create chunks
chunks = create_chunks(transcript)

print(f"Transcript segments: {len(transcript)}")
print(f"Created chunks: {len(chunks)}")

# 3. Create embedding model
embedding_model = get_embedding_model()

# 4. Create vector store
vector_store = create_vector_store(
    chunks,
    embedding_model
)

print("\nVector store created successfully!")

# 5. Ask a question
query = "What problem are we trying to solve in this video?"

# 6. Retrieve relevant chunks
results = retrieve_documents(
    vector_store,
    embedding_model,
    query,
    k=3
)

print(f"\nQuestion: {query}")
print(f"\nRetrieved {len(results)} relevant chunks:\n")

# 7. Display results
for i, result in enumerate(results, start=1):

    chunk = result["chunk"]
    score = result["score"]

    print(f"--- Result {i} ---")
    print(f"Similarity: {score:.4f}")
    print(f"Timestamp: {chunk['start']:.2f}s - {chunk['end']:.2f}s")
    print(f"Text: {chunk['text'][:500]}")
    print()