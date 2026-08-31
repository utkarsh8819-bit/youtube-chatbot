from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    """
    Create and return the multilingual embedding model.

    This model supports multiple languages and is better
    suited for English questions over Hindi transcripts.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embedding_model