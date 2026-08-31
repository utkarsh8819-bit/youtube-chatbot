from src.youtube import get_transcript
from src.transcript import create_chunks
from src.embeddings import get_embedding_model
from src.vectorstore import create_vector_store
from src.llm import get_llm
from src.rag import answer_question


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


# 5. Create Gemini LLM
llm = get_llm()


# 6. Ask question
question = "What problem are we trying to solve in this video?"


# 7. Generate RAG answer
result = answer_question(
    question=question,
    vector_store=vector_store,
    embedding_model=embedding_model,
    llm=llm,
    k=3
)


# 8. Print answer
print("\n==============================")
print("RAG ANSWER")
print("==============================\n")

print(result["answer"])


# 9. Print sources
print("\n==============================")
print("SOURCES")
print("==============================\n")

for i, source in enumerate(result["sources"], start=1):

    chunk = source["chunk"]

    print(
        f"{i}. "
        f"{chunk['start']:.2f}s - "
        f"{chunk['end']:.2f}s"
    )