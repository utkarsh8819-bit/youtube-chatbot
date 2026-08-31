def retrieve_documents(vector_store, embedding_model, query, k=3):
    """
    Retrieve the most relevant transcript chunks for a query.
    """

    results = vector_store.similarity_search(
        query,
        embedding_model,
        k=k
    )

    return results