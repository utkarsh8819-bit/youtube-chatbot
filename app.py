import streamlit as st
from urllib.parse import urlparse, parse_qs

from src.pipeline import YouTubeRAGPipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="YouTube AI Chatbot",
    page_icon="🎥",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_video_id(url):
    """
    Extract the YouTube video ID from a YouTube URL.
    """

    try:

        parsed_url = urlparse(url)

        # Normal YouTube URL
        if parsed_url.hostname in [
            "www.youtube.com",
            "youtube.com"
        ]:

            query = parse_qs(parsed_url.query)

            if "v" in query:
                return query["v"][0]

        # Short YouTube URL
        if parsed_url.hostname == "youtu.be":

            return parsed_url.path.strip("/")

    except Exception:

        pass

    return None


def timestamp_to_seconds(timestamp):
    """
    Convert a timestamp in seconds to an integer.
    """

    return int(float(timestamp))


# ============================================================
# HEADER
# ============================================================

st.title("🎥 YouTube RAG Assistant")

st.write(
    "Ask questions about any YouTube video using "
    "Retrieval-Augmented Generation (RAG)."
)


# ============================================================
# SESSION STATE
# ============================================================

if "pipeline" not in st.session_state:

    st.session_state.pipeline = YouTubeRAGPipeline()


if "video_processed" not in st.session_state:

    st.session_state.video_processed = False


if "processed_url" not in st.session_state:

    st.session_state.processed_url = None


if "messages" not in st.session_state:

    st.session_state.messages = []


if "video_info" not in st.session_state:

    st.session_state.video_info = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Project Info")

    st.write(
        "This application uses:"
    )

    st.markdown(
        """
        - 🎥 YouTube Transcript
        - ✂️ Text Chunking
        - 🧠 Multilingual Embeddings
        - 🔎 FAISS Vector Search
        - 🤖 Gemini
        - 💬 Streamlit
        """
    )

    st.divider()

    st.caption(
        "YouTube RAG Assistant"
    )


# ============================================================
# YOUTUBE URL INPUT
# ============================================================

st.subheader("🎬 Select a YouTube Video")

url = st.text_input(
    "YouTube Video URL",
    placeholder="Paste a YouTube URL here...",
    key="youtube_url"
)


# ============================================================
# PROCESS VIDEO
# ============================================================

if st.button(
    "🚀 Process Video",
    use_container_width=False
):

    if not url:

        st.warning(
            "⚠️ Please enter a YouTube URL."
        )

    else:

        video_id = get_video_id(url)

        if not video_id:

            st.error(
                "❌ Invalid YouTube URL. "
                "Please enter a valid YouTube video URL."
            )

        else:

            with st.spinner(
                "🔄 Processing video... "
                "This may take a moment."
            ):

                try:

                    info = (
                        st.session_state.pipeline
                        .process_video(url)
                    )

                    st.session_state.video_processed = True

                    st.session_state.processed_url = url

                    st.session_state.video_info = info

                    # Start fresh conversation
                    st.session_state.messages = []

                    st.success(
                        "✅ Video processed successfully!"
                    )

                except Exception as e:

                    st.session_state.video_processed = False

                    st.session_state.processed_url = None

                    st.session_state.video_info = None

                    st.error(
                        f"❌ Error while processing video:\n\n{e}"
                    )


# ============================================================
# VIDEO INFORMATION + VIDEO PLAYER
# ============================================================

if st.session_state.video_processed:

    st.divider()

    st.subheader("🎥 Video")

    st.video(
        st.session_state.processed_url
    )

    # Video processing statistics
    info = st.session_state.video_info

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Transcript Segments",
            info["segments"]
        )

    with col2:

        st.metric(
            "Text Chunks",
            info["chunks"]
        )


    # ========================================================
    # CHAT SECTION
    # ========================================================

    st.divider()

    st.subheader(
        "💬 Chat with your video"
    )

    st.caption(
        "Ask questions about the content of this video."
    )


    # ========================================================
    # DISPLAY CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

            # Display sources for assistant messages
            if (
                message["role"] == "assistant"
                and "sources" in message
            ):

                sources = message["sources"]

                if sources:

                    with st.expander(
                        "📚 Sources"
                    ):

                        for i, source in enumerate(
                            sources,
                            start=1
                        ):

                            chunk = source["chunk"]

                            start = chunk["start"]
                            end = chunk["end"]

                            start_seconds = (
                                timestamp_to_seconds(start)
                            )

                            video_id = get_video_id(
                                st.session_state.processed_url
                            )

                            timestamp_url = (
                                f"https://www.youtube.com/"
                                f"watch?v={video_id}"
                                f"&t={start_seconds}s"
                            )

                            st.markdown(
                                f"**Source {i}** — "
                                f"[{start:.2f}s → {end:.2f}s]"
                                f"({timestamp_url})"
                            )

                            st.caption(
                                chunk["text"]
                            )

                            if i < len(sources):

                                st.divider()


    # ========================================================
    # CHAT INPUT
    # ========================================================

    question = st.chat_input(
        "Ask something about this video..."
    )


    if question:

        # -----------------------------------------------
        # Display user question
        # -----------------------------------------------

        with st.chat_message("user"):

            st.markdown(
                question
            )


        # -----------------------------------------------
        # Save user question temporarily
        # -----------------------------------------------

        previous_history = (
            st.session_state.messages.copy()
        )


        # -----------------------------------------------
        # Generate answer
        # -----------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "🧠 Thinking..."
            ):

                try:

                    result = (
                        st.session_state.pipeline
                        .ask(
                            question=question,
                            chat_history=previous_history
                        )
                    )

                    answer = result["answer"]

                    sources = result["sources"]


                    # Display answer
                    st.markdown(
                        answer
                    )


                    # Display sources
                    if sources:

                        with st.expander(
                            "📚 Sources"
                        ):

                            for i, source in enumerate(
                                sources,
                                start=1
                            ):

                                chunk = source["chunk"]

                                start = chunk["start"]
                                end = chunk["end"]

                                start_seconds = (
                                    timestamp_to_seconds(start)
                                )

                                video_id = get_video_id(
                                    st.session_state.processed_url
                                )

                                timestamp_url = (
                                    f"https://www.youtube.com/"
                                    f"watch?v={video_id}"
                                    f"&t={start_seconds}s"
                                )

                                st.markdown(
                                    f"**Source {i}** — "
                                    f"[{start:.2f}s → "
                                    f"{end:.2f}s]"
                                    f"({timestamp_url})"
                                )

                                st.caption(
                                    chunk["text"]
                                )

                                if i < len(sources):

                                    st.divider()


                    # -----------------------------------
                    # Save conversation
                    # -----------------------------------

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": question
                        }
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources
                        }
                    )


                except Exception as e:

                    error_message = (
                        "❌ Sorry, I couldn't generate "
                        "an answer.\n\n"
                        f"Error: {e}"
                    )

                    st.error(
                        error_message
                    )

                    st.session_state.messages.append(
                        {
                            "role": "user",
                            "content": question
                        }
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                            "sources": []
                        }
                    )


# ============================================================
# INITIAL STATE MESSAGE
# ============================================================

else:

    st.divider()

    st.info(
        "👆 Paste a YouTube URL above and click "
        "**🚀 Process Video** to get started."
    )