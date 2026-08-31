from src.retriever import retrieve_documents


def answer_question(
    question,
    vector_store,
    embedding_model,
    llm,
    chat_history=None,
    k=3
):
    """
    Retrieve relevant transcript chunks and generate
    an answer using Gemini with conversation history.
    """

    if chat_history is None:
        chat_history = []

    # --------------------------------------------------------
    # Build conversation history text
    # --------------------------------------------------------

    history_parts = []

    for message in chat_history:

        role = message.get("role", "")
        content = message.get("content", "")

        if role == "user":
            history_parts.append(
                f"User: {content}"
            )

        elif role == "assistant":
            history_parts.append(
                f"Assistant: {content}"
            )

    conversation_history = "\n".join(history_parts)

    # --------------------------------------------------------
    # Create a retrieval query
    # --------------------------------------------------------

    if conversation_history:

        retrieval_query = f"""
Previous conversation:

{conversation_history}

Current question:

{question}
"""

    else:

        retrieval_query = question

    # --------------------------------------------------------
    # Retrieve relevant chunks
    # --------------------------------------------------------

    results = retrieve_documents(
        vector_store,
        embedding_model,
        retrieval_query,
        k=k
    )

    # --------------------------------------------------------
    # Build transcript context
    # --------------------------------------------------------

    context_parts = []

    for result in results:

        chunk = result["chunk"]

        context_parts.append(
            f"""
Timestamp: {chunk['start']:.2f}s - {chunk['end']:.2f}s

{chunk['text']}
"""
        )

    context = "\n---\n".join(context_parts)

    # --------------------------------------------------------
    # Build conversation section for Gemini
    # --------------------------------------------------------

    if conversation_history:

        conversation_section = f"""
Previous conversation:

{conversation_history}
"""

    else:

        conversation_section = """
There is no previous conversation.
"""

    # --------------------------------------------------------
    # Prompt Gemini
    # --------------------------------------------------------

    prompt = f"""
You are a helpful AI assistant that answers questions
about a YouTube video.

Your job is to answer the user's question using ONLY
the provided video transcript context.

You also have access to the previous conversation so
you can understand follow-up questions.

IMPORTANT RULES:

- Always answer in English.
- The transcript may be in Hindi, English, or another language.
- If the relevant information is in another language,
  understand it and explain it in English.
- Do not answer in Hindi or any other language.
- Use the previous conversation to understand references
  such as "it", "that", "this", "they", or "the first step".
- Do not rely on your general knowledge when answering
  questions about the video.
- Use ONLY information supported by the provided transcript.
- If the answer cannot be found in the transcript context,
  say that the information is not available in the video.
- Do not make up information.
- Keep the answer clear and easy to understand.

{conversation_section}

Video transcript context:

{context}

Current user question:

{question}

Answer in English:
"""

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    response = llm.invoke(prompt)

    # --------------------------------------------------------
    # Extract clean text from Gemini response
    # --------------------------------------------------------

    content = response.content

    if isinstance(content, list):

        answer_text = ""

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":
                    answer_text += item.get("text", "")

            else:

                answer_text += str(item)

    else:

        answer_text = str(content)

    # --------------------------------------------------------
    # Return answer and sources
    # --------------------------------------------------------

    return {
        "answer": answer_text,
        "sources": results
    }