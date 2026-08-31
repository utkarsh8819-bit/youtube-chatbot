from src.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "Explain what RAG is in two simple sentences."
)

print("\nGemini response:\n")
print(response.content)