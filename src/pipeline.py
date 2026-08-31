from src.youtube import get_transcript
from src.transcript import create_chunks
from src.embeddings import get_embedding_model
from src.vectorstore import create_vector_store
from src.llm import get_llm
from src.rag import answer_question


class YouTubeRAGPipeline:
    """Complete backend pipeline for the YouTube RAG application."""

    def __init__(self):
        self.embedding_model = None
        self.llm = None
        self.vector_store = None
        self.video_url = None
        self.chunks = None

    def process_video(self, url):
        """
        Process a YouTube video and create its vector store.
        """

        self.video_url = url

        # Get transcript
        transcript = get_transcript(url)

        # Create chunks
        self.chunks = create_chunks(transcript)

        # Create embedding model
        if self.embedding_model is None:
            self.embedding_model = get_embedding_model()

        # Create vector store
        self.vector_store = create_vector_store(
            self.chunks,
            self.embedding_model
        )

        return {
            "segments": len(transcript),
            "chunks": len(self.chunks)
        }

    def ask(self, question, chat_history=None, k=3):
        """
        Ask a question about the processed video
        while using previous conversation history.
        """

        if self.vector_store is None:

            raise ValueError(
                "Please process a YouTube video first."
            )

        # Create LLM only when needed
        if self.llm is None:

            self.llm = get_llm()

        result = answer_question(
            question=question,
            vector_store=self.vector_store,
            embedding_model=self.embedding_model,
            llm=self.llm,
            chat_history=chat_history,
            k=k
        )

        # Make sure the answer returned to Streamlit
        # is always a plain string.
        answer = result.get("answer", "")

        if isinstance(answer, list):

            answer_text = ""

            for item in answer:

                if isinstance(item, dict):

                    if item.get("type") == "text":
                        answer_text += item.get("text", "")

                else:

                    answer_text += str(item)

        else:

            answer_text = str(answer)

        result["answer"] = answer_text

        return result